import boto3
import typer
from rich.console import Console
from rich.table import Table
from botocore.exceptions import ClientError
import datetime
from cloud_tools import config

app = typer.Typer(help="Scan and clean EBS snapshots")
console = Console()

def get_boto3_session(region_name=None, profile_name=None):
    # Priority: CLI arg > config > boto3 default
    profile = profile_name or config.AWS_PROFILE_NAME
    return boto3.Session(profile_name=profile, region_name=region_name)

def get_all_regions():
    session = get_boto3_session("us-east-1")
    ec2 = session.client("ec2")
    return [r["RegionName"] for r in ec2.describe_regions()["Regions"]]

def list_snapshots(session, age_days=config.DEFAULT_AGE_DAYS):
    """
    Return a list of snapshots older than `age_days`.
    """
    cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=age_days)
    ec2 = session.client("ec2")
    snapshots = []

    try:
        response = ec2.describe_snapshots(OwnerIds=["self"])
    except ClientError as e:
        console.print(f"[red]Error fetching snapshots: {e}[/red]")
        return snapshots

    for snap in response.get("Snapshots", []):
        start_time = snap["StartTime"].replace(tzinfo=None)
        if start_time < cutoff_date:
            snapshots.append({
                "SnapshotId": snap["SnapshotId"],
                "VolumeId": snap["VolumeId"],
                "StartTime": str(snap["StartTime"]),
                "Description": snap.get("Description", "-")
            })
    return snapshots

def list_volumes_from_stopped_instances(session):
    """
    Return a list of volumes attached to stopped instances.
    """
    ec2 = session.client("ec2")
    candidates = []
    try:
        reservations = ec2.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": ["stopped"]}]
        )["Reservations"]
    except ClientError as e:
        console.print(f"[red]Error fetching stopped instances: {e}[/red]")
        return candidates

    for res in reservations:
        for instance in res["Instances"]:
            for bdm in instance.get("BlockDeviceMappings", []):
                vol_id = bdm["Ebs"]["VolumeId"]
                candidates.append({
                    "VolumeId": vol_id,
                    "InstanceId": instance["InstanceId"],
                    "StartTime": "-",
                    "Description": "Volume from stopped instance, no snapshot yet"
                })
    return candidates

def delete_snapshot(session, snapshot_id):
    """
    Delete a snapshot by ID.
    """
    ec2 = session.client("ec2")
    try:
        ec2.delete_snapshot(SnapshotId=snapshot_id)
        console.print(f"[bold red]Deleted snapshot:[/bold red] {snapshot_id}")
        return True
    except ClientError as e:
        console.print(f"[red]Error deleting snapshot {snapshot_id}: {e}[/red]")
        return False

@app.command()
def scan(
    region: str = typer.Option(None, "--region", "-r", help="Specify AWS region"),
    profile: str = typer.Option(None, "--profile", "-p", help="AWS profile name (overrides AWS_PROFILE env var)"),
    age_days: float = typer.Option(config.DEFAULT_AGE_DAYS, "--age-days", "-a", help="Snapshots older than this are listed"),
    include_stopped_volumes: bool = typer.Option(True, "--include-stopped-volumes", help="Include volumes from stopped instances"),
    delete: bool = typer.Option(False, "--delete", "-d", help="Delete snapshots older than age_days"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview deletions without performing them")
):
    """
    Scan AWS snapshots older than a specified number of days.
    Optionally include volumes from stopped instances and delete snapshots.
    """
    if region:
        regions = [region]
        console.print(f"[bold blue]Scanning specified region: {region}[/bold blue]\n")
    else:
        console.print("[bold blue]No region specified, scanning all regions...[/bold blue]\n")
        regions = get_all_regions()
        console.print(f"[bold blue]Detected {len(regions)} regions: {', '.join(regions)}[/bold blue]\n")

    snapshots_to_delete = []
    stopped_volumes = []

    for reg in regions:
        console.print(f"[bold magenta]Scanning region: {reg}[/bold magenta]")
        session = get_boto3_session(reg, profile)

        # Snapshots
        snapshots = list_snapshots(session, age_days)
        for snap in snapshots:
            snap["Region"] = reg
        snapshots_to_delete.extend(snapshots)

        # Stopped volumes
        if include_stopped_volumes:
            stopped = list_volumes_from_stopped_instances(session)
            for vol in stopped:
                vol["Region"] = reg
            stopped_volumes.extend(stopped)

    # Display snapshots table
    if snapshots_to_delete:
        table = Table(title=f"🚨 Snapshots older than {age_days} days")
        table.add_column("Region", style="cyan")
        table.add_column("Snapshot ID", style="green")
        table.add_column("Volume ID", style="magenta")
        table.add_column("Start Time", style="yellow")
        table.add_column("Description", style="blue")

        for snap in snapshots_to_delete:
            table.add_row(snap["Region"], snap["SnapshotId"], snap["VolumeId"], snap["StartTime"], snap["Description"])
        console.print(table)
        console.print(f"[bold red]Total Snapshots Found: {len(snapshots_to_delete)}[/bold red]")

        # Delete snapshots
        if delete:
            confirm = typer.confirm(
                "Are you sure you want to delete these snapshots?",
                abort=True
            )
            if not dry_run:
                for snap in snapshots_to_delete:
                    delete_snapshot(session, snap["SnapshotId"])
            else:
                console.print("[bold yellow]Dry run enabled: No snapshots were deleted[/bold yellow]")
    else:
        console.print(f"[bold green]✅ No snapshots older than {age_days} days found.[/bold green]")

    # Display stopped volumes table
    if include_stopped_volumes and stopped_volumes:
        table = Table(title="ℹ️ Volumes from Stopped Instances (no snapshot yet)")
        table.add_column("Region", style="cyan")
        table.add_column("Volume ID", style="green")
        table.add_column("Instance ID", style="magenta")
        table.add_column("Start Time", style="yellow")
        table.add_column("Description", style="blue")

        for vol in stopped_volumes:
            table.add_row(vol["Region"], vol["VolumeId"], vol["InstanceId"], vol["StartTime"], vol["Description"])
        console.print(table)
        console.print(f"[bold yellow]Total Stopped Volumes Found: {len(stopped_volumes)}[/bold yellow]")