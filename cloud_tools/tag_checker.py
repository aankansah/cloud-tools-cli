import boto3
import typer
from rich.console import Console
from rich.table import Table
from cloud_tools import config

app = typer.Typer(help="Check AWS resource tags")
console = Console()

def get_boto3_session(region_name=None):
    return boto3.Session(profile_name=config.AWS_PROFILE_TAG_CHECKER, region_name=region_name)

def get_all_regions():
    session = get_boto3_session("us-east-1")
    ec2 = session.client("ec2")
    return [r["RegionName"] for r in ec2.describe_regions()["Regions"]]

def format_tags(tags_list):
    if not tags_list:
        return "-"
    return ", ".join(f"{t['Key']}={t['Value']}" for t in tags_list)

def check_tags(tags_list):
    missing = [tag for tag in config.REQUIRED_TAGS if tag not in [t["Key"] for t in tags_list]]
    return missing

def scan_ec2_instances(session):
    ec2 = session.client("ec2")
    findings = []
    for reservation in ec2.describe_instances()["Reservations"]:
        for instance in reservation["Instances"]:
            tags = instance.get("Tags", [])
            missing_tags = check_tags(tags)
            if missing_tags:
                findings.append({
                    "type": "EC2 Instance",
                    "resource_id": instance["InstanceId"],
                    "resource_name": next((t["Value"] for t in tags if t["Key"]=="Name"), "-"),
                    "tags": format_tags(tags),
                    "missing_tags": ", ".join(missing_tags)
                })
    return findings

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
        findings = scan_ec2_instances(session)
        for f in findings:
            f["region"] = reg
        all_findings.extend(findings)

    if not all_findings:
        console.print("[bold green]✅ All resources have required tags.[/bold green]")
        return

    table = Table(title="🚨 Missing Tags Report")
    table.add_column("Region", style="cyan")
    table.add_column("Resource Type", style="magenta")
    table.add_column("Resource Name", style="yellow")
    table.add_column("Resource ID", style="green")
    table.add_column("Tags", style="blue")
    table.add_column("Missing Tags", style="red")

    for f in all_findings:
        table.add_row(f["region"], f["type"], f["resource_name"], f["resource_id"], f["tags"], f["missing_tags"])

    console.print(table)
    console.print(f"\n[bold red]Total Resources Missing Tags: {len(all_findings)}[/bold red]")