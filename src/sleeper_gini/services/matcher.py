"""Player matching between Sleeper and FantasyCalc."""

from ..models import Player
from ..services.cache import Cache


class PlayerMatcher:
    """Match players between Sleeper and FantasyCalc data sources."""

    def __init__(self, cache: Cache | None = None):
        self.cache = cache or Cache()
        self._sleeper_id_map: dict[str, dict] = {}
        self._name_map: dict[str, dict] = {}

    def build_lookup(
        self,
        fantasycalc_data: list[dict],
        sleeper_players: dict[str, dict] | None = None,
    ) -> None:
        """Build lookup tables from FantasyCalc data.

        Args:
            fantasycalc_data: Response from FantasyCalc API
            sleeper_players: Optional Sleeper player database for fallback matching
        """
        self._sleeper_id_map.clear()
        self._name_map.clear()

        for entry in fantasycalc_data:
            player_data = entry.get("player", {})
            value = entry.get("value", 0)

            # Try to get sleeper ID directly from FantasyCalc
            sleeper_id = player_data.get("sleeperId")

            player_info = {
                "name": player_data.get("name", ""),
                "position": player_data.get("position", ""),
                "team": player_data.get("maybeTeam"),
                "value": value,
                "sleeper_id": sleeper_id,
            }

            # Primary: map by Sleeper ID if available
            if sleeper_id:
                self._sleeper_id_map[sleeper_id] = player_info

            # Secondary: map by normalized name for fallback
            name_key = self._normalize_name(
                player_data.get("name", ""),
                player_data.get("position", ""),
            )
            if name_key:
                self._name_map[name_key] = player_info

        # If sleeper_players provided, build additional name mappings
        if sleeper_players:
            self._enhance_with_sleeper_data(sleeper_players)

    def _enhance_with_sleeper_data(self, sleeper_players: dict[str, dict]) -> None:
        """Add Sleeper ID mappings by matching names."""
        for sleeper_id, player in sleeper_players.items():
            if sleeper_id in self._sleeper_id_map:
                continue

            name_key = self._normalize_name(
                f"{player.get('first_name', '')} {player.get('last_name', '')}".strip(),
                player.get("position", ""),
            )

            if name_key and name_key in self._name_map:
                fc_data = self._name_map[name_key]
                fc_data["sleeper_id"] = sleeper_id
                self._sleeper_id_map[sleeper_id] = fc_data

    def _normalize_name(self, name: str, position: str) -> str:
        """Create a normalized key for name-based matching."""
        if not name:
            return ""
        # Lowercase, remove suffixes like Jr., III, etc.
        normalized = name.lower().strip()
        for suffix in [" jr.", " jr", " sr.", " sr", " iii", " ii", " iv"]:
            normalized = normalized.replace(suffix, "")
        # Include position to avoid collisions
        return f"{normalized}_{position.lower()}"

    def get_player_value(self, sleeper_id: str) -> Player | None:
        """Look up a player's value by their Sleeper ID.

        Args:
            sleeper_id: The player's Sleeper ID

        Returns:
            Player object with value, or None if not found
        """
        if player_data := self._sleeper_id_map.get(sleeper_id):
            return Player(
                sleeper_id=sleeper_id,
                name=player_data["name"],
                position=player_data["position"],
                team=player_data["team"],
                value=player_data["value"],
            )
        return None

    def get_value(self, sleeper_id: str) -> int:
        """Get just the value for a player, defaulting to 0.

        Args:
            sleeper_id: The player's Sleeper ID

        Returns:
            Player's value, or 0 if not found
        """
        if player_data := self._sleeper_id_map.get(sleeper_id):
            return player_data["value"]
        return 0
