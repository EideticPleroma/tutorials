"""
Shared state management for multi-agent systems.

Provides file-based state storage with locking for
safe concurrent access by multiple agents.

Cross-platform file locking:
- Unix/Linux/Mac: Uses fcntl
- Windows: Uses msvcrt
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Optional, Dict
import logging

# Cross-platform file locking
if sys.platform == "win32":
    import msvcrt

    WINDOWS = True
else:
    import fcntl

    WINDOWS = False


class SharedState:
    """
    File-based shared state for multi-agent coordination.

    Provides thread-safe read/write access to shared data
    that multiple agents need to access.

    Uses JSON for human-readable storage and debugging.
    Uses file locking to prevent race conditions.

    Example:
        state = SharedState()

        # Research agent writes
        state.set("research_findings", [
            {"fact": "EV sales: 10M", "source": "IEA"},
            {"fact": "Growth: 55%", "source": "IEA"}
        ])

        # Data agent reads
        findings = state.get("research_findings")
        # Analyze findings...

        state.set("data_analysis", {
            "growth_rate": 55,
            "market_size": 10.1
        })

        # Writer agent reads both
        findings = state.get("research_findings")
        analysis = state.get("data_analysis")
        # Create report...
    """

    def __init__(self, state_dir: str = ".agent_state"):
        """
        Initialize shared state.

        Args:
            state_dir: Directory to store state files
        """
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)
        self.state_file = self.state_dir / "shared_state.json"
        self.logger = logging.getLogger("shared_state")
        self._init_state()

    def _init_state(self):
        """Initialize state file if it doesn't exist."""
        if not self.state_file.exists():
            self._write({"_initialized": True})

    def get(self, key: str, default: Any = None) -> Any:
        """
        Read a value from shared state.

        Args:
            key: State key
            default: Default value if key doesn't exist

        Returns:
            Value for key, or default if not found
        """
        state = self._read()
        return state.get(key, default)

    def set(self, key: str, value: Any):
        """
        Write a value to shared state.

        Args:
            key: State key
            value: Value to store (must be JSON-serializable)
        """
        state = self._read()
        state[key] = value
        self._write(state)
        self.logger.info("State write: %s = %s", key, type(value).__name__)

    def update(self, updates: Dict[str, Any]):
        """
        Update multiple keys at once.

        Args:
            updates: Dictionary of key-value pairs to update
        """
        state = self._read()
        state.update(updates)
        self._write(state)

    def get_all(self) -> Dict[str, Any]:
        """
        Get all state data.

        Returns:
            Complete state dictionary
        """
        return self._read()

    def clear(self):
        """Clear all state data."""
        self._write({"_initialized": True})
        self.logger.info("State cleared")

    def _read(self) -> Dict:
        """
        Read state with file locking (cross-platform).

        Returns:
            State dictionary
        """
        try:
            with open(self.state_file, "r") as f:
                # Lock file for reading
                self._lock_file(f, shared=True)
                try:
                    return json.load(f)
                finally:
                    self._unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"_initialized": True}

    def _write(self, state: Dict):
        """
        Write state with file locking (cross-platform).

        Args:
            state: State dictionary to write
        """
        with open(self.state_file, "w") as f:
            # Lock file for writing
            self._lock_file(f, shared=False)
            try:
                json.dump(state, f, indent=2)
            finally:
                self._unlock_file(f)

    def _lock_file(self, file_obj, shared: bool = False):
        """
        Lock file using platform-specific method.

        Args:
            file_obj: File object to lock
            shared: True for shared read lock, False for exclusive write lock
        """
        if WINDOWS:
            # Windows: msvcrt locking
            # Note: msvcrt doesn't distinguish shared/exclusive at the API level
            # We lock the first byte of the file
            file_obj.seek(0)
            try:
                msvcrt.locking(file_obj.fileno(), msvcrt.LK_LOCK, 1)
            except OSError:
                # File already locked, wait and retry
                import time

                time.sleep(0.1)
                msvcrt.locking(file_obj.fileno(), msvcrt.LK_LOCK, 1)
        else:
            # Unix: fcntl locking
            import fcntl

            lock_type = fcntl.LOCK_SH if shared else fcntl.LOCK_EX
            fcntl.flock(file_obj.fileno(), lock_type)

    def _unlock_file(self, file_obj):
        """
        Unlock file using platform-specific method.

        Args:
            file_obj: File object to unlock
        """
        if WINDOWS:
            # Windows: unlock the first byte
            file_obj.seek(0)
            msvcrt.locking(file_obj.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            # Unix: fcntl unlock
            import fcntl

            fcntl.flock(file_obj.fileno(), fcntl.LOCK_UN)
