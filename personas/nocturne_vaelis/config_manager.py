"""
Nocturne Vaelis - Configuration Manager

Provides module-level config caching to avoid redundant file reads when multiple
components (ScenarioRandomizer, ModeSwitcher, SafetyCoordinator, PersonaEngine)
load the same JSON configuration.  Also exposes delta-update helpers for
minimal-overhead config modifications.
"""

import json
import copy
from typing import Any, Dict

# Module-level cache: maps absolute config path -> parsed config dict
_config_cache: Dict[str, Dict[str, Any]] = {}


def get_config(path: str) -> Dict[str, Any]:
    """
    Return the parsed JSON configuration for *path*, loading and caching it on
    the first call.  Subsequent calls with the same path return the cached copy
    without touching the filesystem.

    Args:
        path: Absolute or relative path to the JSON config file.

    Returns:
        Parsed configuration dictionary.  The returned object is the cached
        instance shared across all callers; **do not mutate it in place**.
        Use :func:`apply_delta` for updates, or call ``dict.copy()`` if you
        need a writable snapshot.
    """
    if path not in _config_cache:
        with open(path, "r") as f:
            _config_cache[path] = json.load(f)
    return _config_cache[path]


def apply_delta(path: str, delta: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply a shallow delta (key→value overrides) to a cached config and return
    the updated copy.  The cache entry is replaced so future calls to
    :func:`get_config` see the new values.

    This supports the *Delta operations* requirement: only changed keys need to
    be supplied, minimising the overhead of incremental config updates.

    Args:
        path:  Path to the config file whose cached entry should be updated.
        delta: Flat dict of top-level key overrides to merge into the config.

    Returns:
        Updated configuration dictionary.
    """
    current = copy.deepcopy(get_config(path))  # deep copy protects nested structures
    current.update(delta)
    _config_cache[path] = current
    return current


def clear_cache(path: str = None) -> None:
    """
    Evict one or all entries from the cache.

    Args:
        path: If provided, evict only that entry; otherwise clear everything.
    """
    if path is not None:
        _config_cache.pop(path, None)
    else:
        _config_cache.clear()
