"""File-based cache with TTL support."""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


class Cache:
    """Simple file-based cache with configurable TTL."""

    def __init__(
        self,
        cache_dir: Path | None = None,
        ttl: timedelta = timedelta(days=1),
    ):
        self.cache_dir = cache_dir or Path.home() / ".cache" / "sleeper-gini"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl

    def _path(self, key: str) -> Path:
        safe_key = key.replace("/", "_").replace(":", "_")
        return self.cache_dir / f"{safe_key}.json"

    def get(self, key: str) -> Any | None:
        """Retrieve a cached value if it exists and hasn't expired."""
        path = self._path(key)

        if not path.exists():
            return None

        try:
            data = json.loads(path.read_text())
            cached_at = datetime.fromisoformat(data["cached_at"])

            if datetime.now() - cached_at > self.ttl:
                path.unlink()
                return None

            return data["value"]
        except (json.JSONDecodeError, KeyError):
            path.unlink(missing_ok=True)
            return None

    def set(self, key: str, value: Any) -> None:
        """Store a value in the cache."""
        data = {
            "cached_at": datetime.now().isoformat(),
            "value": value,
        }
        self._path(key).write_text(json.dumps(data))

    def clear(self) -> None:
        """Clear all cached data."""
        for path in self.cache_dir.glob("*.json"):
            path.unlink()
