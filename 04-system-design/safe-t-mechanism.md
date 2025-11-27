# SAFE-T: Time-Indexed SAFE

**Powered by TRUST | Recorded on LOVE**

---

## One-Liner

**"We raise on a SAFE-T — a Time-Indexed SAFE powered by TRUST and recorded on LOVE."**

Memorable. Explainable. Not gimmicky. Not reactive. Massively different.

---

## What Each Word Means

### SAFE-T — Time-Indexed SAFE

SAFE-T is a standard SAFE that includes:

- **Deterministic pricing over time** — Formulas are public, non-negotiable
- **Visible valuation changes** — Current cap displayed in real-time
- **Guaranteed fair ordering** — First to commit, first in queue
- **Non-negotiable formulas** — No side deals, no exceptions
- **Countdown enforcement** — 7-day TTL to wire or lose spot
- **No side channels** — Everything public, everything transparent

**In plain English:**

The earlier you commit, the better the terms.
The longer you wait, the price rises.

No soft-circling.
No special favors.
No ambiguity.

**Time becomes the pricing engine.**

---

### TRUST — The Pricing Engine

TRUST is not branding.

It is the model layer.

It is the system that:

- calculates valuation
- applies size discounts
- assigns time tiers
- enforces TTLs
- maintains queue order
- governs fairness

**Think of TRUST as:**

The decision-making core.

All math lives here.

Nothing is hidden.

---

### LOVE — The Ledger

LOVE is not "emotion."

LOVE is:

**Ledger of Verifiable Events**

LOVE records:

- commitment timestamps
- valuation locks
- expiration windows
- confirmations
- missed TTLs
- identity records

LOVE does not decide.

LOVE remembers.

LOVE is the memory of the system.

---

## How a SAFE-T Works (One Screen)

### Event Lifecycle

```
1. Investor presses YesPen
   ↓
2. TRUST computes the terms
   ↓
3. LOVE records the moment
   ↓
4. TTL starts (7 days)
   ↓
5. Wire received or expires
   ↓
6. Queue updates publicly
```

**Formulaic. Transparent. Permanent.**

No persuasion.
No chase.
No politics.

Just timing.

---

## Mental Model for Investors

You are not "selling them on a pitch."

You are offering them:

**A deterministic entrance ramp into a company.**

Their position is:

- timestamped
- priced
- ranked
- archived

Instead of vibes.

---

## VC Translation Layer

### "Is this a crypto thing?"

**You say:**

"No — LOVE is our internal ledger. The SAFE is legal. TRUST is our pricing model."

### "Why does valuation move?"

**You say:**

"Because information spreads. We simply refuse to pretend it doesn't."

### "Why is the cap lower later?"

**You say:**

"Because early conviction is rare. And rare things are priced accordingly."

---

## Visual Presentation

**One slide.**

**Black background.**

**Three words:**

```
SAFE-T

Time-Indexed SAFE

POWERED BY

TRUST

RECORDED ON

LOVE
```

**Underneath:**

*Pricing by time. Memory by design. Commitment without negotiation.*

---

## This Makes You Un-Gameable

You no longer negotiate.

You publish a system.

You don't pressure.

You open a window.

You don't chase.

You wait.

---

## The Subtle Power Move

This line:

**"powered by TRUST"**

quietly does something devastating:

**It implies you trust your own system more than their judgment.**

That signals:

- founder authority
- epistemic confidence
- vision beyond check size

Investors respect that far more than softness.

---

## TRUST: The Pricing Formulas

### Base Valuation (Time Decay)

**V(t) = V₀ × (1 - αt)** with floor at `V_min`

Where:
- `V₀` = Starting cap (e.g., $5M)
- `α` = Daily decay rate (e.g., 0.02 = 2% per day)
- `t` = Days since raise start
- `V_min` = Floor (e.g., $3.5M = 70% of V₀)

**Example:**
- Day 0: $5.0M
- Day 1: $4.9M
- Day 7: $4.3M
- Day 14: $3.6M
- Day 20+: $3.5M (floor)

### Size Discount Tiers

| Commitment Size | Discount |
|----------------|----------|
| $5k - $24k     | 0% |
| $25k - $49k    | 5% |
| $50k - $99k    | 10% |
| $100k - $249k  | 15% |
| $250k+         | 20% |

### Temporal Discount Tiers

| Days Since Start | Discount |
|-----------------|----------|
| Day 1-3         | 10% |
| Day 4-7         | 7% |
| Day 8-14        | 5% |
| Day 15-21       | 3% |
| Day 22+         | 0% |

### Effective Valuation Formula

**EffectiveValuation = V(t) × (1 - SizeDiscount) × (1 - TemporalDiscount)**

### Equity Calculation

**Equity% = Commitment / EffectiveValuation**

---

## Examples

### Example 1: Early Large Commitment

**Day 2, $100k commitment:**

- Base V(2) = $4.8M
- Size discount: 15%
- Temporal discount: 10%
- **Effective = $4.8M × 0.85 × 0.90 = $3.67M**
- **Equity = $100k / $3.67M = 2.72%**

### Example 2: Late Small Commitment

**Day 20, $10k commitment:**

- Base V(20) = $3.5M (floor)
- Size discount: 0%
- Temporal discount: 3%
- **Effective = $3.5M × 1.0 × 0.97 = $3.40M**
- **Equity = $10k / $3.40M = 0.29%**

**Per dollar invested:** Early investor gets ~9.4× better terms.

---

## TTL Mechanism

### 7-Day Wire Window

1. **YesPen Press** → TRUST computes terms, LOVE records commitment
2. **TTL Starts** → 7 days to wire funds
3. **Wire Received** → LOVE confirms, spot locked, YesPen engraved
4. **Wire Not Received** → LOVE records expiration, investor goes to end of queue

### Queue System

**Active Queue (Awaiting Wire):**
- Ordered by: YesPen press timestamp
- Status: "Awaiting Wire"
- TTL: 7 days from press

**Expired Queue (Missed TTL):**
- Moved to end of queue
- Must press YesPen again
- Gets current (worse) valuation

**Confirmed Queue (Wired):**
- Locked in
- YesPen engraved
- Investor number assigned

---

## LOVE: Ledger Structure

### Commitment Record

```json
{
  "type": "safe_t_commitment",
  "timestamp": 1234567890,
  "iso_time": "2025-01-15T14:30:00Z",
  "actor": "YesPen_001",
  "action": "COMMITMENT",
  "trust_terms": {
    "base_valuation": 4800000,
    "size_discount": 0.15,
    "temporal_discount": 0.10,
    "effective_valuation": 3672000,
    "commitment_amount": 100000,
    "equity_percentage": 2.72
  },
  "ttl": {
    "deadline": "2025-01-22T14:30:00Z",
    "status": "awaiting_wire"
  },
  "queue_position": 7
}
```

### Confirmation Record

```json
{
  "type": "safe_t_confirmation",
  "timestamp": 1235000000,
  "iso_time": "2025-01-20T10:00:00Z",
  "commitment_id": "commit_1234567890",
  "wire_received": true,
  "investor_number": 7,
  "status": "confirmed"
}
```

### Expiration Record

```json
{
  "type": "safe_t_expiration",
  "timestamp": 1235172800,
  "iso_time": "2025-01-22T14:30:00Z",
  "commitment_id": "commit_1234567890",
  "wire_received": false,
  "status": "expired",
  "queue_action": "moved_to_end"
}
```

---

## Implementation

### TRUST Engine

- **File:** `code/trust.py`
- **Function:** Calculates effective valuations
- **Input:** Days since start, commitment amount
- **Output:** Effective valuation, discounts, equity percentage

### LOVE Ledger

- **File:** `code/love.py`
- **Function:** Records all events
- **Storage:** JSON files in `love_notes/` directory
- **Format:** Standardized LOVE Note structure

### YesPen Integration

- **File:** `code/station.py`
- **Flow:** Press → TRUST computes → LOVE records → TTL starts

---

## Configuration

```python
# TRUST Configuration
V0 = 5_000_000  # Starting cap
V_min = 3_500_000  # Floor (70% of V0)
alpha = 0.02  # 2% daily decay
TTL_DAYS = 7

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
```

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
- ❌ Side deals → Everything recorded on LOVE

---

## Legal Structure

**SAFE-T is a standard SAFE with:**

- Time-indexed valuation cap
- Public pricing formulas
- Non-negotiable terms
- Standard SAFE provisions (discount, MFN, etc.)

**Legal documents reference:**

- TRUST formulas (public, deterministic)
- LOVE ledger (verifiable, timestamped)
- TTL enforcement (7-day window)

**No special legal complexity.**

**Just a standard SAFE with transparent, time-based pricing.**

---

## Next Steps

1. **Implement TRUST engine** → Pricing calculations
2. **Implement LOVE ledger** → Event recording
3. **Integrate with YesPen** → Press → TRUST → LOVE flow
4. **Build investor dashboard** → Show terms, TTL, queue position
5. **Create legal docs** → SAFE-T template with TRUST/LOVE references

---

**SAFE-T: Pricing by time. Memory by design. Commitment without negotiation.**

**Powered by TRUST. Recorded on LOVE.**

