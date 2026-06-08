"""Generate an EU AI Act Article 12 technical file for the last 30 days.

Run:
    pip install aira-sdk
    export AIRA_API_KEY="aira_live_..."
    python generate_article12_report.py

The script asks Aira to generate a PDF report covering all action receipts
in the period, downloads it, then verifies the signature server-side.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta

from aira import Aira


def main() -> None:
    api_key = os.environ["AIRA_API_KEY"]
    aira = Aira(api_key=api_key, base_url=os.environ.get("AIRA_BASE_URL", "https://api.airaproof.com"))

    end = datetime.now(UTC)
    start = end - timedelta(days=30)

    print(f"Requesting Article 12 report for {start.date()} -- {end.date()}")
    report = aira.create_compliance_report(
        framework="eu_ai_act_art12",
        period_start=start.isoformat(),
        period_end=end.isoformat(),
    )
    print(f"  status: {report.status}")
    print(f"  receipts covered: {report.receipt_count}")
    print(f"  pdf size: {report.pdf_size_bytes} bytes")
    print(f"  content_hash: {report.content_hash}")
    print(f"  signature: {report.signature}")

    out_path = f"aira-art12-{report.id}.pdf"
    with open(out_path, "wb") as fh:
        fh.write(aira.download_compliance_report(report.id))
    print(f"  saved to: {out_path}")

    verification = aira.verify_compliance_report(report.id)
    print(f"  signature valid: {verification.valid}")
    print(f"  checks: {verification.checks}")


if __name__ == "__main__":
    main()
