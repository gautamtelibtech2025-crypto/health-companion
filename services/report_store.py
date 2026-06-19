"""
HealthAI Pro — Report Store Service

JSON-based persistence for health assessment reports.
Each report is saved as a JSON file alongside its generated PDF.
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from config.settings import REPORTS_DIR


class ReportStore:
    """Manages reading, writing, listing, and deleting assessment reports."""

    def __init__(self, reports_dir: Path | None = None) -> None:
        self._dir = reports_dir or REPORTS_DIR
        self._dir.mkdir(parents=True, exist_ok=True)

    # ── Write ─────────────────────────────────────────────────────

    def save_report(
        self,
        patient_data: dict[str, Any],
        analysis: dict[str, Any],
        pdf_path: str | None = None,
    ) -> str:
        """Save a report and return its unique ID.

        Args:
            patient_data: Patient information dict.
            analysis: Gemini analysis result dict.
            pdf_path: Optional path to the associated PDF file.

        Returns:
            The unique report ID string.
        """
        report_id = uuid.uuid4().hex[:12]
        now = datetime.now()

        report = {
            "id": report_id,
            "created_at": now.isoformat(),
            "created_at_display": now.strftime("%B %d, %Y at %I:%M %p"),
            "patient_data": patient_data,
            "analysis": analysis,
            "pdf_path": pdf_path,
        }

        filepath = self._dir / f"{report_id}.json"
        filepath.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        return report_id

    # ── Read ──────────────────────────────────────────────────────

    def get_report(self, report_id: str) -> dict[str, Any] | None:
        """Load a single report by ID.

        Returns:
            Report dict or None if not found.
        """
        filepath = self._dir / f"{report_id}.json"
        if not filepath.exists():
            return None
        return json.loads(filepath.read_text(encoding="utf-8"))

    def list_reports(self) -> list[dict[str, Any]]:
        """List all saved reports, sorted newest first.

        Returns:
            List of report dicts (full data).
        """
        reports: list[dict[str, Any]] = []
        for f in sorted(self._dir.glob("*.json"), reverse=True):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                reports.append(data)
            except (json.JSONDecodeError, KeyError):
                continue
        return reports

    def report_count(self) -> int:
        """Return the number of saved reports."""
        return len(list(self._dir.glob("*.json")))

    # ── Delete ────────────────────────────────────────────────────

    def delete_report(self, report_id: str) -> bool:
        """Delete a report and its associated PDF.

        Returns:
            True if the report was found and deleted.
        """
        json_path = self._dir / f"{report_id}.json"
        if not json_path.exists():
            return False

        # Try to delete associated PDF
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
            pdf_path = data.get("pdf_path")
            if pdf_path and os.path.exists(pdf_path):
                os.remove(pdf_path)
        except Exception:
            pass  # PDF cleanup is best-effort

        json_path.unlink()
        return True

    def delete_all_reports(self) -> int:
        """Delete all reports and their PDFs.

        Returns:
            Number of reports deleted.
        """
        count = 0
        for f in self._dir.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                pdf_path = data.get("pdf_path")
                if pdf_path and os.path.exists(pdf_path):
                    os.remove(pdf_path)
            except Exception:
                pass
            f.unlink()
            count += 1
        return count
