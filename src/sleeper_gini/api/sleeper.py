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

    def get_user(self, username: str) -> SleeperUser:
        """Fetch user by username.

        Args:
            username: Sleeper username

        Returns:
            SleeperUser with user_id and display info
        """
        resp = self.client.get(f"/user/{username}")
        resp.raise_for_status()
        return SleeperUser(**resp.json())

    def get_nfl_state(self) -> dict:
        """Fetch current NFL state including season info.

        Returns:
            Dict with season, week, season_type, etc.
        """
        resp = self.client.get("/state/nfl")
        resp.raise_for_status()
        return resp.json()

    def get_user_leagues(
        self, user_id: str, sport: str = "nfl", season: str | None = None
    ) -> list[SleeperLeague]:
        """Fetch all leagues for a user.

        Args:
            user_id: Sleeper user ID
            sport: Sport type (default: nfl)
            season: Season year (default: current season from NFL state)

        Returns:
            List of leagues the user is in
        """
        if season is None:
            state = self.get_nfl_state()
            season = str(state.get("season", "2024"))

        resp = self.client.get(f"/user/{user_id}/leagues/{sport}/{season}")
        resp.raise_for_status()
        return [SleeperLeague(**lg) for lg in resp.json()]
