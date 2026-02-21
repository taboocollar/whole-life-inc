"""
Computer hardware analyzer.

Sends video frames to the OpenAI Vision API (GPT-4o) and extracts structured
information about every computer visible in the frames.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import openai

from .frame_extractor import VideoFrame


# System prompt that instructs the model how to respond.
_SYSTEM_PROMPT = """\
You are an expert computer hardware analyst. You will be shown one or more \
frames from a short video that contains one or more desktop or laptop computers. \
Your task is to identify every distinct computer visible across all frames and \
return a structured JSON array.

For each computer return an object with these keys:
  - "id": a short label like "computer_1", "computer_2", etc.
  - "type": "desktop" | "laptop" | "workstation" | "server" | "unknown"
  - "visible_specs": object with any specs you can read or infer from the \
screen, labels, or physical form factor. Include keys such as:
      "cpu", "ram_gb", "storage", "gpu", "os", "monitor_size_inches", \
"ports_visible", "age_estimate_years"
    – use null for anything you cannot determine.
  - "confidence": a float 0-1 indicating overall confidence in your assessment.
  - "notes": any additional observations (e.g. visible damage, non-standard parts).

Respond with ONLY valid JSON – no markdown, no prose.
Example output:
[
  {
    "id": "computer_1",
    "type": "desktop",
    "visible_specs": {
      "cpu": "Intel Core i5 (sticker visible)",
      "ram_gb": null,
      "storage": null,
      "gpu": null,
      "os": "Windows 10",
      "monitor_size_inches": 24,
      "ports_visible": ["USB-A", "HDMI"],
      "age_estimate_years": 5
    },
    "confidence": 0.72,
    "notes": "Tower has a visible Intel Inside sticker."
  }
]
"""


@dataclass
class ComputerSpec:
    """Structured hardware description for one computer found in the video."""

    id: str
    type: str
    visible_specs: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    notes: str = ""


@dataclass
class AnalysisResult:
    """Output of :meth:`ComputerAnalyzer.analyze_frames`."""

    computers: List[ComputerSpec]
    raw_response: str
    frame_count: int


class ComputerAnalyzer:
    """Use OpenAI Vision to identify computers and their specs in video frames.

    Parameters
    ----------
    api_key:
        OpenAI API key.  Falls back to the ``OPENAI_API_KEY`` environment
        variable when not provided.
    model:
        The vision-capable chat model to use.
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

    def analyze_frames(
        self,
        frames: List[VideoFrame],
        user_needs: Optional[str] = None,
    ) -> AnalysisResult:
        """Identify computers in *frames* and return structured specs.

        Parameters
        ----------
        frames:
            List of :class:`~video_analyzer.frame_extractor.VideoFrame` objects.
        user_needs:
            Optional free-text description of what the user intends to use
            the computers for.  Appended to the user message so the model
            can tailor confidence / notes.
        """
        if not frames:
            return AnalysisResult(computers=[], raw_response="", frame_count=0)

        messages = self._build_messages(frames, user_needs)
        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=2048,
            temperature=0,
        )

        raw = response.choices[0].message.content or ""
        computers = self._parse_response(raw)
        return AnalysisResult(
            computers=computers,
            raw_response=raw,
            frame_count=len(frames),
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _build_messages(
        self,
        frames: List[VideoFrame],
        user_needs: Optional[str],
    ) -> List[Dict[str, Any]]:
        """Construct the messages list for the chat completion call."""
        content: List[Dict[str, Any]] = []

        intro = (
            f"I have extracted {len(frames)} frame(s) from a short video "
            "showing one or more computers. Please identify every distinct "
            "computer and return the JSON array described in the system prompt."
        )
        if user_needs:
            intro += f"\n\nUser's intended workload: {user_needs}"
        content.append({"type": "text", "text": intro})

        for frame in frames:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{frame.base64_jpeg}",
                        "detail": "auto",
                    },
                }
            )

        return [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ]

    @staticmethod
    def _parse_response(raw: str) -> List[ComputerSpec]:
        """Parse the model's JSON response into :class:`ComputerSpec` objects."""
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # Try to extract JSON array from a response that may contain prose.
            start = raw.find("[")
            end = raw.rfind("]") + 1
            if start == -1 or end == 0:
                return []
            try:
                data = json.loads(raw[start:end])
            except json.JSONDecodeError:
                return []

        if not isinstance(data, list):
            return []

        specs = []
        for item in data:
            if not isinstance(item, dict):
                continue
            specs.append(
                ComputerSpec(
                    id=item.get("id", "unknown"),
                    type=item.get("type", "unknown"),
                    visible_specs=item.get("visible_specs", {}),
                    confidence=float(item.get("confidence", 0.0)),
                    notes=item.get("notes", ""),
                )
            )
        return specs
