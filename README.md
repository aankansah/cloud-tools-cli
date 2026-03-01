
# Cloud Tools CLI

**Cloud Tools CLI** is a modular command-line toolkit for AWS cloud operations.  
It provides multiple tools to help DevOps engineers, cloud auditors, and developers manage AWS resources, detect security risks, enforce tagging policies, and visualize infrastructure.

---

## Features

- **Audit** – Scan AWS resources (EC2, Security Groups, S3 Buckets) for public exposure and security risks
  - Detects Security Groups with inbound rules open to `0.0.0.0/0`
  - Identifies EC2 instances with public IP addresses
  - Finds S3 buckets with public ACLs
  - Displays findings in a formatted table with region, resource details, and tags
- **Tag Checker** – Validate resource tags across regions (planned).
- **Snapshot Cleaner** – Clean unused EBS snapshots (planned).
- **Port Visualizer** – Visualize open ports in your VPC (planned).

**All tools support scanning a single region or all AWS regions.**

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/cloud-tools-cli.git
cd cloud-tools-cli
```

2. Install in editable mode:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

3. Ensure you have an AWS CLI profile set up. You can use any profile name; for example:

```bash
aws configure --profile <your-profile-name>
```

Replace `<your-profile-name>` with the profile you will use when running the tools.

---

## Usage

### Audit Tool

Scan all regions:

```bash
./main.py
```

Scan a specific region:

```bash
./main.py --region us-east-1
# or
./main.py -r us-east-1
```

**Example Output:**

```
Scanning specified region: us-east-1

Scanning region: us-east-1
                                                   🚨 Exposure Report                                                   
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Region    ┃ Resource Type  ┃ Resource Name   ┃ Resource ID          ┃ Tags               ┃ Issue                     ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ us-east-1 │ Security Group │ launch-wizard-1 │ sg-0984e10ba44ad0cac │ -                  │ Open port(s) to 0.0.0.0/0 │
│ us-east-1 │ Security Group │ launch-wizard-1 │ sg-0984e10ba44ad0cac │ -                  │ Open port(s) to 0.0.0.0/0 │
│ us-east-1 │ EC2 Instance   │ Sample Server   │ i-00fd50e6204d72f72  │ Name=Sample Server │ Public IP: 54.91.107.51   │
└───────────┴────────────────┴─────────────────┴──────────────────────┴────────────────────┴───────────────────────────┘

Total Findings: 3
```

The tool scans for:
- **Security Groups** with inbound rules open to `0.0.0.0/0`
- **EC2 Instances** with public IP addresses
- **S3 Buckets** with public ACLs

### Future Tools (Coming Soon)

- **Tag Checker:** Validate resource tags across specified regions
- **Snapshot Cleaner:** Clean unused EBS snapshots
- **Port Visualizer:** Visualize open ports in your VPC

---

## Project Structure

```text
cloud-tools/
├── cloud_tools/
│   ├── __init__.py
│   ├── cli.py
│   ├── audit.py
│   ├── tag_checker.py
│   ├── snapshot_cleaner.py
│   └── port_visualizer.py
├── tests/
├── setup.py
└── README.md
```

---

## Contributing

Contributions are welcome!  
- Add new tools by creating a new module with a `Typer` app.  
- Register it in `cli.py` with `app.add_typer(...)`.

---

## License

MIT License

---

## Why This Tool Exists

Managing cloud infrastructure manually is error-prone and risky.  
**Cloud Tools CLI** was built to:

- Provide DevOps engineers with actionable visibility of AWS resources.
- Help developers enforce security best practices.
- Serve as a modular toolkit that grows as your cloud environment evolves.