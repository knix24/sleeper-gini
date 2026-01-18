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
    starters: list[str] | None = None


class SleeperLeague(BaseModel):
    """Sleeper league data."""

    league_id: str
    name: str
    season: str
    total_rosters: int
    roster_positions: list[str] | None = None


class FantasyCalcPlayer(BaseModel):
    """Player data from FantasyCalc API."""

    sleeper_id: str | None = Field(None, alias="sleeperId")
    name: str = ""
    position: str = ""
    team: str | None = Field(None, alias="maybeTeam")
    value: int = 0
    rank: int | None = Field(None, alias="overallRank")

    class Config:
        populate_by_name = True
