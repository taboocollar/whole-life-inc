"""
Unit tests for Nocturne Vaelis config_manager and common modules.
"""

import json
import os
import tempfile
import threading
import unittest

from personas.nocturne_vaelis.config_manager import apply_delta, clear_cache, get_config
from personas.nocturne_vaelis.common import ConsentLevel


class TestConfigManager(unittest.TestCase):
    """Test config caching and delta updates."""

    @classmethod
    def setUpClass(cls):
        """Write a minimal config file in a temp directory."""
        cls._tmp_dir = tempfile.mkdtemp()
        cls.CONFIG_PATH = os.path.join(cls._tmp_dir, "test_config_manager.json")
        config = {"version": "1.0", "key": "original"}
        with open(cls.CONFIG_PATH, "w") as f:
            json.dump(config, f)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.CONFIG_PATH):
            os.remove(cls.CONFIG_PATH)
        os.rmdir(cls._tmp_dir)

    def setUp(self):
        """Ensure cache is clean before each test."""
        clear_cache(self.CONFIG_PATH)

    # ------------------------------------------------------------------
    # get_config
    # ------------------------------------------------------------------

    def test_get_config_returns_dict(self):
        """get_config should return the parsed dict."""
        cfg = get_config(self.CONFIG_PATH)
        self.assertIsInstance(cfg, dict)
        self.assertEqual(cfg["version"], "1.0")

    def test_get_config_caches_result(self):
        """Second call should return the identical object (cached)."""
        first = get_config(self.CONFIG_PATH)
        second = get_config(self.CONFIG_PATH)
        self.assertIs(first, second)

    def test_get_config_does_not_require_reread(self):
        """After caching, removing the file should not break subsequent calls."""
        get_config(self.CONFIG_PATH)  # populate cache
        # Temporarily rename to confirm no file I/O on second call
        tmp_path = self.CONFIG_PATH + ".bak"
        os.rename(self.CONFIG_PATH, tmp_path)
        try:
            cfg = get_config(self.CONFIG_PATH)
            self.assertEqual(cfg["version"], "1.0")
        finally:
            os.rename(tmp_path, self.CONFIG_PATH)

    # ------------------------------------------------------------------
    # apply_delta
    # ------------------------------------------------------------------

    def test_apply_delta_updates_key(self):
        """apply_delta should update specified keys."""
        apply_delta(self.CONFIG_PATH, {"key": "updated"})
        cfg = get_config(self.CONFIG_PATH)
        self.assertEqual(cfg["key"], "updated")

    def test_apply_delta_adds_new_key(self):
        """apply_delta should be able to add new top-level keys."""
        apply_delta(self.CONFIG_PATH, {"new_key": "hello"})
        cfg = get_config(self.CONFIG_PATH)
        self.assertEqual(cfg["new_key"], "hello")

    def test_apply_delta_does_not_lose_other_keys(self):
        """apply_delta should not delete keys not mentioned in the delta."""
        get_config(self.CONFIG_PATH)  # ensure cached
        apply_delta(self.CONFIG_PATH, {"key": "changed"})
        cfg = get_config(self.CONFIG_PATH)
        self.assertIn("version", cfg)

    def test_apply_delta_returns_updated_config(self):
        """apply_delta return value should reflect the new state."""
        result = apply_delta(self.CONFIG_PATH, {"key": "retval_test"})
        self.assertEqual(result["key"], "retval_test")

    # ------------------------------------------------------------------
    # clear_cache
    # ------------------------------------------------------------------

    def test_clear_cache_single_path(self):
        """Clearing a single path forces a file re-read on next get_config."""
        first = get_config(self.CONFIG_PATH)
        clear_cache(self.CONFIG_PATH)
        second = get_config(self.CONFIG_PATH)
        # Objects should be equal but not the same cached instance
        self.assertEqual(first, second)
        self.assertIsNot(first, second)

    def test_clear_cache_all(self):
        """clear_cache() with no argument should evict all entries."""
        get_config(self.CONFIG_PATH)
        clear_cache()  # evict everything
        # After clearing, a fresh read should return an equal (not same) dict
        cfg = get_config(self.CONFIG_PATH)
        self.assertIsInstance(cfg, dict)


    def test_thread_safety(self):
        """Concurrent get_config calls must all receive the same cached object."""
        results = []
        errors = []

        def fetch():
            try:
                results.append(get_config(self.CONFIG_PATH))
            except Exception as exc:  # pragma: no cover
                errors.append(exc)

        threads = [threading.Thread(target=fetch) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0)
        self.assertEqual(len(results), 20)
        # All threads should share the identical cached object
        first = results[0]
        for r in results[1:]:
            self.assertIs(r, first)


class TestCommon(unittest.TestCase):
    """Test shared ConsentLevel enum."""

    def test_consent_level_values(self):
        """ConsentLevel should expose all expected values."""
        expected = {
            "none_required",
            "implied",
            "explicit_required",
            "explicit_negotiated",
            "emotional",
        }
        actual = {level.value for level in ConsentLevel}
        self.assertEqual(actual, expected)

    def test_consent_level_importable_from_scenario_engine(self):
        """ConsentLevel re-exported from scenario_engine for backwards compat."""
        from personas.nocturne_vaelis.scenario_engine import ConsentLevel as SCL

        self.assertIs(SCL, ConsentLevel)

    def test_consent_level_importable_from_safety_module(self):
        """ConsentLevel re-exported from safety_module for backwards compat."""
        from personas.nocturne_vaelis.safety_module import ConsentLevel as SMCL

        self.assertIs(SMCL, ConsentLevel)


if __name__ == "__main__":
    unittest.main()
