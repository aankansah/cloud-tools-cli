import boto3
import typer
from rich.console import Console
from rich.table import Table
from botocore.exceptions import ClientError
from cloud_tools import config

app = typer.Typer(help="Run cloud audit checks")
console = Console()

# Helper functions
def get_boto3_session(region_name=None, profile_name=None):
    # Priority: CLI arg > config > boto3 default
    profile = profile_name or config.AWS_PROFILE_NAME
    return boto3.Session(profile_name=profile, region_name=region_name)

def get_all_regions():
    session = get_boto3_session("us-east-1")
    ec2 = session.client("ec2")
    return [r["RegionName"] for r in ec2.describe_regions()["Regions"]]

def format_tags(tags_list):
    if not tags_list:
        return "-"
    return ", ".join(f"{t['Key']}={t['Value']}" for t in tags_list)

def get_resource_name(tags_list, default_name="-"):
    if not tags_list:
        return default_name
    for tag in tags_list:
        if tag["Key"] == "Name":
            return tag["Value"]
    return default_name

# Scanning functions (EC2, SG, S3)
def scan_security_groups(session):
    ec2 = session.client("ec2")
    findings = []
    for sg in ec2.describe_security_groups()["SecurityGroups"]:
        tags = sg.get("Tags", [])
        name = get_resource_name(tags, sg.get("GroupName", "-"))
        for rule in sg.get("IpPermissions", []):
            for ip_range in rule.get("IpRanges", []):
                if ip_range.get("CidrIp") == config.OPEN_CIDR:
                    findings.append({
                        "type": "Security Group",
                        "resource_id": sg["GroupId"],
                        "resource_name": name,
                        "tags": format_tags(tags),
                        "detail": f"Open port(s) to {config.OPEN_CIDR}"
                    })
    return findings

def scan_ec2_instances(session):
    ec2 = session.client("ec2")
    findings = []
    for reservation in ec2.describe_instances()["Reservations"]:
        for instance in reservation["Instances"]:
            if "PublicIpAddress" in instance:
                tags = instance.get("Tags", [])
                name = get_resource_name(tags)
                findings.append({
                    "type": "EC2 Instance",
                    "resource_id": instance["InstanceId"],
                    "resource_name": name,
                    "tags": format_tags(tags),
                    "detail": f"Public IP: {instance['PublicIpAddress']}"
                })
    return findings

def scan_s3_buckets(session):
    s3 = session.client("s3")
    findings = []
    for bucket in s3.list_buckets()["Buckets"]:
        bucket_name = bucket["Name"]
        try:
            s3.get_public_access_block(Bucket=bucket_name)
        except ClientError:
            acl = s3.get_bucket_acl(Bucket=bucket_name)
            for grant in acl["Grants"]:
                if config.PUBLIC_GRANTEE_IDENTIFIER in str(grant.get("Grantee", {})):
                    findings.append({
                        "type": "S3 Bucket",
                        "resource_id": bucket_name,
                        "resource_name": bucket_name,
                        "tags": "-",
                        "detail": "Public ACL detected"
                    })
    return findings

# CLI command
@app.command()
def scan(
    region: str = typer.Option(None, "--region", "-r", help="Specify AWS region"),
    profile: str = typer.Option(None, "--profile", "-p", help="AWS profile name (overrides AWS_PROFILE env var)")
):
    if region:
        regions = [region]
        console.print(f"[bold blue]Scanning specified region: {region}[/bold blue]\n")
    else:
        console.print("[bold blue]No region specified, scanning all regions...[/bold blue]\n")
        regions = get_all_regions()
        console.print(f"[bold blue]Detected {len(regions)} regions: {', '.join(regions)}[/bold blue]\n")

    all_findings = []

    for reg in regions:
        console.print(f"[bold magenta]Scanning region: {reg}[/bold magenta]")
        session = get_boto3_session(reg, profile)

        findings = []
        findings.extend(scan_security_groups(session))
        findings.extend(scan_ec2_instances(session))
        if reg == regions[0]:
            findings.extend(scan_s3_buckets(session))

        for f in findings:
            f["region"] = reg
        all_findings.extend(findings)

    if not all_findings:
        console.print("[bold green]✅ No public exposure detected.[/bold green]")
        return

    table = Table(title="🚨 Exposure Report")
    table.add_column("Region", style="cyan")
    table.add_column("Resource Type", style="magenta")
    table.add_column("Resource Name", style="yellow")
    table.add_column("Resource ID", style="green")
    table.add_column("Tags", style="blue")
    table.add_column("Issue", style="red")

    for f in all_findings:
        table.add_row(f["region"], f["type"], f["resource_name"], f["resource_id"], f["tags"], f["detail"])

    console.print(table)
    console.print(f"\n[bold red]Total Findings: {len(all_findings)}[/bold red]")