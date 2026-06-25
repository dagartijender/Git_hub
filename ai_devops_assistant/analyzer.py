from __future__ import annotations

from collections import Counter

from ai_devops_assistant.models import AnalysisReport, Finding, Recommendation
from ai_devops_assistant.rules import RULES


SEVERITY_ORDER = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
    "unknown": 0,
}


def analyze_log(log_text: str) -> AnalysisReport:
    """Analyze a DevOps log and return prioritized findings.

    The first version is intentionally deterministic: it behaves like an AI
    triage engine by combining signal extraction, category scoring, confidence,
    and recommended action generation without requiring a live LLM key.
    """

    findings: list[Finding] = []
    recommendations: list[Recommendation] = []

    for rule in RULES:
        match = rule.pattern.search(log_text)
        if not match:
            continue

        evidence = _compact_evidence(match.group(0))
        findings.append(
            Finding(
                title=rule.name,
                category=rule.category,
                severity=rule.severity,
                evidence=evidence,
                confidence=rule.confidence,
            )
        )
        recommendations.append(
            Recommendation(
                action=rule.recommendation,
                owner=rule.owner,
                priority=rule.priority,
            )
        )

    if not findings:
        return AnalysisReport(
            summary="No known DevOps failure pattern was detected. Escalate to manual log review and compare this run with the last successful build.",
            primary_category="Unknown",
            severity="unknown",
            confidence=0.2,
            findings=[
                Finding(
                    title="No known pattern matched",
                    category="Unknown",
                    severity="unknown",
                    evidence=_compact_evidence(log_text[:160]),
                    confidence=0.2,
                )
            ],
            recommendations=[
                Recommendation(
                    action="Capture the full logs, timeline records, changed files, and service connection used by the run.",
                    owner="DevOps",
                    priority="P3",
                )
            ],
        )

    primary_category = _primary_category(findings)
    severity = max(findings, key=lambda item: SEVERITY_ORDER[item.severity]).severity
    confidence = round(sum(finding.confidence for finding in findings) / len(findings), 2)

    return AnalysisReport(
        summary=(
            f"Detected {len(findings)} likely failure signal(s). "
            f"Primary area is {primary_category}; highest severity is {severity}."
        ),
        primary_category=primary_category,
        severity=severity,
        confidence=confidence,
        findings=findings,
        recommendations=_dedupe_recommendations(recommendations),
    )


def _primary_category(findings: list[Finding]) -> str:
    counts = Counter(finding.category for finding in findings)
    return counts.most_common(1)[0][0]


def _compact_evidence(text: str) -> str:
    return " ".join(text.split())[:180]


def _dedupe_recommendations(
    recommendations: list[Recommendation],
) -> list[Recommendation]:
    unique: dict[str, Recommendation] = {}
    for recommendation in recommendations:
        unique.setdefault(recommendation.action, recommendation)
    return list(unique.values())

