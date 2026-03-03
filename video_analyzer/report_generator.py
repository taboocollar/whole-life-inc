"""
Report generator.

Takes the structured output from :class:`~video_analyzer.computer_analyzer.ComputerAnalyzer`
and produces a human-readable evaluation report that covers:

* Current specs of each computer found
* Whether each computer likely meets the user's stated needs
* Estimated cost to upgrade / future-proof each machine
* Overall recommendation
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import openai

from .computer_analyzer import AnalysisResult, ComputerSpec


_REPORT_SYSTEM_PROMPT = """\
You are a senior IT consultant and hardware evaluator. You will receive a JSON \
description of one or more computers that were identified in a user's video. \
Your job is to produce a clear, actionable evaluation report.

The report MUST contain:
1. A brief summary of each computer (model type, key specs, estimated age).
2. A "Meets Needs" assessment (YES / PARTIALLY / NO) for each computer, \
   given the user's stated workload.
3. An itemised upgrade plan for each computer that does *not* fully meet needs, \
   including estimated USD cost ranges for each upgrade.
4. A "Future-Proofing Score" (1-10) for each computer if upgraded as suggested.
5. An overall recommendation: keep, upgrade, or replace – with reasons.

Format the output as plain text with clear section headers. Be concise but \
specific. If specs are unknown, state that and note what would need to be \
verified in person.
"""


@dataclass
class ComputerReport:
    """Evaluation report for a single computer."""

    computer_id: str
    summary: str
    meets_needs: str  # "YES" | "PARTIALLY" | "NO" | "UNKNOWN"
    upgrade_plan: List[Dict[str, Any]] = field(default_factory=list)
    future_proof_score: Optional[int] = None
    recommendation: str = ""


@dataclass
class EvaluationReport:
    """Full evaluation report returned to the caller."""

    computer_reports: List[ComputerReport]
    overall_recommendation: str
    full_text: str


class ReportGenerator:
    """Generate hardware evaluation reports from :class:`AnalysisResult` data.

    Parameters
    ----------
    api_key:
        OpenAI API key.  Falls back to ``OPENAI_API_KEY`` environment variable.
    model:
        Chat model used for report generation (default ``gpt-4o``).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o",
    ) -> None:
        resolved_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        if not resolved_key:
            raise ValueError(
                "An OpenAI API key is required. Pass api_key= or set the "
                "OPENAI_API_KEY environment variable."
            )
        self._client = openai.OpenAI(api_key=resolved_key)
        self.model = model

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_report(
        self,
        analysis: AnalysisResult,
        user_needs: Optional[str] = None,
    ) -> EvaluationReport:
        """Produce an :class:`EvaluationReport` from *analysis*.

        Parameters
        ----------
        analysis:
            The output from :meth:`~video_analyzer.computer_analyzer.ComputerAnalyzer.analyze_frames`.
        user_needs:
            Free-text description of the user's intended workload / requirements.
        """
        if not analysis.computers:
            return EvaluationReport(
                computer_reports=[],
                overall_recommendation="No computers were detected in the video.",
                full_text="No computers were detected in the video.",
            )

        prompt = self._build_prompt(analysis.computers, user_needs)
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": _REPORT_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=4096,
            temperature=0,
        )

        full_text = response.choices[0].message.content or ""
        computer_reports = self._extract_computer_reports(
            analysis.computers, full_text
        )
        overall = self._extract_overall_recommendation(full_text)

        return EvaluationReport(
            computer_reports=computer_reports,
            overall_recommendation=overall,
            full_text=full_text,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_prompt(
        computers: List[ComputerSpec],
        user_needs: Optional[str],
    ) -> str:
        import json

        computers_json = json.dumps(
            [
                {
                    "id": c.id,
                    "type": c.type,
                    "visible_specs": c.visible_specs,
                    "confidence": c.confidence,
                    "notes": c.notes,
                }
                for c in computers
            ],
            indent=2,
        )
        needs_section = (
            f"\nUser's intended workload / requirements:\n{user_needs}\n"
            if user_needs
            else "\nNo specific workload was provided; give a general assessment.\n"
        )
        return (
            f"Here are the computers identified in the video:\n\n"
            f"{computers_json}\n"
            f"{needs_section}\n"
            "Please generate the evaluation report as described."
        )

    @staticmethod
    def _extract_computer_reports(
        computers: List[ComputerSpec],
        full_text: str,
    ) -> List[ComputerReport]:
        """Build minimal ComputerReport objects from the free-text response."""
        reports = []
        text_lower = full_text.lower()
        for computer in computers:
            meets = "UNKNOWN"
            if "yes" in text_lower:
                meets = "YES"
            if "partially" in text_lower:
                meets = "PARTIALLY"
            if " no " in text_lower or text_lower.startswith("no "):
                meets = "NO"

            reports.append(
                ComputerReport(
                    computer_id=computer.id,
                    summary=f"{computer.type} – confidence {computer.confidence:.0%}",
                    meets_needs=meets,
                    recommendation="See full report text for details.",
                )
            )
        return reports

    @staticmethod
    def _extract_overall_recommendation(full_text: str) -> str:
        """Return a short overall recommendation extracted from *full_text*."""
        lower = full_text.lower()
        for keyword in ("overall recommendation", "recommendation:", "in summary"):
            idx = lower.find(keyword)
            if idx != -1:
                snippet = full_text[idx:idx + 400].strip()
                lines = [ln.strip() for ln in snippet.splitlines() if ln.strip()]
                if len(lines) > 1:
                    # Return the line *after* the header that contains the keyword
                    return lines[1]
                return lines[0] if lines else snippet
        # Fallback: return the last non-empty line
        lines = [ln.strip() for ln in full_text.splitlines() if ln.strip()]
        return lines[-1] if lines else full_text[:200]
