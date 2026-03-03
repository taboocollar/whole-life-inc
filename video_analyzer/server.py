"""
FastAPI server that exposes the video analyzer as HTTP endpoints.

This server can be registered as a **ChatGPT custom action** by pointing
ChatGPT to the ``/openapi.json`` endpoint that FastAPI auto-generates, or
by uploading ``chatgpt_tool_schema.json`` directly in the GPT Builder.

Usage
-----
Run locally::

    uvicorn video_analyzer.server:app --reload --port 8000

Environment variables
---------------------
OPENAI_API_KEY
    Required – your OpenAI API key.
MAX_VIDEO_DURATION
    Optional – override the 60-second limit (seconds, default 60).
"""

from __future__ import annotations

import os
import tempfile
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .computer_analyzer import ComputerAnalyzer
from .frame_extractor import FrameExtractor
from .report_generator import ReportGenerator


app = FastAPI(
    title="Video Computer Analyzer",
    description=(
        "Upload a short video (≤60 s) containing computers. "
        "Receive a structured analysis of the hardware and an evaluation "
        "report covering whether the machines meet your needs and estimated "
        "upgrade costs."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------


class VisibleSpecs(BaseModel):
    cpu: Optional[str] = None
    ram_gb: Optional[int] = None
    storage: Optional[str] = None
    gpu: Optional[str] = None
    os: Optional[str] = None
    monitor_size_inches: Optional[float] = None
    ports_visible: Optional[list] = None
    age_estimate_years: Optional[int] = None


class ComputerDetail(BaseModel):
    id: str
    type: str
    visible_specs: dict = Field(default_factory=dict)
    confidence: float
    notes: str


class AnalyzeVideoResponse(BaseModel):
    frame_count: int
    computers_found: int
    computers: list[ComputerDetail]
    report: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/health", summary="Health check")
def health() -> dict:
    """Return a simple health status."""
    return {"status": "ok"}


@app.post(
    "/analyze-video",
    response_model=AnalyzeVideoResponse,
    summary="Analyze a video for computer hardware",
)
async def analyze_video(
    file: UploadFile = File(
        ...,
        description="Video file (mp4, mov, avi, mkv – maximum 60 seconds).",
    ),
    user_needs: Optional[str] = Form(
        default=None,
        description=(
            "Describe your intended workload / requirements so the report can "
            "assess whether the computers meet your needs (e.g. 'video editing "
            "in 4K, running multiple VMs, machine-learning training')."
        ),
    ),
) -> AnalyzeVideoResponse:
    """Upload a video and receive a hardware analysis + evaluation report.

    - Extracts one frame per second (up to 60 frames).
    - Identifies every distinct computer visible in the frames.
    - Returns specs and a full evaluation report.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY environment variable is not set on the server.",
        )

    max_duration = float(os.environ.get("MAX_VIDEO_DURATION", "60"))

    # Save the upload to a temp file so OpenCV can read it.
    suffix = os.path.splitext(file.filename or "video.mp4")[1] or ".mp4"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp_path = tmp.name
        content = await file.read()
        tmp.write(content)

    try:
        extractor = FrameExtractor(max_duration=max_duration)
        try:
            frames = extractor.extract_frames(tmp_path)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))

        analyzer = ComputerAnalyzer(api_key=api_key)
        analysis = analyzer.analyze_frames(frames, user_needs=user_needs)

        generator = ReportGenerator(api_key=api_key)
        report = generator.generate_report(analysis, user_needs=user_needs)

        computers = [
            ComputerDetail(
                id=c.id,
                type=c.type,
                visible_specs=c.visible_specs,
                confidence=c.confidence,
                notes=c.notes,
            )
            for c in analysis.computers
        ]

        return AnalyzeVideoResponse(
            frame_count=analysis.frame_count,
            computers_found=len(computers),
            computers=computers,
            report=report.full_text,
        )
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
