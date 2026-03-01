#!/usr/bin/env python3
import typer

from cloud_tools import audit
from cloud_tools import tag_checker
from cloud_tools import snapshot_cleaner
from cloud_tools import port_visualizer

app = typer.Typer(help="Cloud Tools CLI Suite")

# Add commands
app.add_typer(audit.app, name="audit", help="Run cloud audit checks")
app.add_typer(tag_checker.app, name="tag-checker", help="Check resource tags")
app.add_typer(snapshot_cleaner.app, name="snapshot-cleaner", help="Clean snapshots")
app.add_typer(port_visualizer.app, name="port-visualizer", help="Visualize open ports")

if __name__ == "__main__":
    app()