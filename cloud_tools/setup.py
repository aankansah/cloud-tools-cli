from setuptools import setup, find_packages

setup(
    name="cloud-tools",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "typer",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "cloud-tools=cloud_tools.cli:app",
        ],
    },
)