# Cloud Tools CLI

**Cloud Tools CLI** is a modular command-line toolkit for AWS cloud operations. It provides multiple tools to help DevOps engineers, cloud auditors, and developers manage AWS resources, detect security risks, enforce tagging policies, and visualize infrastructure.

Perfect for:

- **Security audits** of your AWS infrastructure
- **Cost optimization** by cleaning up old snapshots
- **Compliance enforcement** through tag validation
- **Network visibility** and port exposure scanning

---

## Prerequisites

Before installing Cloud Tools CLI, ensure you have:

- **Python 3.9 or higher** — Check with: `python3 --version`
- **AWS Account** — With access to resources you want to scan
- **AWS CLI** (optional but recommended) — For credential configuration
- **Git** — For cloning the repository

### Check Prerequisites

```bash
# Check Python version
python3 --version

# Check if git is installed
git --version

# Check if AWS CLI is installed (optional)
aws --version
```

If you're missing any prerequisites:

- **Python**: Download from [python.org](https://www.python.org/downloads/)
- **Git**: Install from [git-scm.com](https://git-scm.com/download/mac)
- **AWS CLI**: Install via `pip install awscli` or download from [aws.amazon.com](https://aws.amazon.com/cli/)

---

## Features

* **Audit** -- Scan AWS resources (EC2, Security Groups, S3 Buckets) for public exposure and security risks
  * Detects Security Groups with inbound rules open to `0.0.0.0/0`
  * Identifies EC2 instances with public IP addresses
  * Finds S3 buckets with public ACLs
  * Displays findings in a formatted table with region, resource details, and tags
* **Snapshot Cleaner** -- Scan and clean EBS snapshots
* **Tag Checker** -- Validate resource tags across regions (planned)
* **Port Visualizer** -- Visualize open ports in your VPC (planned)

**All tools support scanning a single region or all AWS regions.**

---

## Installation

### Step 1: Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/aankansah/cloud-tools-cli.git
cd cloud-tools-cli
```

If you get an error, make sure:

- Git is installed: `git --version`
- You have internet access
- The repository URL is correct

### Step 2: Create a Python Virtual Environment

A virtual environment isolates this project's dependencies from your system Python:

```bash
python3 -m venv venv
```

This creates a `venv/` folder in your project directory. You should see:

```bash
ls -la venv/
# bin/  include/  lib/  pyvenv.cfg
```

### Step 3: Activate the Virtual Environment

**For macOS/Linux (zsh or bash):**

```bash
source venv/bin/activate
```

You should see `(venv)` appear at the beginning of your terminal prompt:

```
(venv) user@machine cloud-tools %
```

**For Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

**For Windows (Command Prompt):**

```cmd
venv\Scripts\activate.bat
```

### Step 4: Install the Package and Dependencies

With the virtual environment activated, install the package:

```bash
pip install -e .
```

This installs:

- `boto3` — AWS SDK for Python
- `typer` — CLI framework
- `rich` — Beautiful terminal output
- The `cloud-tools` CLI itself

Installation should complete without errors (may take 1-2 minutes).

### Step 5: Verify Installation

Test that the installation worked:

```bash
cloud-tools --help
```

You should see output like:

```
 Usage: cloud-tools [OPTIONS] COMMAND [ARGS]...

 Cloud Tools CLI Suite

 Commands:
   audit             Run cloud audit checks
   tag-checker       Check resource tags
   snapshot-cleaner  Clean snapshots
   port-visualizer   Visualize open ports
```

If you get `command not found: cloud-tools`, make sure your virtual environment is activated (`source venv/bin/activate`).

### Step 6: (Recommended) Set Up Global Access

So you can run `cloud-tools` from any terminal without activating the virtual environment:

#### For macOS/Linux Users:

Add this line to your shell configuration file:

**If using zsh** (default on modern macOS):

```bash
echo 'alias cloud-tools="/path/to/cloud-tools/cloud-tools.sh"' >> ~/.zshrc
source ~/.zshrc
```

Replace `/path/to/cloud-tools/` with your actual project path. Find it with:

```bash
pwd  # while in the cloud-tools directory
```

**If using bash**:

```bash
echo 'alias cloud-tools="/path/to/cloud-tools/cloud-tools.sh"' >> ~/.bashrc
source ~/.bashrc
```

Now open a **new terminal window** and test:

```bash
cloud-tools --help
```

#### For Windows Users:

You'll need to activate the venv before running commands. Create a shortcut or batch file:

**Option A: Create a batch file** (easiest)

1. Create a file named `cloud-tools.bat` in your project directory:

```batch
@echo off
call venv\Scripts\activate.bat
python -m cloud_tools.cli %*
```

2. Add the project directory to PATH, or create an alias in PowerShell:

```powershell
Set-Alias -Name cloud-tools -Value "C:\path\to\cloud-tools\cloud-tools.bat"
```

---

## AWS Credentials Setup

The tools need AWS credentials to access your AWS account. You have three options:

### Option 1: AWS Credentials File (Easiest for Most Users)

1. Get your AWS Access Key ID and Secret Access Key:

   - Log in to [AWS Console](https://console.aws.amazon.com)
   - Go to **IAM > Users > Your Username > Security Credentials**
   - Create an "Access key for CLI"
   - Copy the **Access Key ID** and **Secret Access Key**
2. Create AWS credentials file:

**On macOS/Linux:**

```bash
mkdir -p ~/.aws
cat > ~/.aws/credentials << EOF
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY

[production]
aws_access_key_id = PRODUCTION_ACCESS_KEY_ID
aws_secret_access_key = PRODUCTION_SECRET_ACCESS_KEY
EOF
```

**On Windows PowerShell:**

```powershell
New-Item -Path "$env:USERPROFILE\.aws" -ItemType Directory -Force
@"
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY

[production]
aws_access_key_id = PRODUCTION_ACCESS_KEY_ID
aws_secret_access_key = PRODUCTION_SECRET_ACCESS_KEY
"@ | Out-File -FilePath "$env:USERPROFILE\.aws\credentials" -Encoding ASCII
```

3. Verify it works:

```bash
aws sts get-caller-identity
```

You should see your AWS account ID and user ARN.

### Option 2: AWS Configure Command

If you have AWS CLI installed:

```bash
aws configure --profile my-profile
# AWS Access Key ID [None]: YOUR_ACCESS_KEY_ID
# AWS Secret Access Key [None]: YOUR_SECRET_ACCESS_KEY
# Default region name [None]: us-east-1
# Default output format [None]: json
```

Then use it:

```bash
export AWS_PROFILE=my-profile
cloud-tools audit scan
```

### Option 3: Environment Variables

Set credentials directly (useful for CI/CD):

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"

cloud-tools audit scan
```

### Option 4: IAM Roles (For EC2/ECS/Lambda)

If running on an AWS resource (EC2 instance, ECS task, Lambda), the tools automatically use the resource's IAM role. No configuration needed!

---

## Quick Start

Once installed and credentials are set up, choose a strategy:

### Strategy 1: Default Credentials (Easiest)

If you've set up credentials in `~/.aws/credentials` or have an IAM role:

```bash
cloud-tools audit scan
cloud-tools tag-checker scan
cloud-tools snapshot-cleaner scan
```

### Strategy 2: Use AWS_PROFILE Environment Variable

Set it once per terminal session:

```bash
export AWS_PROFILE=my-profile
cloud-tools audit scan
cloud-tools tag-checker scan
```

Or add it permanently to your shell config (`~/.zshrc` or `~/.bashrc`):

```bash
# Add this line to ~/.zshrc or ~/.bashrc
export AWS_PROFILE=my-profile
```

### Strategy 3: Specify Profile Per Command

Override the profile for a specific command:

```bash
cloud-tools audit scan --profile production
cloud-tools tag-checker scan --profile dev --region us-west-2
```

---

## Usage Guide

### Audit Tool — Find Security Risks

Scan all regions:

```bash
cloud-tools audit scan
```

Scan a specific region:

```bash
cloud-tools audit scan --region us-east-1
cloud-tools audit scan -r us-west-2
```

Specify a profile:

```bash
cloud-tools audit scan --profile production
```

Combine options:

```bash
cloud-tools audit scan --region us-east-1 --profile staging
```

**What it checks for:**

| Finding                                         | Severity  | Fix                                              |
| ----------------------------------------------- | --------- | ------------------------------------------------ |
| **Security Group with 0.0.0.0/0 inbound** | 🔴 High   | Restrict to specific IPs/security groups         |
| **EC2 Instance with Public IP**           | 🟡 Medium | Use AWS Systems Manager or API Gateway instead   |
| **S3 Bucket with Public ACL**             | 🔴 High   | Use bucket policies with restrictive permissions |

**Example output:**

```
🚨 Exposure Report
┏━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Region  ┃ Type        ┃ Name        ┃ ID     ┃ Tags        ┃ Issue        ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ us-east │ Sec.Group   │ web-sg      │ sg-123 │ Name=web    │ Open to 0.0... │
└─────────┴─────────────┴─────────────┴────────┴─────────────┴────────────────┘
Total Findings: 1
```

---

### Snapshot Cleaner — Manage EBS Snapshots

Scan all regions for old snapshots:

```bash
cloud-tools snapshot-cleaner scan
```

Scan a specific region:

```bash
cloud-tools snapshot-cleaner scan --region us-east-1
```

Scan snapshots older than 60 days:

```bash
cloud-tools snapshot-cleaner scan --age-days 60
```

Preview and delete snapshots:

```bash
# Dry run (preview without deleting)
cloud-tools snapshot-cleaner scan --age-days 30 --delete --dry-run

# Actually delete (with confirmation prompt)
cloud-tools snapshot-cleaner scan --age-days 30 --delete
```

Combine options:

```bash
cloud-tools snapshot-cleaner scan --region us-east-1 --age-days 30 --delete
```

**Optional flags:**

| Flag                          | Purpose                                                |
| ----------------------------- | ------------------------------------------------------ |
| `--age-days 30`             | Snapshots older than 30 days (default)                 |
| `--delete`                  | Delete snapshots (requires confirmation)               |
| `--dry-run`                 | Preview deletions without actually deleting            |
| `--include-stopped-volumes` | Show volumes from stopped instances (default: enabled) |

---

### Tag Checker — Enforce Tagging Standards

Scan all regions:

```bash
cloud-tools tag-checker scan
```

Scan a specific region:

```bash
cloud-tools tag-checker scan --region us-east-1
```

Specify a profile:

```bash
cloud-tools tag-checker scan --profile compliance-check
```

**Default required tags:**

| Tag             | Purpose                    |
| --------------- | -------------------------- |
| `Name`        | Resource identifier        |
| `Environment` | dev/staging/prod           |
| `Owner`       | Team or person responsible |

To change required tags, edit [cloud_tools/config.py](cloud_tools/config.py):

```python
REQUIRED_TAGS = ["Name", "Environment", "Owner", "CostCenter", "Application"]
```

---

### Port Visualizer — Find Open Ports

Scan all regions:

```bash
cloud-tools port-visualizer scan
```

Scan a specific region:

```bash
cloud-tools port-visualizer scan --region us-east-1
```

Specify a profile:

```bash
cloud-tools port-visualizer scan --profile production
```

---

## Configuration

All settings are centralized in [cloud_tools/config.py](cloud_tools/config.py) for easy customization.

### AWS Profile for All Tools

By default, tools use boto3's credential chain. Set a default profile:

```python
# In cloud_tools/config.py
AWS_PROFILE_NAME = "my-default-profile"  # or None to use boto3 default
```

Or set via environment variable (takes precedence):

```bash
export AWS_PROFILE=my-profile
cloud-tools audit scan
```

### Security Settings

```python
# CIDR block considered "open" to internet
OPEN_CIDR = "0.0.0.0/0"

# S3 public grantee identifier
PUBLIC_GRANTEE_IDENTIFIER = "AllUsers"
```

### Tag Enforcement

```python
# Required tags for all resources
REQUIRED_TAGS = ["Name", "Environment", "Owner"]

# Custom example for your organization:
REQUIRED_TAGS = [
    "Name",           # Resource identifier
    "Environment",    # dev/staging/prod
    "Owner",          # Team responsible
    "CostCenter",     # For billing
    "Application",    # Which app uses it
    "Compliance",     # Compliance requirement
]
```

### Snapshot Management

```python
# Default age threshold for snapshots
DEFAULT_AGE_DAYS = 30

# Example: Clean up snapshots older than 90 days
DEFAULT_AGE_DAYS = 90
```

### Apply Configuration Changes

After editing [cloud_tools/config.py](cloud_tools/config.py), changes take effect immediately. No reinstall needed.

---

## Troubleshooting

### Issue: "command not found: cloud-tools"

**Cause:** Virtual environment not activated or alias not set up.

**Fix:**

1. Activate virtual environment:

   ```bash
   cd /path/to/cloud-tools
   source venv/bin/activate
   ```
2. Or set up the alias (see Installation Step 6)

### Issue: "ModuleNotFoundError: No module named 'boto3'"

**Cause:** Dependencies not installed.

**Fix:**

```bash
cd /path/to/cloud-tools
source venv/bin/activate
pip install -e .
```

### Issue: "Unable to locate credentials"

**Cause:** AWS credentials not configured.

**Fix:** See [AWS Credentials Setup](#aws-credentials-setup) section above.

### Issue: "An error occurred (UnauthorizedOperation)"

**Cause:** AWS credentials don't have permission for the action.

**Fix:**

1. Verify your credentials work:

   ```bash
   aws sts get-caller-identity --profile your-profile
   ```
2. Ensure your IAM user/role has permissions:

   - `ec2:DescribeInstances`
   - `ec2:DescribeSecurityGroups`
   - `ec2:DescribeRegions`
   - `s3:ListAllMyBuckets` (for audit tool)
   - `ec2:DescribeSnapshots` (for snapshot-cleaner)
3. Contact your AWS administrator to grant permissions.

### Issue: "No such file or directory"

**Cause:** Wrong working directory or incorrect path.

**Fix:**

```bash
# Make sure you're in the project directory
cd /path/to/cloud-tools
pwd  # should show the full path
```

---

## Common Use Cases

### Use Case 1: Regular Security Audit

Run weekly to find and remediate security issues:

```bash
# Check all regions for exposures
cloud-tools audit scan --profile production

# Export for review
cloud-tools audit scan --profile production > audit-report.txt
```

### Use Case 2: Cost Optimization

Clean up old snapshots monthly:

```bash
# Preview snapshots older than 60 days
cloud-tools snapshot-cleaner scan --age-days 60 --profile production

# Delete with confirmation
cloud-tools snapshot-cleaner scan --age-days 60 --delete --profile production
```

### Use Case 3: Compliance Enforcement

Check if all resources are properly tagged:

```bash
# Find untagged resources
cloud-tools tag-checker scan --profile compliance

# Fix tags and re-check
# ... add tags in AWS Console ...
cloud-tools tag-checker scan --profile compliance
```

### Use Case 4: Network Security Review

Identify all open ports across infrastructure:

```bash
# See all open ports
cloud-tools port-visualizer scan --profile production

# Check specific region
cloud-tools port-visualizer scan --region us-east-1 --profile production
```

### Use Case 5: Automated CI/CD Integration

Use in your CI/CD pipeline for automated checks:

```bash
#!/bin/bash
# ci-check.sh

export AWS_ACCESS_KEY_ID=${{ secrets.AWS_ACCESS_KEY_ID }}
export AWS_SECRET_ACCESS_KEY=${{ secrets.AWS_SECRET_ACCESS_KEY }}
export AWS_DEFAULT_REGION=us-east-1

# Install
pip install -e .

# Run checks
cloud-tools audit scan
cloud-tools tag-checker scan

# Exit with error if findings exist
[ $? -eq 0 ] || exit 1
```

---

## FAQ

### Q: Can I use this with read-only AWS credentials?

**A:** Yes! The tools only read AWS resources. Use an IAM user/role with `read` permissions only.

### Q: Does this tool modify AWS resources?

**A:** Only the `snapshot-cleaner` with `--delete` flag can delete snapshots. All other tools are read-only.

### Q: Can I use this on Windows?

**A:** Yes, but you need to activate the virtual environment in PowerShell or Command Prompt first (Step 3).

### Q: How often should I run these tools?

**A:**

- **Audit**: Weekly or after infrastructure changes
- **Snapshot Cleaner**: Monthly
- **Tag Checker**: Weekly or after policy changes
- **Port Visualizer**: After security group changes

### Q: Can I schedule these to run automatically?

**A:** Yes! Use cron (macOS/Linux) or Task Scheduler (Windows).

**Example cron job** (runs audit daily at 8am):

```bash
# Edit with: crontab -e

0 8 * * * /path/to/cloud-tools/cloud-tools.sh audit scan --profile production > /tmp/audit.log 2>&1
```

### Q: Do my AWS credentials get stored or sent anywhere?

**A:** No. This tool runs locally and only communicates with your AWS account. No data is sent to any external service.

---

## Contributing

Contributions welcome! Here's how to add a new tool:

1. Create a new module in `cloud_tools/`:

```python
# cloud_tools/my_tool.py
import typer
from rich.console import Console

app = typer.Typer(help="My custom tool")
console = Console()

@app.command()
def scan():
    console.print("Hello from my tool!")
```

2. Register in [cloud_tools/cli.py](cloud_tools/cli.py):

```python
from cloud_tools import my_tool

app.add_typer(my_tool.app, name="my-tool")
```

3. Test it:

```bash
cloud-tools my-tool scan
```

---

## Project Structure

```text
cloud-tools/
├── cloud_tools/
│   ├── __init__.py              # Package initialization
│   ├── cli.py                   # Main CLI entry point
│   ├── config.py                # Centralized configuration ⚙️
│   ├── audit.py                 # Security audit tool
│   ├── snapshot_cleaner.py       # EBS snapshot management
│   ├── tag_checker.py           # Resource tagging validator
│   └── port_visualizer.py        # Open ports scanner
├── venv/                         # Virtual environment (created after setup)
├── docs/
│   └── images/                  # Example screenshots
├── pyproject.toml               # Project metadata & dependencies
├── README.md                    # This file
├── LICENSE.txt                  # MIT License
├── cloud-tools.sh              # CLI wrapper script
└── .gitignore                  # Git ignore file
```

---

## Project Architecture

The tools follow a modular design using **Typer** for CLI and **boto3** for AWS API calls:

```
┌─────────────────────────────────────┐
│   User Terminal Command             │
│   $ cloud-tools audit scan          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   cloud_tools/cli.py                │
│   (CLI Router & Entry Point)        │
└──────────────┬──────────────────────┘
               │
       ┌───────┴─────────┬──────────────┬──────────────┐
       ▼                 ▼              ▼              ▼
   audit.py         snapshot_      tag_checker   port_visualizer
                    cleaner.py
       │                 │              │              │
       └─────────────────┴──────────────┴──────────────┘
               │
               ▼
   boto3 (AWS API Calls)
               │
               ▼
        AWS Services
   (EC2, S3, CloudWatch, etc.)
```

All configuration is centralized in `config.py` — edit once, applies to all tools.

---

## License

MIT License — See [LICENSE.txt](LICENSE.txt) for details.

---

## Why This Tool Exists

Managing cloud infrastructure manually is error-prone and risky. **Cloud Tools CLI** was built to:

* 🔒 Provide security audits with actionable findings
* 💰 Help optimize costs by identifying unused resources
* ✅ Enforce compliance through automated tag checking
* 👀 Give visibility into open ports and network exposure
* 🛠️ Offer a modular toolkit that grows with your needs

---

## Support & Feedback

Found a bug? Have a feature request?

- **Issues**: [GitHub Issues](https://github.com/yourusername/cloud-tools-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/cloud-tools-cli/discussions)

---

## Acknowledgments

Built with:

- [boto3](https://boto3.amazonaws.com/) — AWS SDK for Python
- [Typer](https://typer.tiangolo.com/) — CLI framework
- [Rich](https://rich.readthedocs.io/) — Beautiful terminal output
