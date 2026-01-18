"""FantasyCalc API client."""

import httpx

from ..services.cache import Cache

BASE_URL = "https://api.fantasycalc.com"


class FantasyCalcClient:
    """Client for the FantasyCalc API."""

    def __init__(self, cache: Cache | None = None, timeout: float = 30.0):
        self.client = httpx.Client(base_url=BASE_URL, timeout=timeout)
        self.cache = cache or Cache()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.client.close()

    def get_values(
        self,
        is_dynasty: bool = True,
        num_qbs: int = 1,
        num_teams: int = 12,
        ppr: float = 1.0,
    ) -> list[dict]:
        """Fetch current player values.

        Args:
            is_dynasty: True for dynasty values, False for redraft
            num_qbs: 1 for 1QB leagues, 2 for superflex
            num_teams: League size (10, 12, 14, etc.)
            ppr: PPR scoring (0, 0.5, 1)

        Returns:
            List of player value objects from FantasyCalc
        """
        cache_key = f"fantasycalc_values_{is_dynasty}_{num_qbs}_{num_teams}_{ppr}"

        if cached := self.cache.get(cache_key):
            return cached

        resp = self.client.get(
            "/values/current",
            params={
                "isDynasty": str(is_dynasty).lower(),
                "numQbs": num_qbs,
                "numTeams": num_teams,
                "ppr": ppr,
            },
        )
        resp.raise_for_status()
        data = resp.json()

        self.cache.set(cache_key, data)
        return data
