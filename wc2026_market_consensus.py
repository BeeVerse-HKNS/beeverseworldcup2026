"""
WC2026 Market Consensus Module
===============================
Provides market consensus data for WC2026 group stage (1st/2nd place per team per group).

Data sourced from UK bookmakers, June 2026. Includes:
  - Tournament winner decimal odds for all 48 teams
  - Derived 1st/2nd place probabilities per group
  - MarketConsensus class with 6-hour cache and Elo fallback
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
#  Import WC2026_GROUPS from formula_v11_emoglyph (with fallback)
# ---------------------------------------------------------------------------
try:
    from formula_v11_emoglyph import WC2026_GROUPS, ELO_RATINGS
except ImportError:
    WC2026_GROUPS: Dict[str, List[str]] = {
        "A": ["Mexico", "South Africa", "South Korea", "Czech Republic"],
        "B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
        "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
        "D": ["USA", "Paraguay", "Australia", "Turkey"],
        "E": ["Germany", "Curacao", "Ivory Coast", "Ecuador"],
        "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
        "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
        "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
        "I": ["France", "Senegal", "Iraq", "Norway"],
        "J": ["Argentina", "Algeria", "Austria", "Jordan"],
        "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
        "L": ["England", "Croatia", "Ghana", "Panama"],
    }
    ELO_RATINGS: Dict[str, float] = {
        "Spain": 2050, "France": 2040, "Argentina": 2020, "England": 1990,
        "Brazil": 1975, "Portugal": 1960, "Germany": 1940, "Netherlands": 1930,
        "Belgium": 1910, "Croatia": 1900, "Uruguay": 1870, "Colombia": 1850,
        "Switzerland": 1830, "USA": 1810, "Mexico": 1800, "Japan": 1790,
        "Morocco": 1780, "Senegal": 1770, "Australia": 1760, "Turkey": 1750,
        "Austria": 1740, "Sweden": 1730, "Ecuador": 1710, "Ivory Coast": 1700,
        "Ghana": 1690, "South Korea": 1660, "Paraguay": 1650, "Egypt": 1640,
        "Algeria": 1630, "Scotland": 1620, "Norway": 1610, "Czech Republic": 1600,
        "Iran": 1590, "Tunisia": 1580, "Panama": 1570, "Iraq": 1560,
        "Bosnia and Herzegovina": 1550, "Qatar": 1540, "Saudi Arabia": 1530,
        "Uzbekistan": 1520, "Jordan": 1510, "New Zealand": 1500, "Haiti": 1490,
        "DR Congo": 1480, "Cape Verde": 1470, "Curacao": 1460,
        "South Africa": 1540, "Canada": 1620,
    }

# ===================================================================
#  TOURNAMENT WINNER ODDS — UK bookmakers, June 2026
# ===================================================================

TOURNAMENT_WINNER_ODDS: Dict[str, float] = {
    "Spain": 5.50, "France": 6.00, "England": 7.50, "Brazil": 9.00,
    "Portugal": 9.00, "Argentina": 10.00, "Germany": 15.00, "Netherlands": 21.00,
    "Norway": 26.00, "Belgium": 34.00, "Colombia": 34.00, "Japan": 51.00,
    "Morocco": 51.00, "USA": 67.00, "Uruguay": 67.00, "Mexico": 67.00,
    "Switzerland": 81.00, "Croatia": 81.00, "Turkey": 81.00, "Ecuador": 101.00,
    "Senegal": 126.00, "Sweden": 126.00, "Canada": 126.00, "Austria": 151.00,
    "Paraguay": 151.00, "Scotland": 251.00, "Ivory Coast": 301.00,
    "Egypt": 301.00, "Czech Republic": 301.00, "Bosnia and Herzegovina": 351.00,
    "Ghana": 401.00, "Algeria": 401.00, "South Korea": 401.00,
    "Tunisia": 501.00, "Australia": 501.00, "Iran": 501.00,
    "DR Congo": 751.00, "South Africa": 1001.00, "Saudi Arabia": 1001.00,
    "Panama": 1501.00, "Iraq": 1501.00, "Uzbekistan": 1501.00,
    "Qatar": 2001.00, "Cape Verde": 2001.00, "New Zealand": 2501.00,
    "Jordan": 2501.00, "Haiti": 2501.00, "Curacao": 3501.00,
}

# ===================================================================
#  BOOKMAKER MARGIN
# ===================================================================

BOOKMAKER_MARGIN = 0.08  # Typical ~8% vigorish
MARGIN_FACTOR = 1.0 - BOOKMAKER_MARGIN  # 0.92 — multiply raw odds by this

# ===================================================================
#  CACHE SETTINGS
# ===================================================================

_CACHE_TTL_SECONDS = 6 * 60 * 60  # 6 hours
_cache: Dict[str, Tuple[float, dict]] = {}  # key → (timestamp, data)
_last_updated: str = "2026-06-10T12:00:00Z"

# ===================================================================
#  DERIVATION HELPERS
# ===================================================================


def _implied_probability(odds: float) -> float:
    """Convert decimal odds to implied probability (raw, includes margin)."""
    return 1.0 / odds


def _compute_group_probabilities(
    teams: List[str],
    odds_dict: Dict[str, float],
) -> Dict[str, Dict[str, float]]:
    """
    Derive 1st and 2nd place probabilities for a 4-team group from
    tournament-winner odds.

    Method:
      1. Convert each team's tournament-winner odds to implied probability.
      2. Compute relative strength within the group.
      3. 1st place probability ≈ relative_strength (with dominance boost).
      4. 2nd place probability via conditional: P(team 2nd) =
         Σ_{other} P(other 1st) × P(team best of remaining).
      5. Apply margin factor to derived odds.
    """
    # Step 1 — raw implied probabilities from tournament-winner odds
    raw_probs = {}
    for t in teams:
        odds = odds_dict.get(t)
        if odds and odds > 1.0:
            raw_probs[t] = _implied_probability(odds)
        else:
            # Fallback: derive from Elo ratings
            elo = ELO_RATINGS.get(t, 1500)
            raw_probs[t] = 10.0 ** ((elo - 1500) / 400.0) / 1000.0

    # Step 2 — relative strength (normalise within group)
    total = sum(raw_probs.values())
    rel_strength = {t: p / total for t, p in raw_probs.items()}

    # Step 3 — 1st place probability
    # Apply a dominance boost: if a team's relative strength exceeds the
    # uniform baseline (0.25), boost it slightly to reflect group-stage
    # consistency advantages.
    first_prob: Dict[str, float] = {}
    for t in teams:
        rs = rel_strength[t]
        if rs > 0.25:
            boost = 1.0 + 0.08 * (rs - 0.25) / 0.75  # up to ~8% boost
        else:
            boost = 1.0
        first_prob[t] = rs * boost

    # Re-normalise 1st place probabilities
    fp_total = sum(first_prob.values())
    first_prob = {t: p / fp_total for t, p in first_prob.items()}

    # Step 4 — 2nd place probability (conditional)
    # P(team_i 2nd) = Σ_{j≠i} P(j 1st) × P(i best of remaining | j 1st)
    second_prob: Dict[str, float] = {t: 0.0 for t in teams}
    for t_first in teams:
        p_first = first_prob[t_first]
        remaining = [t for t in teams if t != t_first]
        # Among remaining, relative strength determines who is "best"
        rem_total = sum(rel_strength[t] for t in remaining)
        for t_second in remaining:
            p_best_of_remaining = rel_strength[t_second] / rem_total
            second_prob[t_second] += p_first * p_best_of_remaining

    # Re-normalise 2nd place probabilities
    sp_total = sum(second_prob.values())
    if sp_total > 0:
        second_prob = {t: p / sp_total for t, p in second_prob.items()}

    # Step 5 — apply bookmaker margin to derived odds
    result: Dict[str, Dict[str, float]] = {}
    for t in teams:
        fp = first_prob[t]
        sp = second_prob[t]
        # Raw odds (no margin)
        raw_first_odds = 1.0 / fp if fp > 0 else 999.0
        raw_second_odds = 1.0 / sp if sp > 0 else 999.0
        # Apply margin — multiply raw odds by MARGIN_FACTOR (0.92)
        first_odds = max(1.01, raw_first_odds * MARGIN_FACTOR)
        second_odds = max(1.01, raw_second_odds * MARGIN_FACTOR)
        result[t] = {
            "1st_prob": round(fp, 4),
            "2nd_prob": round(sp, 4),
            "1st_odds": round(first_odds, 2),
            "2nd_odds": round(second_odds, 2),
        }
    return result


def _build_group_consensus_baseline() -> Dict[str, Dict[str, Dict[str, float]]]:
    """Build GROUP_CONSENSUS_BASELINE for all 12 groups."""
    baseline: Dict[str, Dict[str, Dict[str, float]]] = {}
    for group_name, teams in WC2026_GROUPS.items():
        baseline[group_name] = _compute_group_probabilities(teams, TOURNAMENT_WINNER_ODDS)
    return baseline


# ===================================================================
#  GROUP CONSENSUS BASELINE — pre-computed from tournament winner odds
# ===================================================================

GROUP_CONSENSUS_BASELINE: Dict[str, Dict[str, Dict[str, float]]] = _build_group_consensus_baseline()


# ===================================================================
#  MarketConsensus Class
# ===================================================================


class MarketConsensus:
    """
    Provides market-consensus 1st/2nd place probabilities and odds for
    each team in each WC2026 group.

    Features:
      - 6-hour cache to avoid redundant recomputation
      - Fallback to Elo-derived estimates if odds data unavailable
    """

    def __init__(self, ttl_seconds: int = _CACHE_TTL_SECONDS) -> None:
        self._ttl = ttl_seconds

    # ------------------------------------------------------------------
    #  Cache helpers
    # ------------------------------------------------------------------

    def _is_cache_valid(self, key: str) -> bool:
        if key not in _cache:
            return False
        ts, _ = _cache[key]
        return (time.time() - ts) < self._ttl

    def _set_cache(self, key: str, data: dict) -> None:
        _cache[key] = (time.time(), data)

    def _get_cache(self, key: str) -> Optional[dict]:
        if self._is_cache_valid(key):
            return _cache[key][1]
        return None

    # ------------------------------------------------------------------
    #  Margin removal
    # ------------------------------------------------------------------

    @staticmethod
    def remove_margin(raw_odds_list: List[float]) -> List[float]:
        """
        Remove bookmaker margin (vigorish) from a list of raw decimal odds.

        Method: convert each odd to implied probability, sum them,
        then normalise so probabilities sum to 1.0.

        Returns a list of normalised probabilities (same order as input).
        """
        implied = [1.0 / o for o in raw_odds_list if o > 0]
        total = sum(implied)
        if total == 0:
            return [0.0] * len(raw_odds_list)
        return [p / total for p in implied]

    # ------------------------------------------------------------------
    #  Elo-derived fallback
    # ------------------------------------------------------------------

    @staticmethod
    def _elo_fallback(group_name: str) -> Dict[str, Dict[str, float]]:
        """
        Generate 1st/2nd place estimates from Elo ratings when market
        odds are unavailable.
        """
        teams = WC2026_GROUPS.get(group_name, [])
        if not teams:
            return {}

        # Convert Elo to win expectancy within the group
        elo_scores = {t: ELO_RATINGS.get(t, 1500) for t in teams}
        # Use 10^((elo-1500)/400) as a strength proxy
        strength = {t: 10.0 ** ((e - 1500) / 400.0) for t, e in elo_scores.items()}
        total_s = sum(strength.values())

        first_prob = {t: strength[t] / total_s for t in teams}

        # 2nd place: conditional on each other team being 1st
        second_prob: Dict[str, float] = {t: 0.0 for t in teams}
        for t_first in teams:
            p_first = first_prob[t_first]
            remaining = [t for t in teams if t != t_first]
            rem_total = sum(strength[t] for t in remaining)
            for t_second in remaining:
                second_prob[t_second] += p_first * (strength[t_second] / rem_total)

        sp_total = sum(second_prob.values())
        if sp_total > 0:
            second_prob = {t: p / sp_total for t, p in second_prob.items()}

        result: Dict[str, Dict[str, float]] = {}
        for t in teams:
            fp = first_prob[t]
            sp = second_prob[t]
            raw_first_odds = 1.0 / fp if fp > 0 else 999.0
            raw_second_odds = 1.0 / sp if sp > 0 else 999.0
            result[t] = {
                "1st_prob": round(fp, 4),
                "2nd_prob": round(sp, 4),
                "1st_odds": round(max(1.01, raw_first_odds * MARGIN_FACTOR), 2),
                "2nd_odds": round(max(1.01, raw_second_odds * MARGIN_FACTOR), 2),
            }
        return result

    # ------------------------------------------------------------------
    #  Public API
    # ------------------------------------------------------------------

    def fetch_group_consensus(self, group_name: str) -> Dict[str, Dict[str, float]]:
        """
        Fetch market consensus for a single group.

        Returns:
            dict of team → {
                "1st_prob": float,
                "2nd_prob": float,
                "1st_odds": float,
                "2nd_odds": float,
            }
        """
        cache_key = f"group_{group_name}"
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached

        # Try baseline data first
        data = GROUP_CONSENSUS_BASELINE.get(group_name)
        if data is None:
            # Fallback to Elo-derived estimates
            data = self._elo_fallback(group_name)

        self._set_cache(cache_key, data)
        return data

    def fetch_all_groups_consensus(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        """
        Fetch market consensus for all 12 groups.

        Returns:
            dict of group_name → group_consensus_data
        """
        cache_key = "all_groups"
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached

        result: Dict[str, Dict[str, Dict[str, float]]] = {}
        for group_name in WC2026_GROUPS:
            result[group_name] = self.fetch_group_consensus(group_name)

        self._set_cache(cache_key, result)
        return result

    def get_last_updated(self) -> str:
        """Return ISO 8601 timestamp of when the baseline data was last updated."""
        return _last_updated


# ===================================================================
#  Quick Test
# ===================================================================


def quick_test() -> bool:
    """
    Validate the module's data integrity:
      - All 12 groups have data
      - All 48 teams have 1st and 2nd place probabilities
      - Probabilities sum to approximately 1.0 per group per position
      - All odds are > 1.0
    """
    mc = MarketConsensus()
    all_data = mc.fetch_all_groups_consensus()
    errors: List[str] = []

    # Check all 12 groups present
    if len(all_data) != 12:
        errors.append(f"Expected 12 groups, got {len(all_data)}")

    total_teams = 0
    for group_name, teams_data in all_data.items():
        group_teams = WC2026_GROUPS.get(group_name, [])
        total_teams += len(teams_data)

        # Check all teams in group have data
        for team in group_teams:
            if team not in teams_data:
                errors.append(f"Group {group_name}: missing data for {team}")
                continue

            td = teams_data[team]

            # Check required keys
            for key in ("1st_prob", "2nd_prob", "1st_odds", "2nd_odds"):
                if key not in td:
                    errors.append(f"Group {group_name}, {team}: missing key '{key}'")

            # Check odds > 1.0
            if td.get("1st_odds", 0) <= 1.0:
                errors.append(f"Group {group_name}, {team}: 1st_odds <= 1.0 ({td.get('1st_odds')})")
            if td.get("2nd_odds", 0) <= 1.0:
                errors.append(f"Group {group_name}, {team}: 2nd_odds <= 1.0 ({td.get('2nd_odds')})")

        # Check probabilities sum ≈ 1.0 per position
        if teams_data:
            sum_1st = sum(td.get("1st_prob", 0) for td in teams_data.values())
            sum_2nd = sum(td.get("2nd_prob", 0) for td in teams_data.values())
            if abs(sum_1st - 1.0) > 0.02:
                errors.append(f"Group {group_name}: 1st_prob sum = {sum_1st:.4f} (expected ~1.0)")
            if abs(sum_2nd - 1.0) > 0.02:
                errors.append(f"Group {group_name}: 2nd_prob sum = {sum_2nd:.4f} (expected ~1.0)")

    # Check all 48 teams covered
    if total_teams != 48:
        errors.append(f"Expected 48 teams, got {total_teams}")

    # Check last_updated is valid
    last_updated = mc.get_last_updated()
    if not last_updated:
        errors.append("get_last_updated() returned empty string")

    if errors:
        print("QUICK TEST FAILED — errors:")
        for e in errors:
            print(f"  - {e}")
        return False

    print("QUICK TEST PASSED — all 12 groups, 48 teams validated.")
    print(f"  Last updated: {mc.get_last_updated()}")
    return True


if __name__ == "__main__":
    quick_test()
