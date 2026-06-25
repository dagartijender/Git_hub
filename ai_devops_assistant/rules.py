from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class TriageRule:
    name: str
    category: str
    severity: str
    pattern: re.Pattern[str]
    recommendation: str
    owner: str
    priority: str
    confidence: float


RULES: tuple[TriageRule, ...] = (
    TriageRule(
        name="Secret detected",
        category="Secret Scanning",
        severity="critical",
        pattern=re.compile(r"(secret|gitleaks).*(detected|leak|finding)", re.I),
        recommendation="Rotate the exposed credential, revoke the old token, and remove the secret from Git history.",
        owner="Security",
        priority="P0",
        confidence=0.94,
    ),
    TriageRule(
        name="SonarQube quality gate failed",
        category="Code Quality",
        severity="high",
        pattern=re.compile(r"(quality gate|sonarqube).*(failed|error)", re.I),
        recommendation="Review the SonarQube gate details, fix blocker issues, and rerun coverage/analysis.",
        owner="Service Team",
        priority="P1",
        confidence=0.88,
    ),
    TriageRule(
        name="Black Duck policy violation",
        category="Supply Chain Security",
        severity="high",
        pattern=re.compile(r"(black duck|blackduck|detect).*(policy|vulnerability|violation)", re.I),
        recommendation="Review vulnerable dependencies, upgrade or add an approved exception with expiry.",
        owner="Security",
        priority="P1",
        confidence=0.9,
    ),
    TriageRule(
        name="Veracode flaw found",
        category="Application Security",
        severity="high",
        pattern=re.compile(r"(veracode).*(flaw|policy|failed|very high|high)", re.I),
        recommendation="Open the Veracode findings, fix exploitable flaws, and resubmit the artifact.",
        owner="Application Security",
        priority="P1",
        confidence=0.89,
    ),
    TriageRule(
        name="Dockerfile or build context issue",
        category="Container Build",
        severity="medium",
        pattern=re.compile(r"(dockerfile|build context|COPY failed|no such file|failed to solve)", re.I),
        recommendation="Confirm the pipeline passes the correct Dockerfile path and build context for this microservice.",
        owner="DevOps",
        priority="P2",
        confidence=0.82,
    ),
    TriageRule(
        name="ACR authentication or authorization failure",
        category="Container Registry",
        severity="high",
        pattern=re.compile(r"(acr|registry|docker).*(unauthorized|denied|forbidden|authentication required)", re.I),
        recommendation="Validate the ACR service connection and confirm the pipeline identity has AcrPush.",
        owner="Platform",
        priority="P1",
        confidence=0.86,
    ),
    TriageRule(
        name="Terraform state lock",
        category="Terraform",
        severity="medium",
        pattern=re.compile(r"(terraform).*(state lock|acquiring the state lock|locked)", re.I),
        recommendation="Check for active Terraform runs before force-unlocking the state; never unlock a live run.",
        owner="Platform",
        priority="P2",
        confidence=0.84,
    ),
    TriageRule(
        name="Terraform plan or apply failed",
        category="Terraform",
        severity="high",
        pattern=re.compile(r"(terraform).*(error|failed|invalid|unauthorized|forbidden)", re.I),
        recommendation="Inspect the plan/apply output, validate provider authentication, and rerun plan before apply.",
        owner="Platform",
        priority="P1",
        confidence=0.8,
    ),
    TriageRule(
        name="Helm or Kubernetes rollout failed",
        category="Kubernetes Deployment",
        severity="high",
        pattern=re.compile(r"(helm|kubernetes|aks|pod|deployment).*(failed|timeout|crashloop|imagepullbackoff)", re.I),
        recommendation="Check ArgoCD sync status, pod events, image tag, and Helm values for the failed release.",
        owner="Platform",
        priority="P1",
        confidence=0.83,
    ),
)

