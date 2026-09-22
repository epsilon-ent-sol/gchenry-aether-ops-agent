"""
Tool definitions registered with the ADK Agent.
"""
import re
from typing import Dict, Any

def security_scan_manifest(manifest_content: str, environment: str = "production") -> Dict[str, Any]:
    """
    Scans Kubernetes/Cloud Run/Terraform configuration for critical vulnerabilities.
    """
    findings = []
    status = "PASSED"

    # Rule 1: Check for hardcoded credentials or API keys
    if re.search(r'(?i)(api[_-]?key|password|secret)\s*[:=]\s*["\'][a-zA-Z0-9_\-]{8,}["\']', manifest_content):
        findings.append("CRITICAL: Hardcoded API Key or Secret detected in configuration.")
        status = "FAILED"

    # Rule 2: Check for root user execution
    if "USER root" in manifest_content or 'runAsNonRoot: false' in manifest_content:
        findings.append("HIGH: Container configured to execute as root user.")
        status = "FAILED"

    # Rule 3: Check for wildcard open ingress in production
    if environment == "production" and "allUsers" in manifest_content and "admin" in manifest_content:
        findings.append("HIGH: Admin endpoint exposed unauthenticated to 'allUsers'.")
        status = "FAILED"

    if not findings:
        findings.append("All security and policy checks passed successfully.")

    return {
        "status": status,
        "environment": environment,
        "findings": findings,
        "policy_version": "2026.3.0-enterprise"
    }

def request_production_deployment(artifact_id: str, target_cluster: str, actor_id: str) -> Dict[str, Any]:
    """
    Simulates a multi-agent orchestration call to the downstream Deployer Agent.
    """
    return {
        "dispatch_status": "QUEUED",
        "deployment_id": f"dep-{hash(artifact_id) % 1000000:06d}",
        "artifact_id": artifact_id,
        "target_cluster": target_cluster,
        "authorized_by": actor_id,
        "message": f"Artifact {artifact_id} dispatched to {target_cluster} via secure agent channel."
    }

