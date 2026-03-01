
# Cloud Tools CLI

**Cloud Tools CLI** is a modular command-line toolkit for AWS cloud operations.  
It provides multiple tools to help DevOps engineers, cloud auditors, and developers manage AWS resources, detect security risks, enforce tagging policies, and visualize infrastructure.

---

## Features

- **Audit** – Scan AWS resources (EC2, S3, Security Groups) for public exposure.
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
cloud-tools audit scan
```

Scan a specific region:

```bash
cloud-tools audit scan --region us-east-1
# or
cloud-tools audit scan -r us-east-1
```

### Future Tools

- **Tag Checker:** 

```bash
cloud-tools tag-checker --region us-east-1
```

- **Snapshot Cleaner:** 

```bash
cloud-tools snapshot-cleaner --region us-east-1
```

- **Port Visualizer:** 

```bash
cloud-tools port-visualizer --region us-east-1
```

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