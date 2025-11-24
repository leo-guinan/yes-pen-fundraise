# Yes Room Architecture

## Overview

The Yes Room is the open, GitHub-based data room for the Yes Pen Raise.

It is:

- a repository of truth
- a coordination space for scouting
- a reference for investors
- a living artifact of the raise

## GitHub-as-Data-Room

**Why GitHub:**

- full history of changes
- easy forking + PRs
- markdown-native
- transparent contributions
- simple permissions
- widely understood in tech

Each file is a unit of clarity.

Each PR is a unit of contribution.

## Structure

High-level structure:

```
yes-pen-raise/
├── README.md
├── 00-charter/
├── 01-founder/
├── 02-vision-product/
├── 03-market-memetics/
├── 04-system-design/
├── 05-risk-constraints/
├── 06-traction-metrics/
├── 07-scouting/
├── 08-investor-brief/
├── templates/
└── meta/
```

- **00-charter/** – principles, protocols
- **01-founder/** – bio, motivation, track record
- **02-vision-product/** – Yes Pen overview, roadmap, story, use cases
- **03-market-memetics/** – market overview, memetic hooks, GTM
- **04-system-design/** – PRDs, diagrams, math
- **05-risk-constraints/** – risks + mitigations
- **06-traction-metrics/** – current status and metrics
- **07-scouting/** – evaluations, artifacts, leaderboard
- **08-investor-brief/** – investor quickstart, thesis, FAQ
- **templates/** – contribution templates
- **meta/** – CONTRIBUTING, CODE_OF_CONDUCT, LICENSE, etc.

## Data Flow

### Founder → Repo

Seeds initial docs (charter, bio, product, basic market).

### Scouts → Repo

1. Fork repo
2. Add evaluations/artifacts under 07-scouting/
3. PR back into main repo

### Maintainer (you or team) → Repo

1. Reviews PRs
2. Merges high-quality contributions
3. Updates leaderboard / metrics

### Investors → Repo

1. Read README.md → 08-investor-brief/ → deeper folders as needed
2. Make Yes/No decision based on public info

### Founder → External Systems

1. Update Yes Ledger (may live in Notion/Airtable initially)
2. Generate engraving specs from ledger + multipliers

### Artifacts → Outside World

Diagrams, maps, and stories can be exported for marketing, pitch decks, etc.

## Integration Points

- **Notion/Airtable/Sheets** for Yes Ledger and pen orders
- **Engraving / manufacturing partner** for Yes Pens
- **Farcaster / Twitter / communities** pointing to the repo as source-of-truth

**Optional future:**

- Scripts to auto-generate leaderboards from markdown/CSV
- Dashboards visualizing scouting activity
- Simple static site (e.g., via GitHub Pages) for investors who aren't GitHub-native

---

**This is the technical architecture document.**
