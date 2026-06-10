"""
WC2026 Portfolio Optimizer
==========================
Portfolio optimization for WC2026 group stage investment using
Kelly Criterion, ROI analysis, and risk-adjusted scoring.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Optional import – wc2026_market_consensus may not be available in all envs
# ---------------------------------------------------------------------------
try:
    from wc2026_market_consensus import get_consensus_prob  # type: ignore[import-untyped]
except ImportError:
    def get_consensus_prob(group: str, team: str, position: str) -> Optional[float]:
        return None


# ===================================================================
# Kelly Criterion
# ===================================================================

class KellyCriterion:
    """Calculates the Kelly fraction for each betting position."""

    @staticmethod
    def kelly_fraction(model_prob: float, market_odds: float) -> float:
        """
        kelly_fraction = (model_prob * market_odds - 1) / (market_odds - 1)

        Returns 0 if the result is negative (no edge).
        """
        if market_odds <= 1.0:
            return 0.0
        fraction = (model_prob * market_odds - 1) / (market_odds - 1)
        return max(0.0, fraction)


# ===================================================================
# ROI Calculator
# ===================================================================

class ROICalculator:
    """Calculates ROI and edge for each position."""

    @staticmethod
    def roi(model_prob: float, market_odds: float) -> float:
        """roi = (model_prob * market_odds - 1) * 100"""
        return (model_prob * market_odds - 1) * 100

    @staticmethod
    def edge(model_prob: float, market_implied_prob: float) -> float:
        """edge = (model_prob - market_implied_prob) * 100"""
        return (model_prob - market_implied_prob) * 100


# ===================================================================
# Explanation Generator
# ===================================================================

class ExplanationGenerator:
    """Generates plain-language explanations in EN / zh-Hant / zh-Hans."""

    @staticmethod
    def generate(
        team: str,
        group: str,
        position: str,
        consensus_pct: float,
        model_pct: float,
        edge_pct: float,
    ) -> Dict[str, str]:
        return {
            "en": (
                f"{team} has {consensus_pct:.1f}% consensus for {position} in "
                f"Group {group}, but our model gives {model_pct:.1f}% — "
                f"the {edge_pct:.1f}% gap creates value"
            ),
            "zh_hant": (
                f"{team} 在 {group} 組 {position} 的市場共識為 "
                f"{consensus_pct:.1f}%，但模型預測 {model_pct:.1f}% — "
                f"{edge_pct:.1f}% 的差距創造了價值"
            ),
            "zh_hans": (
                f"{team} 在 {group} 组 {position} 的市场共识为 "
                f"{consensus_pct:.1f}%，但模型预测 {model_pct:.1f}% — "
                f"{edge_pct:.1f}% 的差距创造了价值"
            ),
        }


# ===================================================================
# Data classes
# ===================================================================

@dataclass
class PositionResult:
    group: str
    position: str                       # "1st" or "2nd"
    team: str
    market_odds: float
    market_implied_prob: float
    model_prob: float
    edge_pct: float
    roi_pct: float
    kelly_fraction: float
    allocation_hkd: float
    expected_return_hkd: float
    risk_score: float
    explanation: Dict[str, str] = field(default_factory=dict)


@dataclass
class PortfolioResult:
    positions: List[PositionResult]     # sorted by edge descending
    total_allocation: float
    total_expected_return: float
    portfolio_roi: float
    risk_level: str                     # "Low" / "Medium" / "High"
    top_picks: List[PositionResult]     # top 5 by edge


# ===================================================================
# Portfolio Optimizer
# ===================================================================

class PortfolioOptimizer:
    """Main portfolio optimizer for WC2026 group-stage positions."""

    MAX_POSITION_PCT = 0.25  # cap any single position at 25 % of budget

    def __init__(self) -> None:
        self.kelly = KellyCriterion()
        self.roi_calc = ROICalculator()
        self.explainer = ExplanationGenerator()

    # ------------------------------------------------------------------
    def optimize(
        self,
        budget_hkd: float,
        positions: List[Dict],
        model_probs: Optional[Dict[str, float]] = None,
    ) -> PortfolioResult:
        """
        Run portfolio optimisation.

        Parameters
        ----------
        budget_hkd : float
            Total budget in HKD.
        positions : list[dict]
            Each dict must contain:
                group, position, team, market_odds, market_implied_prob, model_prob
        model_probs : dict, optional
            Override model probabilities keyed by "{group}:{position}:{team}".

        Returns
        -------
        PortfolioResult
        """
        # ---- a. Calculate Kelly fraction for each position ----
        candidates: List[PositionResult] = []
        for pos in positions:
            key = f"{pos['group']}:{pos['position']}:{pos['team']}"
            mp = model_probs.get(key, pos["model_prob"]) if model_probs else pos["model_prob"]
            odds = pos["market_odds"]
            mip = pos["market_implied_prob"]

            kf = self.kelly.kelly_fraction(mp, odds)
            edge_pct = self.roi_calc.edge(mp, mip)
            roi_pct = self.roi_calc.roi(mp, odds)

            # Volatility estimate: sqrt(p*(1-p)) * odds
            volatility = math.sqrt(mp * (1 - mp)) * odds
            risk_score = (mp * odds - 1) / volatility if volatility > 0 else 0.0

            explanation = self.explainer.generate(
                team=pos["team"],
                group=pos["group"],
                position=pos["position"],
                consensus_pct=mip * 100,
                model_pct=mp * 100,
                edge_pct=edge_pct,
            )

            candidates.append(PositionResult(
                group=pos["group"],
                position=pos["position"],
                team=pos["team"],
                market_odds=odds,
                market_implied_prob=mip,
                model_prob=mp,
                edge_pct=edge_pct,
                roi_pct=roi_pct,
                kelly_fraction=kf,
                allocation_hkd=0.0,
                expected_return_hkd=0.0,
                risk_score=risk_score,
                explanation=explanation,
            ))

        # ---- b. Filter to positive-edge positions only ----
        positive = [c for c in candidates if c.edge_pct > 0]
        if not positive:
            return PortfolioResult(
                positions=[],
                total_allocation=0.0,
                total_expected_return=0.0,
                portfolio_roi=0.0,
                risk_level="Low",
                top_picks=[],
            )

        # ---- c. Cap any single position at 25 % of budget ----
        total_kelly = sum(c.kelly_fraction for c in positive)
        if total_kelly == 0:
            return PortfolioResult(
                positions=[],
                total_allocation=0.0,
                total_expected_return=0.0,
                portfolio_roi=0.0,
                risk_level="Low",
                top_picks=[],
            )

        for c in positive:
            raw_alloc = (c.kelly_fraction / total_kelly) * budget_hkd
            capped_alloc = min(raw_alloc, self.MAX_POSITION_PCT * budget_hkd)
            c.allocation_hkd = round(capped_alloc, 2)

        # Re-normalise if capping reduced total below budget
        total_allocated = sum(c.allocation_hkd for c in positive)
        if total_allocated > budget_hkd:
            scale = budget_hkd / total_allocated
            for c in positive:
                c.allocation_hkd = round(c.allocation_hkd * scale, 2)
            total_allocated = sum(c.allocation_hkd for c in positive)

        # ---- d. Allocation is already proportional to Kelly (done above) ----

        # ---- e. Calculate expected return for each position ----
        for c in positive:
            c.expected_return_hkd = round(c.allocation_hkd * c.model_prob * c.market_odds, 2)

        # ---- f. Total portfolio expected return and ROI ----
        total_expected_return = sum(c.expected_return_hkd for c in positive)
        portfolio_roi = ((total_expected_return - total_allocated) / total_allocated * 100) if total_allocated > 0 else 0.0

        # Risk level based on weighted average risk score
        avg_risk = (
            sum(c.risk_score * c.allocation_hkd for c in positive) / total_allocated
            if total_allocated > 0
            else 0.0
        )
        if avg_risk < 0.5:
            risk_level = "Low"
        elif avg_risk < 1.0:
            risk_level = "Medium"
        else:
            risk_level = "High"

        # Sort by edge descending
        positive.sort(key=lambda c: c.edge_pct, reverse=True)
        top_picks = positive[:5]

        return PortfolioResult(
            positions=positive,
            total_allocation=round(total_allocated, 2),
            total_expected_return=round(total_expected_return, 2),
            portfolio_roi=round(portfolio_roi, 2),
            risk_level=risk_level,
            top_picks=top_picks,
        )


# ===================================================================
# Quick test
# ===================================================================

def quick_test() -> None:
    """Validate the optimizer with sample data."""
    budget = 1000.0

    positions = [
        {
            "group": "A",
            "position": "1st",
            "team": "Argentina",
            "market_odds": 2.50,
            "market_implied_prob": 0.40,
            "model_prob": 0.55,
        },
        {
            "group": "B",
            "position": "1st",
            "team": "France",
            "market_odds": 1.80,
            "market_implied_prob": 0.556,
            "model_prob": 0.50,
        },
        {
            "group": "C",
            "position": "2nd",
            "team": "Japan",
            "market_odds": 4.00,
            "market_implied_prob": 0.25,
            "model_prob": 0.35,
        },
    ]

    optimizer = PortfolioOptimizer()
    result = optimizer.optimize(budget, positions)

    # ---- Verify Kelly fractions ----
    kelly = KellyCriterion()
    for pos in positions:
        kf = kelly.kelly_fraction(pos["model_prob"], pos["market_odds"])
        expected_kf = (pos["model_prob"] * pos["market_odds"] - 1) / (pos["market_odds"] - 1)
        expected_kf = max(0.0, expected_kf)
        assert abs(kf - expected_kf) < 1e-9, (
            f"Kelly mismatch for {pos['team']}: got {kf}, expected {expected_kf}"
        )
    print("[PASS] Kelly fractions verified")

    # ---- Verify ROI calculations ----
    roi_calc = ROICalculator()
    for pos in positions:
        r = roi_calc.roi(pos["model_prob"], pos["market_odds"])
        expected_r = (pos["model_prob"] * pos["market_odds"] - 1) * 100
        assert abs(r - expected_r) < 1e-9, (
            f"ROI mismatch for {pos['team']}: got {r}, expected {expected_r}"
        )
    print("[PASS] ROI calculations verified")

    # ---- Verify 25 % cap ----
    max_alloc = budget * 0.25
    for pr in result.positions:
        assert pr.allocation_hkd <= max_alloc + 0.01, (
            f"Cap violated for {pr.team}: {pr.allocation_hkd} > {max_alloc}"
        )
    print("[PASS] 25% budget cap verified")

    # ---- Print results ----
    print(f"\nBudget: HKD {budget:.0f}")
    print(f"Total allocated: HKD {result.total_allocation:.2f}")
    print(f"Total expected return: HKD {result.total_expected_return:.2f}")
    print(f"Portfolio ROI: {result.portfolio_roi:.2f}%")
    print(f"Risk level: {result.risk_level}")
    print(f"Positions with edge: {len(result.positions)}")
    print()
    for pr in result.positions:
        print(
            f"  {pr.group} {pr.position} – {pr.team}: "
            f"edge={pr.edge_pct:.1f}%, ROI={pr.roi_pct:.1f}%, "
            f"Kelly={pr.kelly_fraction:.4f}, "
            f"alloc=HKD {pr.allocation_hkd:.2f}, "
            f"E[return]=HKD {pr.expected_return_hkd:.2f}, "
            f"risk={pr.risk_score:.3f}"
        )
        print(f"    EN: {pr.explanation['en']}")

    print("\nTop picks:")
    for tp in result.top_picks:
        print(f"  {tp.team} ({tp.group} {tp.position}) – edge {tp.edge_pct:.1f}%")

    print("\n[ALL TESTS PASSED]")


if __name__ == "__main__":
    quick_test()
