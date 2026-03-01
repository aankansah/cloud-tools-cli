"""
Centralized configuration for Cloud Tools CLI.

Edit this file to customize settings across all tools.
"""

import os

# ============================================================================
# AWS Profile Configuration
# ============================================================================
# AWS profile to use for all tools. Set to None to use boto3's default credential chain.
#
# Priority order:
# 1. AWS_PROFILE environment variable (if set)
# 2. AWS_PROFILE_NAME variable below (if set)
# 3. boto3's default credential chain (IAM role, ~/.aws/credentials, etc.)
#
# Configure profiles with: aws configure --profile <profile-name>
# Or set environment variable: export AWS_PROFILE=<profile-name>

AWS_PROFILE_NAME = os.getenv("AWS_PROFILE")


# ============================================================================
# Security & Exposure Detection
# ============================================================================
# CIDR block considered "open" to the internet
OPEN_CIDR = "0.0.0.0/0"

# S3 public grantee identifier
PUBLIC_GRANTEE_IDENTIFIER = "AllUsers"


# ============================================================================
# Tag Enforcement
# ============================================================================
# Required tags that should be present on all resources
REQUIRED_TAGS = ["Name", "Environment", "Owner"]


# ============================================================================
# Snapshot Management
# ============================================================================
# Default age in days for considering snapshots as "old" and eligible for cleanup
DEFAULT_AGE_DAYS = 30
