# sleeper-gini

Analyze competitive balance in Sleeper dynasty fantasy football leagues using the Gini coefficient.

## What it does

Pulls roster data from Sleeper and player trade values from FantasyCalc to measure how evenly "wealth" (roster value) is distributed across your league.

```
$ sleeper-gini
Enter your Sleeper username: fantasy_guru

Leagues for fantasy_guru:

┏━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ # ┃ League Name                    ┃ Teams  ┃ Season ┃
┡━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ 1 │ Dynasty Bros League            │ 12     │ 2025   │
│ 2 │ Work League                    │ 10     │ 2025   │
└───┴────────────────────────────────┴────────┴────────┘

Select a league [1]: 1

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

**Quick install with pipx (recommended):**
```bash
pipx install git+https://github.com/knix24/sleeper-gini.git
```

**Or with pip:**
```bash
pip install git+https://github.com/knix24/sleeper-gini.git
```

**Run from repo:**
```bash
git clone https://github.com/knix24/sleeper-gini.git
cd sleeper-gini
python3 -m venv .venv && .venv/bin/pip install -e .
source .venv/bin/activate
./sleeper-gini
```

## Usage

```bash
# Interactive mode - prompts for username and league selection
./sleeper-gini

# Direct mode - specify league ID directly
./sleeper-gini <league_id>

# JSON output (for piping to other tools)
./sleeper-gini --json
```

Scoring settings (PPR, superflex) are auto-detected from the league.

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
