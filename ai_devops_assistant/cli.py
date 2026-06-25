from __future__ import annotations

import argparse
import json
from pathlib import Path

from ai_devops_assistant import analyze_log


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze DevOps pipeline logs and recommend next actions."
    )
    parser.add_argument("log_file", type=Path, help="Path to a pipeline log file.")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    args = parser.parse_args()

    report = analyze_log(args.log_file.read_text(encoding="utf-8"))
    if args.format == "json":
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(report.to_markdown())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

