"""
Video Analyzer – extract frames from short videos and evaluate computer hardware
using OpenAI Vision, then generate structured upgrade/cost reports.
"""

from .frame_extractor import FrameExtractor
from .computer_analyzer import ComputerAnalyzer
from .report_generator import ReportGenerator

__all__ = ["FrameExtractor", "ComputerAnalyzer", "ReportGenerator"]
