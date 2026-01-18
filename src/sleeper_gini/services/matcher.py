"""Player matching between Sleeper and FantasyCalc."""

from ..models import Player


class PlayerMatcher:
    """Match players between Sleeper and FantasyCalc data sources."""

    def __init__(self):
        self._sleeper_id_map: dict[str, dict] = {}

    def build_lookup(self, fantasycalc_data: list[dict]) -> None:
        """Build lookup table from FantasyCalc data.

        Args:
            fantasycalc_data: Response from FantasyCalc API
        """
        self._sleeper_id_map.clear()

        for entry in fantasycalc_data:
            player_data = entry.get("player", {})
            sleeper_id = player_data.get("sleeperId")

            if sleeper_id:
                self._sleeper_id_map[sleeper_id] = {
                    "name": player_data.get("name", ""),
                    "position": player_data.get("position", ""),
                    "team": player_data.get("maybeTeam"),
                    "value": entry.get("value", 0),
                }

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
