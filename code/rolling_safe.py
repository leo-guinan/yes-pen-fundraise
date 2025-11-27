"""
TRUST: The Pricing Engine

TRUST is the model layer that:
- Calculates valuation with time decay
- Applies size discounts
- Assigns temporal discounts
- Enforces TTLs
- Maintains queue order
- Governs fairness

All math lives here. Nothing is hidden.
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SAFETerms:
    """SAFE-T terms locked in at YesPen press (computed by TRUST)"""
    timestamp: datetime
    commitment_amount: float
    base_valuation: float
    size_discount: float
    temporal_discount: float
    effective_valuation: float
    equity_percentage: float
    ttl_deadline: datetime
    status: str  # "awaiting_wire", "confirmed", "expired"
    queue_position: Optional[int] = None


class TRUST:
    """
    TRUST: The Pricing Engine
    
    Calculates effective valuations for SAFE-T commitments.
    All formulas are public, deterministic, and non-negotiable.
    """
    
    def __init__(
        self,
        v0: float = 5_000_000,  # Starting cap
        v_min: float = 3_500_000,  # Floor (70% of V0)
        alpha: float = 0.02,  # 2% daily decay
        ttl_days: int = 7,
    ):
        self.v0 = v0
        self.v_min = v_min
        self.alpha = alpha
        self.ttl_days = ttl_days
        
        # Size discount tiers
        self.size_tiers = {
            (5_000, 24_999): 0.00,
            (25_000, 49_999): 0.05,
            (50_000, 99_999): 0.10,
            (100_000, 249_999): 0.15,
            (250_000, float('inf')): 0.20,
        }
        
        # Temporal discount tiers (days since raise start)
        self.temporal_tiers = {
            (0, 3): 0.10,
            (4, 7): 0.07,
            (8, 14): 0.05,
            (15, 21): 0.03,
            (22, float('inf')): 0.00,
        }
    
    def calculate_base_valuation(self, days_since_start: float) -> float:
        """
        Calculate base valuation with time decay.
        
        Uses linear decay: V(t) = V₀ × (1 - αt) with floor at V_min
        """
        decayed = self.v0 * (1 - self.alpha * days_since_start)
        return max(decayed, self.v_min)
    
    def get_size_discount(self, commitment: float) -> float:
        """Get size discount based on commitment tier"""
        for (min_size, max_size), discount in self.size_tiers.items():
            if min_size <= commitment <= max_size:
                return discount
        return 0.0
    
    def get_temporal_discount(self, days_since_start: float) -> float:
        """Get temporal discount based on days since raise start"""
        for (min_days, max_days), discount in self.temporal_tiers.items():
            if min_days <= days_since_start <= max_days:
                return discount
        return 0.0
    
    def calculate_effective_valuation(
        self,
        days_since_start: float,
        commitment_amount: float
    ) -> Dict[str, float]:
        """
        Calculate effective valuation with all discounts applied.
        
        Returns dict with:
        - base_valuation: V(t)
        - size_discount: discount percentage
        - temporal_discount: discount percentage
        - effective_valuation: final valuation after discounts
        - equity_percentage: commitment / effective_valuation
        """
        base_val = self.calculate_base_valuation(days_since_start)
        size_disc = self.get_size_discount(commitment_amount)
        temp_disc = self.get_temporal_discount(days_since_start)
        
        effective_val = base_val * (1 - size_disc) * (1 - temp_disc)
        equity_pct = (commitment_amount / effective_val) * 100
        
        return {
            "base_valuation": base_val,
            "size_discount": size_disc,
            "temporal_discount": temp_disc,
            "effective_valuation": effective_val,
            "equity_percentage": equity_pct,
        }
    
    def compute_safe_terms(
        self,
        raise_start_date: datetime,
        commitment_amount: float,
        press_timestamp: Optional[datetime] = None,
        queue_position: Optional[int] = None
    ) -> SAFETerms:
        """
        Compute SAFE-T terms at YesPen press moment.
        
        This is what TRUST does: calculates the deterministic terms
        based on time and commitment size.
        
        Args:
            raise_start_date: When the raise started
            commitment_amount: Investment amount
            press_timestamp: When YesPen was pressed (defaults to now)
            queue_position: Position in queue (optional)
        
        Returns:
            SAFETerms with all computed values (to be recorded on LOVE)
        """
        if press_timestamp is None:
            press_timestamp = datetime.now()
        
        days_since_start = (press_timestamp - raise_start_date).total_seconds() / 86400
        
        terms = self.calculate_effective_valuation(days_since_start, commitment_amount)
        
        ttl_deadline = press_timestamp + timedelta(days=self.ttl_days)
        
        return SAFETerms(
            timestamp=press_timestamp,
            commitment_amount=commitment_amount,
            base_valuation=terms["base_valuation"],
            size_discount=terms["size_discount"],
            temporal_discount=terms["temporal_discount"],
            effective_valuation=terms["effective_valuation"],
            equity_percentage=terms["equity_percentage"],
            ttl_deadline=ttl_deadline,
            status="awaiting_wire",
            queue_position=queue_position,
        )
    
    def check_ttl_expired(self, commitment: SAFETerms, current_time: Optional[datetime] = None) -> bool:
        """Check if SAFE-T commitment TTL has expired"""
        if current_time is None:
            current_time = datetime.now()
        return current_time > commitment.ttl_deadline and commitment.status == "awaiting_wire"
    
    def get_current_valuation(self, raise_start_date: datetime, current_time: Optional[datetime] = None) -> float:
        """Get current base valuation (for display)"""
        if current_time is None:
            current_time = datetime.now()
        days_since_start = (current_time - raise_start_date).total_seconds() / 86400
        return self.calculate_base_valuation(days_since_start)


# Example usage
if __name__ == "__main__":
    # TRUST: The Pricing Engine
    trust = TRUST()
    
    # Assume raise started on Jan 1, 2025
    raise_start = datetime(2025, 1, 1)
    
    # Example 1: Early large commitment (Day 2, $100k)
    press_time_1 = datetime(2025, 1, 3)  # Day 2
    terms_1 = trust.compute_safe_terms(raise_start, 100_000, press_time_1, queue_position=1)
    
    print("TRUST Example 1: Early Large Commitment")
    print(f"  Commitment: ${terms_1.commitment_amount:,.0f}")
    print(f"  Base Valuation: ${terms_1.base_valuation:,.0f}")
    print(f"  Size Discount: {terms_1.size_discount*100:.0f}%")
    print(f"  Temporal Discount: {terms_1.temporal_discount*100:.0f}%")
    print(f"  Effective Valuation: ${terms_1.effective_valuation:,.0f}")
    print(f"  Equity: {terms_1.equity_percentage:.2f}%")
    print(f"  TTL Deadline: {terms_1.ttl_deadline}")
    print(f"  Queue Position: {terms_1.queue_position}")
    print()
    
    # Example 2: Late small commitment (Day 20, $10k)
    press_time_2 = datetime(2025, 1, 21)  # Day 20
    terms_2 = trust.compute_safe_terms(raise_start, 10_000, press_time_2, queue_position=15)
    
    print("TRUST Example 2: Late Small Commitment")
    print(f"  Commitment: ${terms_2.commitment_amount:,.0f}")
    print(f"  Base Valuation: ${terms_2.base_valuation:,.0f}")
    print(f"  Size Discount: {terms_2.size_discount*100:.0f}%")
    print(f"  Temporal Discount: {terms_2.temporal_discount*100:.0f}%")
    print(f"  Effective Valuation: ${terms_2.effective_valuation:,.0f}")
    print(f"  Equity: {terms_2.equity_percentage:.2f}%")
    print(f"  TTL Deadline: {terms_2.ttl_deadline}")
    print(f"  Queue Position: {terms_2.queue_position}")
    print()
    
    # Current valuation display
    current_val = trust.get_current_valuation(raise_start)
    print(f"TRUST Current Base Valuation: ${current_val:,.0f}")

