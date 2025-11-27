import json
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple


# ---------- Data model ----------

@dataclass
class SafeTRoundConfig:
    round_id: str
    start_time_utc: datetime
    initial_cap: float
    daily_decay_rate: float
    floor_cap: float
    wire_ttl_days: int
    commitment_tiers: list  # list of (min_amount, max_amount, discount_float)


# ---------- Loading config ----------

def load_round_config(path: str) -> SafeTRoundConfig:
    """Load round configuration from JSON file.
    
    Args:
        path: Path to the JSON config file (can be relative or absolute)
    """
    with open(path, "r") as f:
        data = json.load(f)

    tiers = []
    for key, disc in data["commitment_tiers"].items():
        if "+" in key:
            # Handle "100000+" format
            lo = float(key.replace("+", ""))
            hi = float("inf")
        elif "-" in key:
            # Handle "10000-24999" format
            lo, hi = key.split("-")
            lo = float(lo)
            hi = float(hi)
        else:
            # Single value (shouldn't happen but handle gracefully)
            lo = float(key)
            hi = float("inf")
        tiers.append((lo, hi, float(disc)))

    return SafeTRoundConfig(
        round_id=data["round_id"],
        start_time_utc=datetime.fromisoformat(data["start_time_utc"].replace("Z", "+00:00")),
        initial_cap=float(data["initial_valuation_cap"]),
        daily_decay_rate=float(data["daily_decay_rate"]),
        floor_cap=float(data["minimum_cap_floor"]),
        wire_ttl_days=int(data["wire_ttl_days"]),
        commitment_tiers=sorted(tiers, key=lambda t: t[0]),
    )


# ---------- Core math ----------

def days_elapsed(start: datetime, now: Optional[datetime] = None) -> float:
    if now is None:
        now = datetime.now(timezone.utc)
    delta = now - start
    return delta.total_seconds() / 86400.0


def current_cap(cfg: SafeTRoundConfig,
                now: Optional[datetime] = None) -> float:
    """Linear time-decay with floor."""
    d = days_elapsed(cfg.start_time_utc, now)
    decayed = cfg.initial_cap * (1.0 - cfg.daily_decay_rate * d)
    return max(decayed, cfg.floor_cap)


def size_discount(cfg: SafeTRoundConfig, amount: float) -> float:
    """Return discount fraction (e.g. 0.10 for 10%)."""
    for lo, hi, disc in cfg.commitment_tiers:
        if lo <= amount <= hi:
            return disc
    return 0.0


def effective_cap(cfg: SafeTRoundConfig,
                  amount: float,
                  now: Optional[datetime] = None) -> Tuple[float, float, float]:
    """
    Returns (base_cap, discount, eff_cap)
    - base_cap: raw time-decayed cap before size discount
    - discount: size discount fraction
    - eff_cap: final cap used for this commitment
    """
    base = current_cap(cfg, now)
    disc = size_discount(cfg, amount)
    eff = base * (1.0 - disc)
    return base, disc, eff


def equity_percentage(eff_cap: float, amount: float) -> float:
    """Return equity percentage (0.0164 = 1.64%)."""
    return amount / eff_cap if eff_cap > 0 else 0.0


# ---------- Convenience wrapper (for UI / LOVE Note) ----------

def price_commitment(cfg: SafeTRoundConfig,
                     amount: float,
                     now: Optional[datetime] = None) -> dict:
    """
    Compute the full pricing snapshot for a commitment made at `now`.
    Returns a dict ready to inject into your LOVE Note.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    base_cap, disc, eff_cap = effective_cap(cfg, amount, now)
    eq = equity_percentage(eff_cap, amount)
    ttl_deadline = now + timedelta(days=cfg.wire_ttl_days)

    return {
        "round_id": cfg.round_id,
        "timestamp": now.isoformat(),
        "commitment_amount": amount,
        "base_cap": round(base_cap, 2),
        "size_discount": disc,                # 0.10 = 10%
        "effective_cap": round(eff_cap, 2),
        "equity_percentage": eq,              # 0.0164 = 1.64%
        "ttl_deadline": ttl_deadline.isoformat()
    }


# ---------- Small demo ----------

if __name__ == "__main__":
    cfg = load_round_config("SAFE-T_2025_01.json")
    amount = 50_000

    now = datetime.now(timezone.utc)
    snapshot = price_commitment(cfg, amount, now)

    print("=== TRUST v1.0 Pricing Snapshot ===")
    print(f"Round:            {snapshot['round_id']}")
    print(f"Timestamp (UTC):  {snapshot['timestamp']}")
    print(f"Commitment:       ${snapshot['commitment_amount']:,.0f}")
    print(f"Base cap:         ${snapshot['base_cap']:,.0f}")
    print(f"Size discount:    {snapshot['size_discount'] * 100:.1f}%")
    print(f"Effective cap:    ${snapshot['effective_cap']:,.0f}")
    print(f"Equity:           {snapshot['equity_percentage'] * 100:.3f}%")
    print(f"TTL deadline:     {snapshot['ttl_deadline']}")

