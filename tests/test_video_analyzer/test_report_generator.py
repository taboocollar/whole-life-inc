"""
Unit tests for ReportGenerator.

All OpenAI calls are mocked – no real API requests are made.
"""

from __future__ import annotations

import json
import unittest
from unittest.mock import MagicMock, patch

from video_analyzer.computer_analyzer import AnalysisResult, ComputerSpec
from video_analyzer.report_generator import (
    EvaluationReport,
    ReportGenerator,
    ComputerReport,
)


def _make_analysis(computers=None) -> AnalysisResult:
    if computers is None:
        computers = [
            ComputerSpec(
                id="computer_1",
                type="desktop",
                visible_specs={"cpu": "Intel i5", "ram_gb": 8},
                confidence=0.85,
                notes="Tower PC",
            )
        ]
    return AnalysisResult(
        computers=computers,
        raw_response="[]",
        frame_count=5,
    )


def _make_generator(api_key: str = "sk-test") -> ReportGenerator:
    with patch("video_analyzer.report_generator.openai.OpenAI"):
        return ReportGenerator(api_key=api_key)


def _mock_response(content: str) -> MagicMock:
    choice = MagicMock()
    choice.message.content = content
    resp = MagicMock()
    resp.choices = [choice]
    return resp


class TestReportGeneratorInit(unittest.TestCase):
    """Test constructor behaviour."""

    def test_requires_api_key(self):
        import os
        os.environ.pop("OPENAI_API_KEY", None)
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ValueError):
                ReportGenerator(api_key="")

    def test_accepts_api_key_argument(self):
        with patch("video_analyzer.report_generator.openai.OpenAI"):
            gen = ReportGenerator(api_key="sk-test")
            self.assertEqual(gen.model, "gpt-4o")


class TestGenerateReportNoComputers(unittest.TestCase):
    """When no computers are detected the report should say so."""

    def test_empty_analysis(self):
        gen = _make_generator()
        empty = AnalysisResult(computers=[], raw_response="", frame_count=0)
        report = gen.generate_report(empty)
        self.assertIsInstance(report, EvaluationReport)
        self.assertEqual(report.computer_reports, [])
        self.assertIn("No computers", report.overall_recommendation)


class TestGenerateReportMocked(unittest.TestCase):
    """Test generate_report with mocked OpenAI responses."""

    _SAMPLE_REPORT = """
## Computer Analysis Report

### Computer 1: desktop (Intel i5 / 8 GB RAM)

**Meets Needs**: PARTIALLY

The machine is adequate for light tasks but will struggle with 4K editing.

**Upgrade Plan**
- RAM: upgrade from 8 GB → 32 GB (~$60–$90)
- Storage: add NVMe SSD (~$80–$120)
- GPU: add dedicated GPU (~$200–$400)

**Future-Proofing Score**: 7/10

### Overall Recommendation
Upgrade the existing desktop before replacing it. Estimated total cost: $340–$610.
"""

    def test_returns_evaluation_report(self):
        gen = _make_generator()
        gen._client.chat.completions.create.return_value = _mock_response(
            self._SAMPLE_REPORT
        )
        report = gen.generate_report(_make_analysis())
        self.assertIsInstance(report, EvaluationReport)
        self.assertIsInstance(report.full_text, str)
        self.assertGreater(len(report.full_text), 0)

    def test_computer_reports_created(self):
        gen = _make_generator()
        gen._client.chat.completions.create.return_value = _mock_response(
            self._SAMPLE_REPORT
        )
        report = gen.generate_report(_make_analysis())
        self.assertEqual(len(report.computer_reports), 1)
        cr = report.computer_reports[0]
        self.assertIsInstance(cr, ComputerReport)
        self.assertEqual(cr.computer_id, "computer_1")

    def test_overall_recommendation_extracted(self):
        gen = _make_generator()
        gen._client.chat.completions.create.return_value = _mock_response(
            self._SAMPLE_REPORT
        )
        report = gen.generate_report(_make_analysis())
        self.assertIn("Upgrade", report.overall_recommendation)

    def test_user_needs_included_in_prompt(self):
        gen = _make_generator()
        gen._client.chat.completions.create.return_value = _mock_response("done")

        gen.generate_report(_make_analysis(), user_needs="machine learning training")

        call_kwargs = gen._client.chat.completions.create.call_args.kwargs
        messages = call_kwargs.get("messages", [])
        user_msg = next((m for m in messages if m["role"] == "user"), None)
        self.assertIsNotNone(user_msg)
        self.assertIn("machine learning training", user_msg["content"])

    def test_multiple_computers_all_reported(self):
        gen = _make_generator()
        gen._client.chat.completions.create.return_value = _mock_response(
            "No issues found. Overall recommendation: all good."
        )
        computers = [
            ComputerSpec("c1", "desktop", {}, 0.9, ""),
            ComputerSpec("c2", "laptop",  {}, 0.7, ""),
        ]
        analysis = AnalysisResult(computers=computers, raw_response="", frame_count=10)
        report = gen.generate_report(analysis)
        self.assertEqual(len(report.computer_reports), 2)


class TestBuildPrompt(unittest.TestCase):
    """Unit tests for the _build_prompt static method."""

    def test_includes_computer_data(self):
        computers = [ComputerSpec("c1", "laptop", {"cpu": "M2"}, 0.8, "")]
        prompt = ReportGenerator._build_prompt(computers, user_needs=None)
        self.assertIn("c1", prompt)
        self.assertIn("laptop", prompt)
        self.assertIn("M2", prompt)

    def test_includes_user_needs(self):
        computers = [ComputerSpec("c1", "desktop", {}, 0.9, "")]
        prompt = ReportGenerator._build_prompt(computers, user_needs="video editing")
        self.assertIn("video editing", prompt)

    def test_no_user_needs_fallback(self):
        computers = [ComputerSpec("c1", "desktop", {}, 0.9, "")]
        prompt = ReportGenerator._build_prompt(computers, user_needs=None)
        self.assertIn("No specific workload", prompt)


class TestExtractOverallRecommendation(unittest.TestCase):
    """Unit tests for _extract_overall_recommendation."""

    def test_finds_overall_recommendation_header(self):
        text = "Some stuff.\n\n### Overall Recommendation\nReplace computer_1."
        result = ReportGenerator._extract_overall_recommendation(text)
        self.assertIn("Replace computer_1", result)

    def test_finds_recommendation_colon(self):
        text = "Analysis done.\nRecommendation: Upgrade the RAM."
        result = ReportGenerator._extract_overall_recommendation(text)
        self.assertIn("Recommendation", result)

    def test_fallback_last_line(self):
        text = "Line one.\nLine two.\nFinal line."
        result = ReportGenerator._extract_overall_recommendation(text)
        self.assertEqual(result, "Final line.")


if __name__ == "__main__":
    unittest.main()
