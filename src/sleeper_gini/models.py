"""Data models for sleeper-gini."""

from pydantic import BaseModel, Field


class Player(BaseModel):
    """A player with valuation data."""

    sleeper_id: str
    name: str
    position: str
    team: str | None = None
    value: int = 0


class ValuedRoster(BaseModel):
    """A roster with total valuation."""

    owner_id: str
    owner_name: str
    total_value: int
    players: list[Player] = Field(default_factory=list)


class LeagueBalance(BaseModel):
    """Complete league balance analysis result."""

    league_id: str
    league_name: str
    gini_coefficient: float
    interpretation: str
    rosters: list[ValuedRoster]
    average_value: float
    std_dev: float
    top_bottom_ratio: float


class SleeperUser(BaseModel):
    """Sleeper user data."""

    user_id: str
    display_name: str | None = None
    username: str | None = None
    avatar: str | None = None

    @property
    def name(self) -> str:
        return self.display_name or self.username or "Unknown"


class SleeperRoster(BaseModel):
    """Sleeper roster data."""

    roster_id: int
    owner_id: str | None = None
    players: list[str] | None = None


class SleeperLeague(BaseModel):
    """Sleeper league data."""

    league_id: str
    name: str
    season: str
    total_rosters: int
    scoring_settings: dict | None = None
    roster_positions: list[str] | None = None

    @property
    def ppr(self) -> float:
        """Get PPR scoring value (0, 0.5, or 1)."""
        if self.scoring_settings:
            return float(self.scoring_settings.get("rec", 1.0))
        return 1.0

    @property
    def is_superflex(self) -> bool:
        """Check if league is superflex (has SUPER_FLEX position)."""
        if self.roster_positions:
            return "SUPER_FLEX" in self.roster_positions
        return False
