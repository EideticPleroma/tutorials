"""
Shared state management for multi-agent systems.

Provides file-based state storage with locking for
safe concurrent access by multiple agents.
"""

import json
import os
from pathlib import Path
from typing import Any, Optional, Dict
import fcntl
import logging


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
        self.logger.info(f"State write: {key} = {type(value).__name__}")
    
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
        Read state with file locking.
        
        Returns:
            State dictionary
        """
        try:
            with open(self.state_file, 'r') as f:
                # Shared read lock (multiple readers OK)
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                try:
                    return json.load(f)
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"_initialized": True}
    
    def _write(self, state: Dict):
        """
        Write state with file locking.
        
        Args:
            state: State dictionary to write
        """
        with open(self.state_file, 'w') as f:
            # Exclusive write lock (only one writer)
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                json.dump(state, f, indent=2)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

