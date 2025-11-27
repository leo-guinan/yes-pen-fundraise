# Rolling Safe Mechanism: Time-Decay Valuation with Commitment Tiers

## Overview

The Rolling Safe is a dynamic fundraising mechanism that:

- **Rewards conviction** — earlier commitments and larger sizes get better terms
- **Creates urgency** — valuation decays as more people see it and meetings pack in
- **Enforces commitment** — 7-day TTL to wire funds or lose your spot
- **Captures moments** — YesPen press locks in the valuation at that instant

This aligns with Conscious Economics: **time has value, conviction has value, commitment has value.**

---

## Core Mechanism

### 1. Base Valuation Decay Function

The base valuation starts at `V₀` and decays over time as signal spreads:

**V(t) = V₀ × e^(-λt)**

Where:
- `V₀` = Starting valuation cap (e.g., $5M)
- `λ` = Decay rate (e.g., 0.05 per day = 5% daily decay)
- `t` = Days since raise start

**Alternative: Linear Decay (Simpler)**

**V(t) = V₀ × (1 - αt)**

Where:
- `α` = Daily decay percentage (e.g., 0.02 = 2% per day)
- `t` = Days since raise start
- Minimum floor: `V_min` (e.g., 70% of V₀)

**Example:**
- Start: $5M cap
- Day 1: $5M × 0.98 = $4.9M
- Day 7: $5M × 0.86 = $4.3M
- Day 14: $5M × 0.72 = $3.6M
- Floor at $3.5M (70%)

### 2. Commitment Size Multiplier

Larger commitments get better effective valuations:

**SizeMultiplier(commitment) = 1 + β × log(commitment / min_commitment)**

Where:
- `β` = Size sensitivity (e.g., 0.15)
- `min_commitment` = Minimum investment (e.g., $5k)

**Tiered Alternative (Clearer for investors):**

| Commitment Size | Effective Valuation Discount |
|----------------|----------------------------|
| $5k - $24k     | Base valuation (no discount) |
| $25k - $49k    | 5% discount |
| $50k - $99k    | 10% discount |
| $100k - $249k  | 15% discount |
| $250k+         | 20% discount |

**Effective Valuation = V(t) × (1 - SizeDiscount)**

### 3. Temporal Multiplier (Early Believer Bonus)

Earlier commitments get additional discounts:

**TemporalMultiplier(t) = 1 + γ × (T_max - t) / T_max**

Where:
- `γ` = Temporal bonus max (e.g., 0.20 = 20% max bonus)
- `T_max` = Decay period (e.g., 30 days)
- `t` = Days since raise start

**Tiered Alternative:**

| Commitment Day | Additional Discount |
|----------------|-------------------|
| Day 1-3        | 10% |
| Day 4-7        | 7% |
| Day 8-14       | 5% |
| Day 15-21      | 3% |
| Day 22+        | 0% |

### 4. Final Effective Valuation Formula

**EffectiveValuation(t, commitment) = V(t) × (1 - SizeDiscount) × (1 - TemporalDiscount)**

**Example:**
- Day 2, $50k commitment
- Base V(2) = $4.9M
- Size discount: 10%
- Temporal discount: 10%
- **Effective = $4.9M × 0.90 × 0.90 = $3.97M**

vs.

- Day 15, $10k commitment
- Base V(15) = $3.7M
- Size discount: 0%
- Temporal discount: 3%
- **Effective = $3.7M × 1.0 × 0.97 = $3.59M**

**The early $50k investor gets ~10% better terms than the late $10k investor.**

---

## TTL Mechanism (7-Day Wire Window)

### How It Works

1. **YesPen Press** → Commitment registered, valuation locked
2. **7-Day Clock Starts** → Investor has 7 days to wire funds
3. **Wire Received** → Spot confirmed, YesPen engraved, investor number assigned
4. **Wire Not Received** → Commitment expires, investor goes to end of queue

### Queue System

**Active Queue (Committed, Not Wired):**
- Ordered by: YesPen press timestamp
- Status: "Awaiting Wire"
- TTL: 7 days from press

**Expired Queue (Missed TTL):**
- Moved to end of queue
- Must press YesPen again to re-enter
- Gets current (worse) valuation

**Confirmed Queue (Wired):**
- Locked in
- YesPen engraved
- Investor number assigned

### TTL Enforcement

```
On YesPen Press:
  - Register commitment with timestamp T₀
  - Lock in EffectiveValuation(T₀, commitment)
  - Set TTL = T₀ + 7 days
  - Add to Active Queue

On Day 7 Check:
  IF wire NOT received:
    - Move to Expired Queue
    - Release spot
    - Notify investor (optional)
  
  IF wire received:
    - Confirm spot
    - Engrave YesPen
    - Assign investor number
    - Move to Confirmed Queue
```

---

## YesPen Integration

### Capturing the Moment

When YesPen is pressed:

1. **Timestamp captured** → `t_press`
2. **Current valuation calculated** → `V(t_press)`
3. **Commitment size recorded** → Investor specifies amount
4. **Effective valuation locked** → `EffectiveValuation(t_press, commitment)`
5. **TTL set** → `t_press + 7 days`
6. **LOVE Note minted** → Includes all terms

### LOVE Note Structure

```json
{
  "type": "investment_commitment",
  "timestamp": 1234567890,
  "iso_time": "2025-01-15T14:30:00Z",
  "actor": "YesPen_001",
  "action": "YES_COMMITMENT",
  "context": {
    "session_id": "raise_2025_01",
    "role": "investor_commitment",
    "commitment_amount": 50000,
    "base_valuation": 4900000,
    "size_discount": 0.10,
    "temporal_discount": 0.10,
    "effective_valuation": 3969000,
    "equity_percentage": 1.26,
    "ttl_deadline": "2025-01-22T14:30:00Z",
    "status": "awaiting_wire"
  },
  "machine_signature": "pending_crypto_layer"
}
```

---

## Examples

### Example 1: Early Large Commitment

**Scenario:**
- Day 2 of raise
- Investor presses YesPen
- Commits $100k
- Base valuation: $4.9M

**Calculation:**
- Size discount: 15% (tier: $100k-$249k)
- Temporal discount: 10% (Day 1-3)
- Effective valuation: $4.9M × 0.85 × 0.90 = **$3.75M**
- Equity: $100k / $3.75M = **2.67%**

**If they wire within 7 days:** Locked in at $3.75M cap
**If they don't wire:** Go to end of queue, must commit again at worse terms

### Example 2: Late Small Commitment

**Scenario:**
- Day 20 of raise
- Investor presses YesPen
- Commits $10k
- Base valuation: $3.6M (decayed)

**Calculation:**
- Size discount: 0% (tier: $5k-$24k)
- Temporal discount: 3% (Day 15-21)
- Effective valuation: $3.6M × 1.0 × 0.97 = **$3.49M**
- Equity: $10k / $3.49M = **0.29%**

**Comparison:** Early $100k investor gets 2.67% vs late $10k investor gets 0.29%
**Per dollar invested:** Early investor gets ~9.2× better terms per dollar

### Example 3: TTL Expiration

**Scenario:**
- Day 5: Investor presses YesPen, commits $50k
- Effective valuation locked: $4.2M
- TTL deadline: Day 12
- Day 12: No wire received

**Result:**
- Commitment expires
- Investor moved to Expired Queue
- Day 15: Investor presses YesPen again
- New effective valuation: $3.5M (worse due to decay)
- New TTL: Day 22

**Lesson:** Wire quickly or pay the decay cost.

---

## Implementation Considerations

### Real-Time Valuation Display

The Yes Room should show:
- Current base valuation: `V(t)` (updates daily)
- Time until next decay: Countdown
- Active commitments: Number awaiting wire
- Confirmed commitments: Number wired

### Investor Dashboard

Each investor sees:
- Their locked effective valuation
- TTL countdown
- Wire instructions
- Status (awaiting wire / confirmed / expired)

### Decay Triggers

Valuation can decay based on:
- **Time** (daily decay)
- **Signal spread** (meetings scheduled, YesPens pressed)
- **Commitment density** (more commitments = faster decay)

**Hybrid Decay:**

**V(t, meetings, commitments) = V₀ × e^(-λt) × (1 - δ × meetings) × (1 - ε × commitments)**

Where:
- `δ` = Meeting impact (e.g., 0.01 per meeting = 1% per meeting)
- `ε` = Commitment impact (e.g., 0.005 per commitment = 0.5% per commitment)

This creates urgency: **"As I pack meetings and others commit, your window closes."**

---

## Alignment with Conscious Economics

### Principles Applied

1. **Time Violence Elimination** → 7-day TTL prevents slow-walking
2. **Conviction Rewarded** → Early + large = better terms
3. **Transparency** → All formulas public, real-time valuation visible
4. **Mutual Sovereignty** → Investor chooses commitment size, founder sets mechanism
5. **Pattern Recognition** → Rewards those who see it early

### Anti-Patterns Prevented

- ❌ Slow-drip interest → TTL forces decision
- ❌ Endless negotiation → Terms are formulaic
- ❌ Fake urgency → Real decay creates real urgency
- ❌ Information asymmetry → All formulas public

---

## Formula Summary

### Base Valuation (Time Decay)

**V(t) = V₀ × (1 - αt)** with floor at `V_min`

### Size Multiplier

**SizeDiscount = f(commitment)** where:
- $5k-$24k: 0%
- $25k-$49k: 5%
- $50k-$99k: 10%
- $100k-$249k: 15%
- $250k+: 20%

### Temporal Multiplier

**TemporalDiscount = g(t)** where:
- Day 1-3: 10%
- Day 4-7: 7%
- Day 8-14: 5%
- Day 15-21: 3%
- Day 22+: 0%

### Final Effective Valuation

**EffectiveValuation = V(t) × (1 - SizeDiscount) × (1 - TemporalDiscount)**

### Equity Calculation

**Equity% = Commitment / EffectiveValuation**

---

## Configuration Parameters

```python
# Base valuation
V0 = 5_000_000  # Starting cap
V_min = 3_500_000  # Floor (70% of V0)
alpha = 0.02  # 2% daily decay

# Size tiers
SIZE_TIERS = {
    (5_000, 24_999): 0.00,
    (25_000, 49_999): 0.05,
    (50_000, 99_999): 0.10,
    (100_000, 249_999): 0.15,
    (250_000, float('inf')): 0.20,
}

# Temporal tiers
TEMPORAL_TIERS = {
    (0, 3): 0.10,
    (4, 7): 0.07,
    (8, 14): 0.05,
    (15, 21): 0.03,
    (22, float('inf')): 0.00,
}

# TTL
TTL_DAYS = 7
```

---

## Next Steps

1. **Implement calculation engine** → Python function that computes effective valuation
2. **Integrate with YesPen** → Capture timestamp, calculate terms, mint LOVE Note
3. **Build investor dashboard** → Show locked terms, TTL countdown, wire status
4. **Create real-time display** → Current valuation, decay countdown, active commitments
5. **Wire tracking system** → Monitor TTLs, move expired commitments to queue

---

**This mechanism rewards conviction, creates urgency, and aligns incentives perfectly.**

**The YesPen press captures maximum value that rapidly decays as signal spreads.**

**Wire within 7 days or lose your spot.**

