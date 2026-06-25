import unittest

from ai_devops_assistant import analyze_log


class AiDevOpsAssistantTests(unittest.TestCase):
    def test_detects_secret_scan_failure(self):
        report = analyze_log("Gitleaks detected a secret finding in appsettings.json")

        self.assertEqual(report.primary_category, "Secret Scanning")
        self.assertEqual(report.severity, "critical")
        self.assertTrue(report.recommendations)

    def test_detects_docker_context_failure(self):
        report = analyze_log("Docker build failed to solve: COPY failed no such file")

        self.assertEqual(report.primary_category, "Container Build")
        self.assertEqual(report.severity, "medium")

    def test_detects_multiple_security_signals(self):
        report = analyze_log(
            "Black Duck policy violation found. Veracode policy failed with high flaw."
        )

        categories = {finding.category for finding in report.findings}
        self.assertIn("Supply Chain Security", categories)
        self.assertIn("Application Security", categories)
        self.assertEqual(report.severity, "high")

    def test_unknown_log_gets_manual_review_recommendation(self):
        report = analyze_log("Agent job completed with an unexpected non-zero exit.")

        self.assertEqual(report.primary_category, "Unknown")
        self.assertEqual(report.severity, "unknown")
        self.assertEqual(report.recommendations[0].owner, "DevOps")


if __name__ == "__main__":
    unittest.main()

