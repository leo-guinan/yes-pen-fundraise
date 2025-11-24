# Scouting Game PRD

## Overview

The Scouting Game turns community members into First Believer Scouts who:

- evaluate the project,
- build the Yes Room (data room),
- recruit other scouts/investors,
- and earn multipliers that are later engraved on their Yes Pens.

It is a gamified diligence protocol aligned with TrustOps (structure) and LoveOps (recognition).

## Goals

The Scouting Game is designed to:

- Crowdsource high-quality diligence
- Turn attention into clarity, not hype
- Train a new generation of pattern-recognition investors
- Reward early belief and contribution
- Produce a living, public data room (the Yes Room)
- Reduce verification cost for investors
- Protect founder time

## Mechanics

### Point System

Scouts earn points in four buckets:

**Core Points (C) – completing evaluations on the 5 axes**

- +5 pts per axis
- +10 pts for peer-endorsed clarity
- +20 pts for founder-endorsed insight

**Artifact Points (A) – contributing research artifacts**

- +10 pts minor artifact (e.g., a small market map)
- +25 pts substantial artifact (deep dive, model)
- +50 pts keystone artifact (system diagram, risk model)
- +5 pts per community upvote

**Lineage Points (L) – recruiting other scouts/investors**

- +10 pts per direct scout
- +20 pts per investor
- +5 pts per second-degree scout (diminishing returns)

**Temporal Points (T-tier) – joining early**

- First 10 scouts → +50 pts
- Scouts 11–50 → +30 pts
- Scouts 51–200 → +15 pts
- After 200 → +5 pts

Points feed into the Scouting Multiplier formula (see Multipliers section).

### Multipliers

Points translate to ScoutingMultiplier:

**(C × 0.01) + (A × 0.02) + (L × 0.015) + T**

This multiplier:

- appears on leaderboards
- is engraved on the Yes Pen
- can influence future opportunities (e.g., scout certification, invites)

### Leaderboard

The leaderboard is a simple ranking of scouts by:

- Final Scouting Multiplier

Tie-breakers:

- total artifact quality
- founder endorsements
- timeliness

Initial version can be a manual leaderboard.md updated regularly.

## User Flows

### Scout Flow

1. Discovers Yes Pen Raise (Farcaster, Twitter, community)
2. Reads Scout Manifesto & Scouting Guide
3. Forks Yes Room repo
4. Fills out evaluation-template.md under 07-scouting/evaluations/
5. Optionally adds artifacts under 07-scouting/artifacts/
6. Opens PR
7. PR is reviewed, merged, scored
8. Points accrue → multiplier updates → leaderboard updates
9. When raise ends, scout receives engraved Yes Pen reflecting their impact

## Success Metrics

- # of active scouts
- # of evaluations submitted
- # of artifacts contributed
- Quality of artifacts (peer + founder votes)
- Time from scout signup → first contribution
- Number of investors who cite the Yes Room in their decision
- Founder-reported clarity improvements

---

**This is the game design document.**
