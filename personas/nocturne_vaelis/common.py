"""
Nocturne Vaelis - Shared Common Types

Centralises types that are reused across multiple persona modules so that each
module imports from a single authoritative source rather than maintaining its
own duplicate definition.

Previously, ``ConsentLevel`` was defined independently in both
``scenario_engine`` and ``safety_module``.  Moving it here eliminates that
redundancy while preserving full backwards-compatibility: both modules now
re-export the enum so existing import paths continue to work.
"""

from enum import Enum


class ConsentLevel(Enum):
    """
    Required consent levels, ordered from least to most explicit.

    Used by both the scenario engine (to gate scenario selection) and the
    safety module (to gate proposed actions).
    """

    NONE_REQUIRED = "none_required"
    IMPLIED = "implied"
    EXPLICIT_REQUIRED = "explicit_required"
    EXPLICIT_NEGOTIATED = "explicit_negotiated"
    EMOTIONAL = "emotional"
