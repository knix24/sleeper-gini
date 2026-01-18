"""Sleeper API client."""

import httpx

from ..models import SleeperLeague, SleeperRoster, SleeperUser

BASE_URL = "https://api.sleeper.app/v1"


class SleeperClient:
    """Client for the Sleeper API."""

    def __init__(self, timeout: float = 30.0):
        self.client = httpx.Client(base_url=BASE_URL, timeout=timeout)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.client.close()

    def get_league(self, league_id: str) -> SleeperLeague:
        """Fetch league metadata."""
        resp = self.client.get(f"/league/{league_id}")
        resp.raise_for_status()
        return SleeperLeague(**resp.json())

    def get_rosters(self, league_id: str) -> list[SleeperRoster]:
        """Fetch all rosters in a league."""
        resp = self.client.get(f"/league/{league_id}/rosters")
        resp.raise_for_status()
        return [SleeperRoster(**r) for r in resp.json()]

    def get_users(self, league_id: str) -> list[SleeperUser]:
        """Fetch all users in a league."""
        resp = self.client.get(f"/league/{league_id}/users")
        resp.raise_for_status()
        return [SleeperUser(**u) for u in resp.json()]

    def get_players(self) -> dict[str, dict]:
        """Fetch all NFL players. Returns dict keyed by player ID.

        Note: This is a large response (~5MB). Should be cached.
        """
        resp = self.client.get("/players/nfl")
        resp.raise_for_status()
        return resp.json()
