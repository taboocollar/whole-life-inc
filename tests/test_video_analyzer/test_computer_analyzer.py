"""
Unit tests for ComputerAnalyzer.

These tests mock the OpenAI client so no real API calls are made.
"""

from __future__ import annotations

import json
import unittest
from unittest.mock import MagicMock, patch

from video_analyzer.computer_analyzer import (
    ComputerAnalyzer,
    ComputerSpec,
    AnalysisResult,
)
from video_analyzer.frame_extractor import VideoFrame


def _make_frame(index: int = 0) -> VideoFrame:
    return VideoFrame(index=index, timestamp_seconds=float(index), base64_jpeg="abc123")


def _make_analyzer(api_key: str = "sk-test") -> ComputerAnalyzer:
    with patch("video_analyzer.computer_analyzer.openai.OpenAI"):
        return ComputerAnalyzer(api_key=api_key)


class TestComputerAnalyzerInit(unittest.TestCase):
    """Test constructor behaviour."""

    def test_requires_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            # Remove OPENAI_API_KEY if present
            import os
            os.environ.pop("OPENAI_API_KEY", None)
            with self.assertRaises(ValueError):
                ComputerAnalyzer(api_key="")

    def test_accepts_api_key_argument(self):
        with patch("video_analyzer.computer_analyzer.openai.OpenAI"):
            analyzer = ComputerAnalyzer(api_key="sk-test")
            self.assertEqual(analyzer.model, "gpt-4o")

    def test_accepts_env_variable(self):
        with patch.dict("os.environ", {"OPENAI_API_KEY": "sk-env-key"}):
            with patch("video_analyzer.computer_analyzer.openai.OpenAI"):
                analyzer = ComputerAnalyzer()
                self.assertIsNotNone(analyzer)


class TestAnalyzeFramesEmpty(unittest.TestCase):
    """analyze_frames should return an empty result for no frames."""

    def test_empty_frames(self):
        analyzer = _make_analyzer()
        result = analyzer.analyze_frames([])
        self.assertIsInstance(result, AnalysisResult)
        self.assertEqual(result.computers, [])
        self.assertEqual(result.frame_count, 0)


class TestAnalyzeFramesMocked(unittest.TestCase):
    """Test analyze_frames with mocked OpenAI responses."""

    def _mock_response(self, content: str) -> MagicMock:
        choice = MagicMock()
        choice.message.content = content
        response = MagicMock()
        response.choices = [choice]
        return response

    def test_parses_valid_json_response(self):
        analyzer = _make_analyzer()
        computers_json = json.dumps([
            {
                "id": "computer_1",
                "type": "desktop",
                "visible_specs": {"cpu": "Intel i7", "ram_gb": 16},
                "confidence": 0.9,
                "notes": "Visible i7 sticker",
            }
        ])
        analyzer._client.chat.completions.create.return_value = (
            self._mock_response(computers_json)
        )

        frames = [_make_frame(0), _make_frame(1)]
        result = analyzer.analyze_frames(frames)

        self.assertEqual(result.frame_count, 2)
        self.assertEqual(len(result.computers), 1)
        self.assertEqual(result.computers[0].id, "computer_1")
        self.assertEqual(result.computers[0].type, "desktop")
        self.assertAlmostEqual(result.computers[0].confidence, 0.9)

    def test_handles_malformed_json_gracefully(self):
        analyzer = _make_analyzer()
        analyzer._client.chat.completions.create.return_value = (
            self._mock_response("This is not JSON at all.")
        )

        result = analyzer.analyze_frames([_make_frame()])
        self.assertEqual(result.computers, [])

    def test_extracts_json_from_prose(self):
        """JSON embedded in prose should still be parsed."""
        analyzer = _make_analyzer()
        prose = (
            "Here is the result:\n"
            '[{"id":"c1","type":"laptop","visible_specs":{},"confidence":0.5,"notes":""}]'
            "\nEnd of response."
        )
        analyzer._client.chat.completions.create.return_value = (
            self._mock_response(prose)
        )

        result = analyzer.analyze_frames([_make_frame()])
        self.assertEqual(len(result.computers), 1)
        self.assertEqual(result.computers[0].id, "c1")

    def test_multiple_computers(self):
        analyzer = _make_analyzer()
        computers_json = json.dumps([
            {"id": "c1", "type": "desktop", "visible_specs": {}, "confidence": 0.8, "notes": ""},
            {"id": "c2", "type": "laptop",  "visible_specs": {}, "confidence": 0.6, "notes": ""},
        ])
        analyzer._client.chat.completions.create.return_value = (
            self._mock_response(computers_json)
        )

        result = analyzer.analyze_frames([_make_frame(0), _make_frame(1)])
        self.assertEqual(len(result.computers), 2)

    def test_user_needs_passed_in_message(self):
        analyzer = _make_analyzer()
        analyzer._client.chat.completions.create.return_value = (
            self._mock_response("[]")
        )

        frames = [_make_frame()]
        analyzer.analyze_frames(frames, user_needs="4K video editing")

        call_args = analyzer._client.chat.completions.create.call_args
        messages = call_args.kwargs.get("messages") or call_args.args[0] if call_args.args else []
        # Find user message content
        user_msg = next(
            (m for m in (call_args.kwargs.get("messages", []) or []) if m["role"] == "user"),
            None,
        )
        if user_msg:
            content_text = " ".join(
                block.get("text", "") for block in user_msg["content"]
                if isinstance(block, dict) and block.get("type") == "text"
            )
            self.assertIn("4K video editing", content_text)


class TestParseResponse(unittest.TestCase):
    """Unit tests for the _parse_response static method."""

    def test_valid_json(self):
        raw = json.dumps([
            {"id": "c1", "type": "laptop", "visible_specs": {}, "confidence": 0.7, "notes": "test"}
        ])
        specs = ComputerAnalyzer._parse_response(raw)
        self.assertEqual(len(specs), 1)
        self.assertIsInstance(specs[0], ComputerSpec)

    def test_empty_array(self):
        specs = ComputerAnalyzer._parse_response("[]")
        self.assertEqual(specs, [])

    def test_non_array_json(self):
        specs = ComputerAnalyzer._parse_response('{"key": "value"}')
        self.assertEqual(specs, [])

    def test_invalid_json(self):
        specs = ComputerAnalyzer._parse_response("not json")
        self.assertEqual(specs, [])

    def test_defaults_for_missing_fields(self):
        raw = json.dumps([{}])
        specs = ComputerAnalyzer._parse_response(raw)
        self.assertEqual(len(specs), 1)
        self.assertEqual(specs[0].id, "unknown")
        self.assertEqual(specs[0].type, "unknown")
        self.assertEqual(specs[0].confidence, 0.0)


if __name__ == "__main__":
    unittest.main()
