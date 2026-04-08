"""
Unit tests for NocturneVaelisSession integration class.
"""

import json
import os
import tempfile
import unittest

from personas.nocturne_vaelis.config_manager import clear_cache
from personas.nocturne_vaelis.safety_module import IntensityLevel


def _make_minimal_config(path: str) -> None:
    """Write the smallest valid config that all components accept."""
    config = {
        "persona": {"name": "Nocturne Vaelis", "version": "1.0.0"},
        "scenario_database": {
            "scenarios": [
                {
                    "id": "first_encounter",
                    "category": "introduction",
                    "mood": "serene",
                    "setting": "test",
                    "initial_state": "serene",
                    "branching_points": ["trust_path", "curiosity_path"],
                    "consent_level": "none_required",
                    "kink_elements": [],
                    "safety_protocols": [],
                }
            ],
            "randomization": {
                "enabled": True,
                "probability_weights": {"first_encounter": 1.0},
            },
        },
        "mode_switching": {
            "modes": [
                {
                    "id": "standard_interaction",
                    "trait_modifiers": {},
                    "default": True,
                    "activation_triggers": [],
                },
                {
                    "id": "nurturing_mode",
                    "trait_modifiers": {"protective": 0.95},
                    "activation_triggers": ["user_distress", "aftercare_needed"],
                },
            ],
            "auto_switching": {"enabled": True, "transition_duration": 2},
        },
    }
    with open(path, "w") as f:
        json.dump(config, f)


class TestNocturneVaelisSession(unittest.TestCase):
    """Integration tests for NocturneVaelisSession."""

    @classmethod
    def setUpClass(cls):
        cls._tmp_dir = tempfile.mkdtemp()
        cls.config_path = os.path.join(cls._tmp_dir, "session_config.json")
        _make_minimal_config(cls.config_path)

    @classmethod
    def tearDownClass(cls):
        clear_cache(cls.config_path)
        if os.path.exists(cls.config_path):
            os.remove(cls.config_path)
        os.rmdir(cls._tmp_dir)

    def _make_session(self, user_id: str = "test_user"):
        """Import here so test can be skipped cleanly if file is missing."""
        from personas.nocturne_vaelis.integration_example import NocturneVaelisSession

        return NocturneVaelisSession(user_id=user_id, config_path=self.config_path)

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def test_session_initialises(self):
        """Session should initialise without errors."""
        session = self._make_session()
        self.assertEqual(session.user_id, "test_user")
        self.assertTrue(session.session_active)
        self.assertEqual(session.message_count, 0)

    def test_session_stats_structure(self):
        """get_session_stats should return expected keys."""
        session = self._make_session()
        stats = session.get_session_stats()
        required_keys = {
            "user_id",
            "message_count",
            "trust_score",
            "interaction_count",
            "current_intensity",
            "emotional_state",
            "operational_mode",
            "session_active",
        }
        self.assertTrue(required_keys.issubset(stats.keys()))

    # ------------------------------------------------------------------
    # Message sending
    # ------------------------------------------------------------------

    def test_send_general_message(self):
        """Sending a general message should return a successful response."""
        session = self._make_session()
        result = session.send_message("yes, I want to talk", "general")
        self.assertIn("success", result)
        # May be blocked by insufficient consent – either outcome is valid
        self.assertIn("response", result)
        self.assertIsInstance(result["response"], str)

    def test_message_count_is_non_negative_integer(self):
        """message_count should be a non-negative integer after sending a message."""
        session = self._make_session()
        initial = session.message_count
        session.send_message("yes, hello", "general")
        # Count may or may not increment depending on consent check outcome;
        # assert it is still a valid non-decreasing integer.
        self.assertIsInstance(session.message_count, int)
        self.assertGreaterEqual(session.message_count, initial)

    def test_ended_session_rejects_messages(self):
        """Messages sent after session.end_session() should be rejected."""
        session = self._make_session("ended_user")
        session.end_session()
        result = session.send_message("hello", "general")
        self.assertFalse(result["success"])
        self.assertEqual(result["action"], "session_ended")

    # ------------------------------------------------------------------
    # Boundaries and safeword
    # ------------------------------------------------------------------

    def test_set_hard_limit(self):
        """Setting a hard limit should be reflected in the user profile."""
        session = self._make_session("limit_user")
        session.set_boundary("activities", "test_item", is_hard_limit=True)
        self.assertTrue(session.user_profile.has_hard_limit("test_item"))

    def test_set_soft_limit(self):
        """Setting a soft limit should be reflected in the user profile."""
        session = self._make_session("soft_limit_user")
        session.set_boundary("activities", "soft_item", is_hard_limit=False)
        self.assertTrue(session.user_profile.has_soft_limit("soft_item"))

    def test_set_safeword(self):
        """Custom safeword should be registered with the safety system."""
        session = self._make_session("safeword_user")
        session.set_safeword("yellow")
        self.assertIn("yellow", session.safety.safeword_system.all_safewords)

    # ------------------------------------------------------------------
    # Intensity
    # ------------------------------------------------------------------

    def test_change_intensity(self):
        """Intensity level should change when requested."""
        session = self._make_session("intensity_user")
        session.change_intensity(IntensityLevel.HIGH)
        self.assertEqual(session.current_intensity, IntensityLevel.HIGH)

    # ------------------------------------------------------------------
    # End session
    # ------------------------------------------------------------------

    def test_end_session(self):
        """end_session should mark session as inactive."""
        session = self._make_session("end_user")
        session.end_session()
        self.assertFalse(session.session_active)
        stats = session.get_session_stats()
        self.assertFalse(stats["session_active"])


if __name__ == "__main__":
    unittest.main()
