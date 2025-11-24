# Multipliers: Formulas and Curves

This folder defines the mechanism math behind the Yes Pen Raise and Scouting Game.

## Yes Curve

The Yes Curve converts signing order and timing into a base premium multiplier for investors who say Yes.

### Option A — Logarithmic Early Believer Curve

For investor with signing order n out of N total investors:

**BasePremium(n) = 1 + log(N/n)**

- n = 1 (first investor): largest boost
- As n approaches N, BasePremium approaches 1 (no premium)

**Example (N = 100):**

- n = 1 → 1 + log(100/1) ≈ 1 + 4.605 = **5.605×**
- n = 10 → 1 + log(100/10) ≈ 1 + 2.303 = **3.303×**
- n = 50 → 1 + log(100/50) ≈ 1 + 0.693 = **1.693×**
- n = 100 → 1 + log(100/100) = 1 + 0 = **1.0×**

### Option B — Tiered Yes Curve

Simple tiering for clarity:

- Investors #1–10 → **3.0×**
- #11–50 → **2.0×**
- #51–100 → **1.5×**
- #101+ → **1.1×**

You can run both in parallel (log curve for internal calculation, tier as public branding).

## Scouting Multiplier

The Scouting Multiplier rewards:

- Core contributions (evaluations)
- Artifacts (data room contributions)
- Lineage (who you bring in)
- Temporal timing (when you join)

Let:

- C = CorePoints
- A = ArtifactPoints
- L = LineagePoints
- T = TemporalMultiplier (based on tier)

**Suggested:**

**ScoutingMultiplier = (C × 0.01) + (A × 0.02) + (L × 0.015) + T**

Where **TemporalMultiplier T:**

- Scouts #1–10 → T = 3.0
- #11–50 → T = 2.0
- #51–200 → T = 1.5
- #201+ → T = 1.1

## Formulas

### 1. Final Investor Multiplier

**InvestorMultiplier = BasePremium(YesOrder) + ScoutingBonus**

Where ScoutingBonus is non-zero if the investor also acts as a scout.

### 2. Final Scout Multiplier (for engraving)

**FinalScoutMultiplier = ScoutingMultiplier**

This number is engraved on their Yes Pen.

## Examples

### Example Scout A

- CorePoints C = 60
- ArtifactPoints A = 120
- LineagePoints L = 40
- Temporal tier = first 10 scouts → T = 3.0

**ScoutingMultiplier = (60 × 0.01) + (120 × 0.02) + (40 × 0.015) + 3.0**

**= 0.6 + 2.4 + 0.6 + 3.0 = 6.6×**

Engraving might show: **SCOUT MULTI: 6.6×**.

### Example Investor B

- Yes order = 7 of 100 → BasePremium ≈ 1 + log(100/7) ≈ 1 + 2.659 = **3.659×**
- Also minor scout: ScoutingBonus = 0.5×

**Total:**

**InvestorMultiplier ≈ 3.659 + 0.5 = 4.159×**

---

**This is the mechanism math.**
