"""
Frame extractor for short videos (≤60 seconds).

Reads a local video file with OpenCV and returns evenly-spaced frames as
base64-encoded JPEG strings suitable for the OpenAI Vision API.
"""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass, field
from typing import List

import cv2


MAX_DURATION_SECONDS = 60
DEFAULT_FRAMES_PER_SECOND = 1  # one representative frame per second


@dataclass
class VideoFrame:
    """A single extracted video frame."""

    index: int
    timestamp_seconds: float
    base64_jpeg: str = field(repr=False)


class FrameExtractor:
    """Extract key frames from a video file.

    Parameters
    ----------
    max_duration:
        Hard cap on video length in seconds (default 60).
    frames_per_second:
        How many frames to sample per second of video (default 1).
    """

    def __init__(
        self,
        max_duration: float = MAX_DURATION_SECONDS,
        frames_per_second: float = DEFAULT_FRAMES_PER_SECOND,
    ) -> None:
        if max_duration <= 0:
            raise ValueError("max_duration must be positive")
        if frames_per_second <= 0:
            raise ValueError("frames_per_second must be positive")
        self.max_duration = max_duration
        self.frames_per_second = frames_per_second

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract_frames(self, video_path: str) -> List[VideoFrame]:
        """Return a list of :class:`VideoFrame` objects from *video_path*.

        Parameters
        ----------
        video_path:
            Absolute or relative path to the video file.

        Raises
        ------
        FileNotFoundError
            If *video_path* does not exist.
        ValueError
            If the file cannot be opened as a video or if its duration
            exceeds ``max_duration``.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")

        try:
            fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps

            if duration > self.max_duration:
                raise ValueError(
                    f"Video duration {duration:.1f}s exceeds the "
                    f"{self.max_duration}s limit. Please trim the video."
                )

            return self._sample_frames(cap, fps, duration)
        finally:
            cap.release()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _sample_frames(
        self,
        cap: cv2.VideoCapture,
        fps: float,
        duration: float,
    ) -> List[VideoFrame]:
        """Sample frames at the configured rate and encode them."""
        interval = 1.0 / self.frames_per_second
        timestamps = []
        t = 0.0
        while t <= duration:
            timestamps.append(t)
            t += interval

        frames: List[VideoFrame] = []
        for idx, ts in enumerate(timestamps):
            frame_number = int(ts * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            success, frame = cap.read()
            if not success:
                continue
            frames.append(
                VideoFrame(
                    index=idx,
                    timestamp_seconds=round(ts, 2),
                    base64_jpeg=self._encode_frame(frame),
                )
            )
        return frames

    @staticmethod
    def _encode_frame(frame) -> str:
        """Encode an OpenCV BGR frame as a base64 JPEG string."""
        success, buffer = cv2.imencode(".jpg", frame)
        if not success:
            raise ValueError("Failed to encode frame as JPEG")
        return base64.b64encode(buffer.tobytes()).decode("utf-8")
