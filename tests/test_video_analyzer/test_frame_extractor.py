"""
Unit tests for FrameExtractor.

These tests do NOT require a real video file or OpenCV GPU support.
They validate:
  - Constructor validation
  - Correct ValueError for videos longer than max_duration
  - Correct FileNotFoundError for missing files
  - Frame encoding helper
  - _sample_frames logic via a mock VideoCapture
"""

from __future__ import annotations

import base64
import os
import struct
import unittest
from unittest.mock import MagicMock, patch, call

import numpy as np

from video_analyzer.frame_extractor import FrameExtractor, VideoFrame, MAX_DURATION_SECONDS


def _make_bgr_frame(width: int = 4, height: int = 4) -> np.ndarray:
    """Return a tiny solid-colour BGR frame."""
    return np.zeros((height, width, 3), dtype=np.uint8)


class TestFrameExtractorInit(unittest.TestCase):
    """Test constructor validation."""

    def test_default_values(self):
        fe = FrameExtractor()
        self.assertEqual(fe.max_duration, MAX_DURATION_SECONDS)
        self.assertEqual(fe.frames_per_second, 1)

    def test_custom_values(self):
        fe = FrameExtractor(max_duration=30, frames_per_second=2)
        self.assertEqual(fe.max_duration, 30)
        self.assertEqual(fe.frames_per_second, 2)

    def test_invalid_max_duration(self):
        with self.assertRaises(ValueError):
            FrameExtractor(max_duration=0)

    def test_invalid_frames_per_second(self):
        with self.assertRaises(ValueError):
            FrameExtractor(frames_per_second=-1)


class TestExtractFramesMissingFile(unittest.TestCase):
    """Test that a missing file raises FileNotFoundError."""

    def test_missing_file(self):
        fe = FrameExtractor()
        with self.assertRaises(FileNotFoundError):
            fe.extract_frames("/tmp/does_not_exist_xyz.mp4")


class TestExtractFramesMockedCapture(unittest.TestCase):
    """Test extract_frames using a mocked cv2.VideoCapture."""

    def _make_cap_mock(self, fps: float, frame_count: int) -> MagicMock:
        cap = MagicMock()
        cap.isOpened.return_value = True
        cap.get.side_effect = lambda prop: {
            0: fps,          # CAP_PROP_POS_MSEC  (not used directly)
            5: fps,          # CAP_PROP_FPS
            7: frame_count,  # CAP_PROP_FRAME_COUNT
        }.get(prop, fps)
        # read() returns a simple frame each call
        frame = _make_bgr_frame()
        cap.read.return_value = (True, frame)
        return cap

    @patch("video_analyzer.frame_extractor.cv2.VideoCapture")
    @patch("video_analyzer.frame_extractor.os.path.exists", return_value=True)
    def test_extracts_correct_number_of_frames(self, mock_exists, mock_cap_class):
        fps = 10.0
        duration = 5.0  # 5 seconds
        frame_count = int(fps * duration)
        mock_cap_class.return_value = self._make_cap_mock(fps, frame_count)

        fe = FrameExtractor(max_duration=60, frames_per_second=1)
        frames = fe.extract_frames("/fake/video.mp4")

        # 1 fps × 5 s → should produce frames at t=0,1,2,3,4,5 = 6 frames
        self.assertGreaterEqual(len(frames), 5)
        self.assertIsInstance(frames[0], VideoFrame)

    @patch("video_analyzer.frame_extractor.cv2.VideoCapture")
    @patch("video_analyzer.frame_extractor.os.path.exists", return_value=True)
    def test_raises_on_long_video(self, mock_exists, mock_cap_class):
        fps = 30.0
        duration = 90.0  # exceeds 60-second limit
        frame_count = int(fps * duration)
        mock_cap_class.return_value = self._make_cap_mock(fps, frame_count)

        fe = FrameExtractor(max_duration=60)
        with self.assertRaises(ValueError) as ctx:
            fe.extract_frames("/fake/long_video.mp4")
        self.assertIn("90", str(ctx.exception))

    @patch("video_analyzer.frame_extractor.cv2.VideoCapture")
    @patch("video_analyzer.frame_extractor.os.path.exists", return_value=True)
    def test_raises_when_cap_not_opened(self, mock_exists, mock_cap_class):
        cap = MagicMock()
        cap.isOpened.return_value = False
        mock_cap_class.return_value = cap

        fe = FrameExtractor()
        with self.assertRaises(ValueError):
            fe.extract_frames("/fake/bad.mp4")

    @patch("video_analyzer.frame_extractor.cv2.VideoCapture")
    @patch("video_analyzer.frame_extractor.os.path.exists", return_value=True)
    def test_frames_have_base64_data(self, mock_exists, mock_cap_class):
        fps = 10.0
        frame_count = 30
        mock_cap_class.return_value = self._make_cap_mock(fps, frame_count)

        fe = FrameExtractor(max_duration=60, frames_per_second=1)
        frames = fe.extract_frames("/fake/video.mp4")

        for f in frames:
            # Should be valid base64
            try:
                decoded = base64.b64decode(f.base64_jpeg)
                self.assertGreater(len(decoded), 0)
            except Exception:
                self.fail(f"Frame {f.index} base64_jpeg is not valid base64")


class TestEncodeFrame(unittest.TestCase):
    """Test the static _encode_frame helper."""

    @patch("video_analyzer.frame_extractor.cv2.imencode")
    def test_encode_returns_base64_string(self, mock_imencode):
        fake_bytes = b"\xff\xd8\xff\xe0test_jpeg_data"
        mock_imencode.return_value = (True, np.frombuffer(fake_bytes, dtype=np.uint8))

        frame = _make_bgr_frame()
        result = FrameExtractor._encode_frame(frame)
        self.assertIsInstance(result, str)
        self.assertEqual(result, base64.b64encode(fake_bytes).decode("utf-8"))

    @patch("video_analyzer.frame_extractor.cv2.imencode", return_value=(False, None))
    def test_encode_raises_on_failure(self, mock_imencode):
        frame = _make_bgr_frame()
        with self.assertRaises(ValueError):
            FrameExtractor._encode_frame(frame)


class TestVideoFrameDataclass(unittest.TestCase):
    """Test the VideoFrame dataclass."""

    def test_creation(self):
        vf = VideoFrame(index=0, timestamp_seconds=1.5, base64_jpeg="abc123")
        self.assertEqual(vf.index, 0)
        self.assertEqual(vf.timestamp_seconds, 1.5)
        self.assertEqual(vf.base64_jpeg, "abc123")


if __name__ == "__main__":
    unittest.main()
