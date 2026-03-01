import boto3
import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from cloud_tools import config

app = typer.Typer()
console = Console()


def get_regions(session):
    ec2 = session.client("ec2")
    response = ec2.describe_regions()
    return [r["RegionName"] for r in response["Regions"]]


def get_boto3_session(profile_name=None):
    # Priority: arg > config > boto3 default
    profile = profile_name or config.AWS_PROFILE_NAME
    return boto3.Session(profile_name=profile)


def scan_security_groups(session, region: str):
    ec2 = session.client("ec2", region_name=region)
    response = ec2.describe_security_groups()

    findings = []

    for sg in response["SecurityGroups"]:
        sg_name = sg.get("GroupName")
        sg_id = sg.get("GroupId")

        for permission in sg.get("IpPermissions", []):
            ip_ranges = permission.get("IpRanges", [])
            protocol = permission.get("IpProtocol")

            from_port = permission.get("FromPort")
            to_port = permission.get("ToPort")

            for ip_range in ip_ranges:
                if ip_range.get("CidrIp") == config.OPEN_CIDR:
                    findings.append(
                        {
                            "Region": region,
                            "SecurityGroup": sg_name,
                            "SecurityGroupId": sg_id,
                            "Protocol": protocol,
                            "PortRange": f"{from_port}-{to_port}" if from_port is not None else "All",
                            "Source": config.OPEN_CIDR,
                        }
                    )

    return findings


@app.command()
def scan(
    region: Optional[str] = typer.Option(None, "--region", "-r", help="AWS region"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p", help="AWS profile name (overrides AWS_PROFILE env var)"),
):
    """
    Visualize open ports to {config.OPEN_CIDR} in Security Groups.
    """

    session = get_boto3_session(profile)

    regions: List[str]

    if region:
        console.print(f"Scanning specified region: {region}\n")
        regions = [region]
    else:
        console.print("Scanning all regions...\n")
        regions = get_regions(session)

    all_findings = []

    for reg in regions:
        console.print(f"Scanning region: {reg}")
        findings = scan_security_groups(session, reg)
        all_findings.extend(findings)

    if not all_findings:
        console.print(f"\n✅ No open ports exposed to {config.OPEN_CIDR} found.")
        raise typer.Exit()

    table = Table(title=f"🚨 Open Ports to {config.OPEN_CIDR}")

    table.add_column("Region", style="cyan")
    table.add_column("Security Group")
    table.add_column("SG ID")
    table.add_column("Protocol")
    table.add_column("Port Range")
    table.add_column("Source")

    for item in all_findings:
        table.add_row(
            item["Region"],
            item["SecurityGroup"],
            item["SecurityGroupId"],
            item["Protocol"],
            item["PortRange"],
            item["Source"],
        )

    console.print()
    console.print(table)
    console.print(f"\nTotal Open Ports Found: {len(all_findings)}")