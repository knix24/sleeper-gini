# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

sleeper-gini analyzes competitive balance in Sleeper dynasty fantasy football leagues using the Gini coefficient. It pulls roster data from Sleeper and player values from FantasyCalc to measure wealth distribution across teams.

## Build & Run

```bash
# Setup
python3 -m venv .venv && .venv/bin/pip install -e .

# Run from repo
./sleeper-gini                        # Interactive mode
./sleeper-gini <league_id>            # Direct mode
./sleeper-gini --json                 # JSON output
./sleeper-gini --superflex            # Use superflex values
./sleeper-gini --ppr 0.5              # Specify PPR scoring
```

## Architecture

```
src/sleeper_gini/
├── cli.py              # Click CLI entry point, orchestrates analysis
├── models.py           # Pydantic models for API responses and results
├── api/
│   ├── sleeper.py      # Sleeper API client (leagues, rosters, users)
│   └── fantasycalc.py  # FantasyCalc API client (player values, cached)
└── services/
    ├── cache.py        # File-based cache with 24-hour TTL (~/.cache/sleeper-gini/)
    ├── gini.py         # Gini coefficient calculation and interpretation
    └── matcher.py      # Maps Sleeper player IDs to FantasyCalc values
```

## External APIs

**Sleeper API** (no auth required)
- Base: `https://api.sleeper.app/v1`
- Rate limit: 1000 req/min
- Docs: https://docs.sleeper.com

**FantasyCalc API** (no auth required)
- Base: `https://api.fantasycalc.com`
- Endpoint: `GET /values/current?isDynasty=true&numQbs=1&numTeams=12&ppr=1`
- Values cached for 24 hours to avoid repeated calls

## Key Design Decisions

- Interactive mode prompts for username, fetches user's leagues, and lets them select one
- Season is auto-detected from Sleeper's NFL state endpoint
- League size is auto-detected from selection in interactive mode
- Player matching uses FantasyCalc's `sleeperId` field
- Gini thresholds: <0.15 Highly Competitive, <0.25 Healthy, <0.35 Imbalanced, ≥0.35 Severely Lopsided
- CLI outputs to stderr for status, stdout for results (enables clean JSON piping)
