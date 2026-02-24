"""
Nocturne Vaelis - Configuration Manager

Provides module-level config caching to avoid redundant file reads when multiple
components (ScenarioRandomizer, ModeSwitcher, SafetyCoordinator, PersonaEngine)
load the same JSON configuration.  Also exposes delta-update helpers for
minimal-overhead config modifications.

The cache is protected by a ``threading.Lock`` so concurrent requests share a
single parse result without races.
"""

import copy
import json
import threading
from typing import Any, Dict

# Module-level cache: maps config path -> parsed config dict
_config_cache: Dict[str, Dict[str, Any]] = {}
_cache_lock = threading.Lock()


def _load(path: str) -> Dict[str, Any]:
    """Load and parse a JSON file without touching the cache (no lock required)."""
    with open(path, "r") as f:
        return json.load(f)


def get_config(path: str) -> Dict[str, Any]:
    """
    Return the parsed JSON configuration for *path*, loading and caching it on
    the first call.  Subsequent calls with the same path return the cached copy
    without touching the filesystem.

    Thread-safe: concurrent callers block until the first parse completes, then
    all share the cached result.

    Args:
        path: Absolute or relative path to the JSON config file.

    Returns:
        Parsed configuration dictionary.  The returned object is the cached
        instance shared across all callers; **do not mutate it in place**.
        Use :func:`apply_delta` for updates, or call ``dict.copy()`` if you
        need a writable snapshot.
    """
    with _cache_lock:
        if path not in _config_cache:
            _config_cache[path] = _load(path)
        return _config_cache[path]


def apply_delta(path: str, delta: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply a shallow delta (key→value overrides) to a cached config and return
    the updated copy.  The cache entry is replaced so future calls to
    :func:`get_config` see the new values.

    This supports the *Delta operations* requirement: only changed keys need to
    be supplied, minimising the overhead of incremental config updates.

    Thread-safe: the entire read-modify-write is done under the cache lock.

    Args:
        path:  Path to the config file whose cached entry should be updated.
        delta: Flat dict of top-level key overrides to merge into the config.

    Returns:
        Updated configuration dictionary.
    """
    with _cache_lock:
        # Use cached entry if present; otherwise load from disk – all under lock
        # to avoid a race between checking and populating the cache.
        current = copy.deepcopy(_config_cache.get(path) or _load(path))
        current.update(delta)
        _config_cache[path] = current
        return current


def clear_cache(path: str = None) -> None:
    """
    Evict one or all entries from the cache.

    Args:
        path: If provided, evict only that entry; otherwise clear everything.
    """
    with _cache_lock:
        if path is not None:
            _config_cache.pop(path, None)
        else:
            _config_cache.clear()
