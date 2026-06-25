from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Finding:
    title: str
    category: str
    severity: str
    evidence: str
    confidence: float


@dataclass(frozen=True)
class Recommendation:
    action: str
    owner: str
    priority: str


@dataclass(frozen=True)
class AnalysisReport:
    summary: str
    primary_category: str
    severity: str
    confidence: float
    findings: list[Finding] = field(default_factory=list)
    recommendations: list[Recommendation] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_markdown(self) -> str:
        lines = [
            f"# DevOps AI Triage: {self.primary_category}",
            "",
            f"**Severity:** {self.severity}",
            f"**Confidence:** {self.confidence:.2f}",
            "",
            "## Summary",
            "",
            self.summary,
            "",
            "## Findings",
            "",
        ]

        for finding in self.findings:
            lines.extend(
                [
                    f"- **{finding.title}**",
                    f"  - Category: {finding.category}",
                    f"  - Severity: {finding.severity}",
                    f"  - Evidence: `{finding.evidence}`",
                    f"  - Confidence: {finding.confidence:.2f}",
                ]
            )

        lines.extend(["", "## Recommended Actions", ""])
        for recommendation in self.recommendations:
            lines.append(
                f"- [{recommendation.priority}] {recommendation.action} "
                f"(owner: {recommendation.owner})"
            )

        return "\n".join(lines)

