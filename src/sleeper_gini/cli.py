"""CLI for sleeper-gini."""

import json
import sys

import click
from rich.console import Console
from rich.table import Table

from .api.fantasycalc import FantasyCalcClient
from .api.sleeper import SleeperClient
from .models import LeagueBalance, Player, ValuedRoster
from .services.cache import Cache
from .services.gini import calculate_gini, calculate_stats, interpret_gini
from .services.matcher import PlayerMatcher


def analyze_league(
    league_id: str,
    num_qbs: int = 1,
    num_teams: int = 12,
    ppr: float = 1.0,
) -> LeagueBalance:
    """Analyze competitive balance for a Sleeper league.

    Args:
        league_id: Sleeper league ID
        num_qbs: 1 for 1QB, 2 for superflex
        num_teams: League size for valuation context
        ppr: PPR scoring (0, 0.5, 1)

    Returns:
        LeagueBalance object with full analysis
    """
    cache = Cache()

    with SleeperClient() as sleeper, FantasyCalcClient(cache=cache) as fantasycalc:
        # Fetch data from both APIs
        league = sleeper.get_league(league_id)
        rosters = sleeper.get_rosters(league_id)
        users = sleeper.get_users(league_id)

        # Build user lookup
        user_map = {u.user_id: u for u in users}

        # Get FantasyCalc values
        fc_values = fantasycalc.get_values(
            is_dynasty=True,
            num_qbs=num_qbs,
            num_teams=num_teams,
            ppr=ppr,
        )

        # Build player matcher
        matcher = PlayerMatcher()
        matcher.build_lookup(fc_values)

        # Calculate roster values
        valued_rosters: list[ValuedRoster] = []

        for roster in rosters:
            owner = user_map.get(roster.owner_id) if roster.owner_id else None
            owner_name = owner.name if owner else f"Team {roster.roster_id}"

            players: list[Player] = []
            total_value = 0

            for player_id in roster.players or []:
                if player := matcher.get_player_value(player_id):
                    players.append(player)
                    total_value += player.value

            valued_rosters.append(
                ValuedRoster(
                    owner_id=roster.owner_id or str(roster.roster_id),
                    owner_name=owner_name,
                    total_value=total_value,
                    players=sorted(players, key=lambda p: p.value, reverse=True),
                )
            )

        # Sort rosters by value (highest first)
        valued_rosters.sort(key=lambda r: r.total_value, reverse=True)

        # Calculate Gini and stats
        values = [r.total_value for r in valued_rosters]
        gini = calculate_gini(values)
        stats = calculate_stats(values)

        return LeagueBalance(
            league_id=league_id,
            league_name=league.name,
            gini_coefficient=round(gini, 4),
            interpretation=interpret_gini(gini),
            rosters=valued_rosters,
            average_value=round(stats.average, 2),
            std_dev=round(stats.std_dev, 2),
            top_bottom_ratio=round(stats.top_bottom_ratio, 2),
        )


def print_report(result: LeagueBalance, console: Console) -> None:
    """Print a formatted report to the console."""
    console.print()
    console.print(f"[bold]{result.league_name}[/bold]")
    console.print(
        f"Gini Coefficient: [cyan]{result.gini_coefficient:.3f}[/cyan] "
        f"({result.interpretation})"
    )
    console.print()

    # Roster table
    table = Table(show_header=True, header_style="bold")
    table.add_column("Rank", style="dim", width=4)
    table.add_column("Owner", min_width=15)
    table.add_column("Value", justify="right", min_width=8)
    table.add_column("vs Avg", justify="right", min_width=8)
    table.add_column("Bar", min_width=20)

    max_value = result.rosters[0].total_value if result.rosters else 1

    for i, roster in enumerate(result.rosters, 1):
        diff = roster.total_value - result.average_value
        if diff >= 0:
            diff_str = f"[green]+{diff:,.0f}[/green]"
        else:
            diff_str = f"[red]{diff:,.0f}[/red]"

        # Visual bar
        bar_width = int((roster.total_value / max_value) * 20)
        bar = "[cyan]" + "█" * bar_width + "░" * (20 - bar_width) + "[/cyan]"

        table.add_row(
            str(i),
            roster.owner_name,
            f"{roster.total_value:,}",
            diff_str,
            bar,
        )

    console.print(table)
    console.print()
    console.print(f"Average Value: {result.average_value:,.0f}")
    console.print(f"Std Deviation: {result.std_dev:,.0f}")
    console.print(f"Top/Bottom Ratio: {result.top_bottom_ratio:.2f}x")
    console.print()


@click.command()
@click.argument("league_id")
@click.option(
    "--superflex",
    is_flag=True,
    help="Use superflex (2QB) values instead of 1QB",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Output as JSON instead of formatted table",
)
@click.option(
    "--teams",
    default=12,
    type=int,
    help="League size for valuation context (default: 12)",
)
@click.option(
    "--ppr",
    default=1.0,
    type=float,
    help="PPR scoring: 0, 0.5, or 1 (default: 1)",
)
def main(
    league_id: str,
    superflex: bool,
    as_json: bool,
    teams: int,
    ppr: float,
) -> None:
    """Analyze competitive balance for a Sleeper dynasty league.

    LEAGUE_ID is the Sleeper league ID (found in the league URL).
    """
    console = Console(stderr=True)

    try:
        with console.status("Fetching league data..."):
            result = analyze_league(
                league_id=league_id,
                num_qbs=2 if superflex else 1,
                num_teams=teams,
                ppr=ppr,
            )

        if as_json:
            # Output JSON to stdout for piping
            print(json.dumps(result.model_dump(), indent=2))
        else:
            print_report(result, Console())

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
