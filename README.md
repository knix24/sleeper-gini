# sleeper-gini

Analyze competitive balance in Sleeper dynasty fantasy football leagues using the Gini coefficient.

## What it does

Pulls roster data from Sleeper and player trade values from FantasyCalc to measure how evenly "wealth" (roster value) is distributed across your league.

```
$ sleeper-gini 123456789012345678

Dynasty Bros League
Gini Coefficient: 0.284 (Healthy)

┏━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Rank ┃ Owner           ┃    Value ┃   vs Avg ┃ Bar                  ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ 1    │ gridiron_king   │   42,800 │  +10,967 │ ████████████████████ │
│ 2    │ touchdown_tom   │   36,200 │   +4,367 │ █████████████████░░░ │
│ 3    │ fantasy_guru    │   33,100 │   +1,267 │ ████████████████░░░░ │
│ ...  │                 │          │          │                      │
└──────┴─────────────────┴──────────┴──────────┴──────────────────────┘

Average Value: 31,833
Top/Bottom Ratio: 2.30x
```

## Installation

```bash
git clone https://github.com/yourusername/sleeper-gini.git
cd sleeper-gini
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
# Basic usage (find league ID in your Sleeper league URL)
sleeper-gini <league_id>

# Superflex league
sleeper-gini <league_id> --superflex

# JSON output (for piping to other tools)
sleeper-gini <league_id> --json

# Custom league settings
sleeper-gini <league_id> --teams 14 --ppr 0.5
```

## Gini Coefficient Interpretation

| Score | Meaning |
|-------|---------|
| < 0.15 | Highly Competitive - roster values very even |
| 0.15 - 0.25 | Healthy - normal variance |
| 0.25 - 0.35 | Imbalanced - clear haves and have-nots |
| > 0.35 | Severely Lopsided - league health concern |

## Data Sources

- **Sleeper API** - roster and league data (free, no auth)
- **FantasyCalc API** - dynasty player trade values (free, no auth)

Player values are cached locally for 24 hours to minimize API calls.
