"""
WC2026 Group Stage Combination Engine
======================================

Models ALL possible group stage outcomes for each team in the
World Cup 2026 format (48 teams, 12 groups of 4).

Each team plays 3 matches → 16 possible result patterns (W/D/L).
The engine calculates pattern probabilities via Elo-based match
probabilities and derives strategic recommendations including:

  - Six-points-after-two detection (structural rotation advantage)
  - Must-win match-3 detection
  - Tri-lingual strategic recommendations (EN / 簡中 / 繁中)
  - Third-place rankings across all 12 groups
  - Third-place advancement probability
  - R32 opponent projection for third-place qualifiers

Usage:
    from wc2026_group_combinations import GroupCombinationEngine, quick_test

    engine = GroupCombinationEngine()
    combos = engine.generate_team_combinations("France")
    engine.quick_test()

Dependencies:
    - formula_v11_emoglyph (WC2026_GROUPS, ELO_RATINGS, GROUP_STRENGTH_DATA,
      COACH_STYLES_2026)
"""

import math
from itertools import product
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Import with fallback
# ---------------------------------------------------------------------------
try:
    from formula_v11_emoglyph import (
        WC2026_GROUPS,
        ELO_RATINGS,
        GROUP_STRENGTH_DATA,
        COACH_STYLES_2026,
    )
    _HAS_FORMULA_V11 = True
except ImportError:
    _HAS_FORMULA_V11 = False
    WC2026_GROUPS = {}  # type: ignore[assignment]
    ELO_RATINGS = {}  # type: ignore[assignment]
    GROUP_STRENGTH_DATA = {}  # type: ignore[assignment]
    COACH_STYLES_2026 = {}  # type: ignore[assignment]


# ===================================================================
#  CONSTANTS — 16 result patterns for 3 matches
# ===================================================================

RESULT_PATTERNS: Dict[str, Dict[str, Any]] = {
    "WWW": {"points": 9, "implication": "Guaranteed 1st, full rotation in match 3"},
    "WWL": {"points": 6, "implication": "Likely 1st or 2nd, rotation possible in match 3 if 6pts secured"},
    "WWD": {"points": 7, "implication": "Guaranteed top 2, rotation possible in match 3"},
    "WW-": {"points": 6, "implication": "KEY: Can rest in match 3 (structural advantage!)"},
    "WLW": {"points": 6, "implication": "Recovered from loss, likely 2nd"},
    "WLD": {"points": 4, "implication": "Borderline, match 3 is must-not-lose"},
    "WDL": {"points": 4, "implication": "Borderline, match 3 is must-win"},
    "WDD": {"points": 5, "implication": "Likely 2nd or 3rd"},
    "LWW": {"points": 6, "implication": "Recovered from loss, likely 2nd"},
    "LWL": {"points": 3, "implication": "Dangerous, must win match 3"},
    "LWD": {"points": 4, "implication": "Borderline"},
    "LDW": {"points": 4, "implication": "Borderline"},
    "LDL": {"points": 1, "implication": "Likely eliminated"},
    "LDD": {"points": 2, "implication": "Need help from other results"},
    "DLL": {"points": 1, "implication": "Eliminated"},
    "DDD": {"points": 3, "implication": "3rd place candidate (goal difference matters!)"},
}

# Points per result
POINTS = {"W": 3, "D": 1, "L": 0}

# R32 bracket mapping: 3rd-place team from group → opponent group winner
THIRD_PLACE_R32_BRACKET: Dict[str, str] = {
    "A": "B",  # 3rd A → plays Group B winner
    "C": "D",  # 3rd C → plays Group D winner
    "E": "F",  # 3rd E → plays Group F winner
    "G": "H",  # 3rd G → plays Group H winner
    "I": "J",  # 3rd I → plays Group J winner
    "K": "L",  # 3rd K → plays Group L winner
    "B": "A",  # 3rd B → plays Group A winner
    "D": "C",  # 3rd D → plays Group C winner
}

# Third-place advancement probability lookup by (points, GD sign)
THIRD_PLACE_ADV_PROB: Dict[Tuple[int, str], float] = {
    (4, "positive"): 0.90,
    (4, "zero"): 0.75,
    (4, "negative"): 0.60,
    (3, "positive"): 0.50,
    (3, "zero"): 0.35,
    (3, "negative"): 0.20,
    (2, "any"): 0.05,
    (1, "any"): 0.01,
    (0, "any"): 0.00,
}


# ===================================================================
#  GROUP COMBINATION ENGINE
# ===================================================================

class GroupCombinationEngine:
    """Group Stage Combination Engine for WC2026 (48 teams, 12 groups of 4)."""

    def __init__(self) -> None:
        if not _HAS_FORMULA_V11:
            raise ImportError(
                "formula_v11_emoglyph is required. "
                "Ensure it is importable from the same directory."
            )
        self.groups: Dict[str, List[str]] = WC2026_GROUPS
        self.elo: Dict[str, float] = ELO_RATINGS
        self.group_strength: Dict[str, Dict[str, Any]] = GROUP_STRENGTH_DATA
        self.coach_styles: Dict[str, Dict[str, Any]] = COACH_STYLES_2026

    # ------------------------------------------------------------------
    #  Helpers
    # ------------------------------------------------------------------

    def _find_group(self, team: str) -> Optional[str]:
        """Return the group letter for a team, or None."""
        for group_id, teams in self.groups.items():
            if team in teams:
                return group_id
        return None

    def _get_opponents(self, team: str) -> List[str]:
        """Return the 3 group opponents for a team."""
        group_id = self._find_group(team)
        if group_id is None:
            return []
        return [t for t in self.groups[group_id] if t != team]

    def _elo_win_prob(self, team_elo: float, opp_elo: float) -> float:
        """Elo-based win probability: P(win) = 1 / (1 + 10^((opp_elo - team_elo)/400))"""
        return 1.0 / (1.0 + 10.0 ** ((opp_elo - team_elo) / 400.0))

    def _match_probabilities(self, team: str, opponent: str) -> Dict[str, float]:
        """Calculate P(W), P(D), P(L) for a single match.

        Draw probability: base 0.25, adjusted by Elo closeness.
        When teams are close in Elo, draws are more likely.
        When there's a large gap, draws are less likely.
        """
        team_elo = self.elo.get(team, 1500)
        opp_elo = self.elo.get(opponent, 1500)
        elo_diff = abs(team_elo - opp_elo)

        # Base draw prob 0.25; reduce as elo_diff grows
        # At diff=200, draw ≈ 0.20; at diff=400, draw ≈ 0.15
        draw_prob = max(0.10, 0.25 - (elo_diff / 400.0) * 0.10)

        raw_win = self._elo_win_prob(team_elo, opp_elo)
        raw_lose = self._elo_win_prob(opp_elo, team_elo)

        # Normalize win/lose to fill the remaining probability
        remaining = 1.0 - draw_prob
        total_raw = raw_win + raw_lose
        if total_raw == 0:
            win_prob = remaining / 2.0
            lose_prob = remaining / 2.0
        else:
            win_prob = remaining * (raw_win / total_raw)
            lose_prob = remaining * (raw_lose / total_raw)

        return {"W": win_prob, "D": draw_prob, "L": lose_prob}

    def _estimate_goal_difference(self, team: str, opponent: str) -> float:
        """Estimate expected goal difference for a single match.

        Formula: (elo_diff / 400) * 0.5
        Positive means team is expected to outscore opponent.
        """
        team_elo = self.elo.get(team, 1500)
        opp_elo = self.elo.get(opponent, 1500)
        return (team_elo - opp_elo) / 400.0 * 0.5

    def _pattern_points(self, pattern: str) -> int:
        """Calculate total points for a result pattern."""
        return sum(POINTS.get(c, 0) for c in pattern)

    # ------------------------------------------------------------------
    #  1. generate_team_combinations
    # ------------------------------------------------------------------

    def generate_team_combinations(self, team: str) -> Dict[str, float]:
        """For a given team, calculate the probability of each result pattern.

        Returns dict mapping pattern string (e.g. 'WWW', 'WLD') → probability.
        The special 'WW-' pattern is reported separately as the probability
        of having 6 points after 2 matches (WW in first two games).
        """
        opponents = self._get_opponents(team)
        if len(opponents) != 3:
            return {}

        # Per-match probabilities (match order: opp[0], opp[1], opp[2])
        match_probs = [self._match_probabilities(team, opp) for opp in opponents]

        # Enumerate all 27 possible outcomes (3^3)
        outcomes = list(product(["W", "D", "L"], repeat=3))

        pattern_probs: Dict[str, float] = {}
        six_points_after_two = 0.0

        for outcome in outcomes:
            prob = 1.0
            for i, result in enumerate(outcome):
                prob *= match_probs[i][result]

            pattern = "".join(outcome)
            pattern_probs[pattern] = prob

            # Track WW after 2 matches
            if outcome[0] == "W" and outcome[1] == "W":
                six_points_after_two += prob

        # Add the special WW- pattern (probability of having 6 pts after 2)
        pattern_probs["WW-"] = six_points_after_two

        return pattern_probs

    # ------------------------------------------------------------------
    #  2. detect_six_points_after_two
    # ------------------------------------------------------------------

    def detect_six_points_after_two(self, team: str) -> Dict[str, Any]:
        """Check if team is likely to have 6 points after 2 matches.

        Returns dict with:
          - probability: P(6 points after match 2)
          - strategic_implication: what this means for rotation
        """
        combos = self.generate_team_combinations(team)
        prob = combos.get("WW-", 0.0)

        group_id = self._find_group(team)
        early_secure = 0.0
        if group_id and group_id in self.group_strength:
            early_secure = self.group_strength[group_id].get("early_secure_prob", 0.0)

        if prob >= 0.50:
            implication = (
                f"High probability ({prob:.0%}) of 6 pts after 2 matches. "
                f"Coach can rotate squad in match 3 — major structural advantage "
                f"for knockout preparation."
            )
        elif prob >= 0.25:
            implication = (
                f"Moderate probability ({prob:.0%}) of 6 pts after 2 matches. "
                f"Rotation is possible but not guaranteed; match 3 may still matter."
            )
        else:
            implication = (
                f"Low probability ({prob:.0%}) of 6 pts after 2 matches. "
                f"Every match counts — rotation unlikely."
            )

        return {
            "team": team,
            "probability": prob,
            "early_secure_group_rate": early_secure,
            "strategic_implication": implication,
        }

    # ------------------------------------------------------------------
    #  3. detect_must_win_match3
    # ------------------------------------------------------------------

    def detect_must_win_match3(self, team: str) -> Dict[str, Any]:
        """Check if team faces a must-win scenario in match 3.

        Must-win after 2 matches: LW (3 pts), WL (3 pts), LD (1 pt).
        Must-not-lose: WD (4 pts borderline), DD (2 pts).

        Returns dict with probability and which scenarios create must-win.
        """
        combos = self.generate_team_combinations(team)
        opponents = self._get_opponents(team)

        # Must-win scenarios (need a win in match 3 to have realistic chance)
        must_win_patterns = {
            "LWW": "After LW, must win match 3 vs " + (opponents[2] if len(opponents) > 2 else "?"),
            "WLW": "After WL, must win match 3 vs " + (opponents[2] if len(opponents) > 2 else "?"),
            "LDW": "After LD, must win match 3 vs " + (opponents[2] if len(opponents) > 2 else "?"),
        }

        # Must-not-lose scenarios (draw is acceptable, loss is not)
        must_not_lose_patterns = {
            "WWD": "After WW, draw is fine but win seals top",
            "WDD": "After WD, must not lose match 3",
            "LDD": "After LD, must not lose match 3",
        }

        must_win_prob = sum(combos.get(p, 0.0) for p in must_win_patterns)
        must_not_lose_prob = sum(combos.get(p, 0.0) for p in must_not_lose_patterns)

        # Determine which match-3 opponent
        match3_opp = opponents[2] if len(opponents) > 2 else "Unknown"

        return {
            "team": team,
            "must_win_probability": must_win_prob,
            "must_not_lose_probability": must_not_lose_prob,
            "match3_opponent": match3_opp,
            "must_win_scenarios": {
                pattern: {
                    "probability": combos.get(pattern, 0.0),
                    "description": desc,
                }
                for pattern, desc in must_win_patterns.items()
            },
            "must_not_lose_scenarios": {
                pattern: {
                    "probability": combos.get(pattern, 0.0),
                    "description": desc,
                }
                for pattern, desc in must_not_lose_patterns.items()
            },
        }

    # ------------------------------------------------------------------
    #  4. project_strategic_recommendation
    # ------------------------------------------------------------------

    def project_strategic_recommendation(self, team: str, language: str = "en") -> str:
        """Return tri-lingual strategic recommendation based on most likely pattern.

        language: 'en', 'zh_cn', 'zh_tw'
        """
        combos = self.generate_team_combinations(team)
        if not combos:
            return "Team not found in group data."

        # Find most likely pattern (excluding WW- which is a meta-pattern)
        actual_combos = {k: v for k, v in combos.items() if k != "WW-"}
        most_likely = max(actual_combos, key=actual_combos.get)
        most_likely_prob = actual_combos[most_likely]
        points = self._pattern_points(most_likely)

        six_pts = self.detect_six_points_after_two(team)
        must_win = self.detect_must_win_match3(team)

        group_id = self._find_group(team) or "?"

        # Build recommendation based on pattern category
        recommendations: Dict[str, Dict[str, str]] = {
            "WWW": {
                "en": (
                    f"{team} (Group {group_id}): Dominant — 9 points expected. "
                    f"Full squad rotation in match 3 is the key strategic move. "
                    f"Rest key players, protect cards, prepare for R32."
                ),
                "zh_cn": (
                    f"{team}（{group_id}组）：统治级表现——预计9分。 "
                    f"第三场全面轮换是关键战略。休息核心球员，避免黄牌停赛，为32强做准备。"
                ),
                "zh_tw": (
                    f"{team}（{group_id}組）：統治級表現——預計9分。 "
                    f"第三場全面輪換是關鍵戰略。休息核心球員，避免黃牌停賽，為32強做準備。"
                ),
            },
            "dominant_6_7": {
                "en": (
                    f"{team} (Group {group_id}): Strong — {points} points expected. "
                    f"Likely top 2 finish. Rotation possible in match 3 if 6+ points secured early. "
                    f"Six-points-after-two probability: {six_pts['probability']:.0%}."
                ),
                "zh_cn": (
                    f"{team}（{group_id}组）：强势——预计{points}分。 "
                    f"大概率前两名出线。若提前锁定6分，第三场可轮换。"
                    f"两轮6分概率：{six_pts['probability']:.0%}。"
                ),
                "zh_tw": (
                    f"{team}（{group_id}組）：強勢——預計{points}分。 "
                    f"大概率前兩名出線。若提前鎖定6分，第三場可輪換。"
                    f"兩輪6分概率：{six_pts['probability']:.0%}。"
                ),
            },
            "borderline_4_5": {
                "en": (
                    f"{team} (Group {group_id}): Borderline — {points} points expected. "
                    f"Match 3 is critical. Must-win probability: {must_win['must_win_probability']:.0%}. "
                    f"Coach must decide: go for win or play safe for draw."
                ),
                "zh_cn": (
                    f"{team}（{group_id}组）：边缘——预计{points}分。 "
                    f"第三场至关重要。必胜概率：{must_win['must_win_probability']:.0%}。"
                    f"教练需抉择：全力争胜还是保平求稳。"
                ),
                "zh_tw": (
                    f"{team}（{group_id}組）：邊緣——預計{points}分。 "
                    f"第三場至關重要。必勝概率：{must_win['must_win_probability']:.0%}。"
                    f"教練需抉擇：全力爭勝還是保平求穩。"
                ),
            },
            "danger_1_3": {
                "en": (
                    f"{team} (Group {group_id}): Danger zone — {points} points expected. "
                    f"Likely eliminated or needing help. Must-win probability: {must_win['must_win_probability']:.0%}. "
                    f"Every match is a final."
                ),
                "zh_cn": (
                    f"{team}（{group_id}组）：危险区——预计{points}分。 "
                    f"大概率淘汰或需看别人脸色。必胜概率：{must_win['must_win_probability']:.0%}。"
                    f"每场都是生死战。"
                ),
                "zh_tw": (
                    f"{team}（{group_id}組）：危險區——預計{points}分。 "
                    f"大概率淘汰或需看別人臉色。必勝概率：{must_win['must_win_probability']:.0%}。"
                    f"每場都是生死戰。"
                ),
            },
        }

        # Select category
        if most_likely == "WWW":
            category = "WWW"
        elif points >= 6:
            category = "dominant_6_7"
        elif points >= 4:
            category = "borderline_4_5"
        else:
            category = "danger_1_3"

        lang_key = language if language in ("en", "zh_cn", "zh_tw") else "en"
        base_rec = recommendations[category][lang_key]

        # Append most likely pattern info
        pattern_info = RESULT_PATTERNS.get(most_likely, {})
        implication = pattern_info.get("implication", "")

        if lang_key == "en":
            suffix = (
                f"\n  Most likely pattern: {most_likely} ({most_likely_prob:.1%}) — {implication}"
            )
        elif lang_key == "zh_cn":
            suffix = (
                f"\n  最可能模式：{most_likely}（{most_likely_prob:.1%}）—— {implication}"
            )
        else:
            suffix = (
                f"\n  最可能模式：{most_likely}（{most_likely_prob:.1%}）—— {implication}"
            )

        return base_rec + suffix

    # ------------------------------------------------------------------
    #  5. project_third_place_rankings
    # ------------------------------------------------------------------

    def project_third_place_rankings(self) -> List[Dict[str, Any]]:
        """Simulate group stage outcomes for ALL 12 groups and rank 3rd-place teams.

        Tiebreakers:
          1. Points (primary)
          2. Goal difference (secondary) — estimated from opponent strength
          3. Goals scored (tertiary) — estimated from team's attacking strength

        Returns the top 8 3rd-place teams that advance to R32.
        """
        third_place_teams: List[Dict[str, Any]] = []

        for group_id, teams in self.groups.items():
            # For each team, compute expected group stage stats
            team_stats: List[Dict[str, Any]] = []

            for team in teams:
                opponents = [t for t in teams if t != team]
                combos = self.generate_team_combinations(team)

                # Expected points (weighted average across all patterns)
                expected_pts = 0.0
                for pattern, prob in combos.items():
                    if pattern == "WW-":
                        continue
                    expected_pts += self._pattern_points(pattern) * prob

                # Expected goal difference (sum across 3 matches)
                expected_gd = sum(
                    self._estimate_goal_difference(team, opp) for opp in opponents
                )

                # Expected goals scored — estimate from Elo and coach style
                team_elo = self.elo.get(team, 1500)
                coach_info = self.coach_styles.get(team, {})
                style = coach_info.get("style", "balanced")
                # Attacking styles score more
                style_bonus = {
                    "attacking": 1.3, "high_press": 1.15, "possession": 1.1,
                    "balanced": 1.0, "pragmatic": 0.95, "counter_attack": 1.05,
                    "defensive": 0.85,
                }.get(style, 1.0)

                # Base goals ≈ 1.0 + (elo - 1600)/800, scaled by style
                base_goals = max(0.5, 1.0 + (team_elo - 1600) / 800.0)
                expected_gf = base_goals * style_bonus * 3  # across 3 matches

                team_stats.append({
                    "team": team,
                    "group": group_id,
                    "expected_points": expected_pts,
                    "expected_gd": expected_gd,
                    "expected_gf": expected_gf,
                })

            # Sort by points, GD, GF to determine group positions
            team_stats.sort(
                key=lambda x: (x["expected_points"], x["expected_gd"], x["expected_gf"]),
                reverse=True,
            )

            # 3rd place team (index 2)
            if len(team_stats) >= 3:
                third = team_stats[2]
                third_place_teams.append(third)

        # Rank all 3rd-place teams by same criteria
        third_place_teams.sort(
            key=lambda x: (x["expected_points"], x["expected_gd"], x["expected_gf"]),
            reverse=True,
        )

        # Top 8 advance
        for i, entry in enumerate(third_place_teams):
            entry["third_place_rank"] = i + 1
            entry["advances"] = i < 8

        return third_place_teams

    # ------------------------------------------------------------------
    #  6. project_third_place_advancement_probability
    # ------------------------------------------------------------------

    def project_third_place_advancement_probability(self, team: str) -> Dict[str, Any]:
        """Calculate the probability a team advances as a 3rd-place team.

        Based on points + goal difference thresholds:
          - 4 pts + positive GD: Very likely (90%+)
          - 4 pts + negative GD: Possible (60%)
          - 3 pts + positive GD: Possible (50%)
          - 3 pts + negative GD: Unlikely (20%)
          - 2 pts: Very unlikely (5%)
        """
        combos = self.generate_team_combinations(team)
        if not combos:
            return {"team": team, "advancement_probability": 0.0, "error": "Team not found"}

        opponents = self._get_opponents(team)
        expected_gd = sum(self._estimate_goal_difference(team, opp) for opp in opponents)

        # Weighted advancement probability across all patterns
        total_adv_prob = 0.0

        for pattern, prob in combos.items():
            if pattern == "WW-":
                continue

            pts = self._pattern_points(pattern)

            # Estimate GD contribution for this specific pattern
            # Each W adds ~0.7 GD, D adds ~0, L subtracts ~0.7 relative to expected
            pattern_gd = expected_gd
            for c in pattern:
                if c == "W":
                    pattern_gd += 0.7
                elif c == "L":
                    pattern_gd -= 0.7

            # Determine GD sign
            if pattern_gd > 0.5:
                gd_sign = "positive"
            elif pattern_gd < -0.5:
                gd_sign = "negative"
            else:
                gd_sign = "zero"

            # Look up advancement probability
            adv_prob = THIRD_PLACE_ADV_PROB.get((pts, gd_sign), None)
            if adv_prob is None:
                # Try fallback with "any"
                adv_prob = THIRD_PLACE_ADV_PROB.get((pts, "any"), 0.0)

            total_adv_prob += prob * adv_prob

        # Also compute: probability of finishing 3rd specifically
        # (not 1st or 2nd) — approximate from expected points
        group_id = self._find_group(team)
        group_teams = self.groups.get(group_id, [])
        team_elo = self.elo.get(team, 1500)

        # Rough estimate: probability of finishing 3rd based on relative Elo
        if group_teams:
            group_elos = sorted(
                [self.elo.get(t, 1500) for t in group_teams], reverse=True
            )
            rank = 1
            for i, elo in enumerate(group_elos):
                if abs(elo - team_elo) < 1:
                    rank = i + 1
                    break
            # Probability of being 3rd is higher if team is 3rd strongest
            p_third = max(0.05, 0.50 - abs(rank - 3) * 0.15)
        else:
            p_third = 0.25

        final_adv = total_adv_prob * p_third

        return {
            "team": team,
            "group": group_id,
            "expected_gd": expected_gd,
            "advancement_probability": min(1.0, final_adv),
            "third_place_finish_probability": p_third,
            "conditional_advancement_probability": total_adv_prob,
            "note": (
                f"P(advance) = P(finish 3rd) × P(3rd advances) = "
                f"{p_third:.2f} × {total_adv_prob:.2f} = {final_adv:.2f}"
            ),
        }

    # ------------------------------------------------------------------
    #  7. project_r32_opponent_for_third_place
    # ------------------------------------------------------------------

    def project_r32_opponent_for_third_place(self, team: str) -> Dict[str, Any]:
        """If team advances as 3rd place, project their R32 opponent.

        The 8 best 3rd-place teams are seeded into specific R32 slots
        based on which group they come from.
        """
        group_id = self._find_group(team)
        if group_id is None:
            return {"team": team, "error": "Team not found in any group"}

        # Check if this group's 3rd-place team has a bracket slot
        if group_id not in THIRD_PLACE_R32_BRACKET:
            return {
                "team": team,
                "group": group_id,
                "error": f"Group {group_id} 3rd-place team has no direct R32 bracket slot "
                         f"(only 8 of 12 groups' 3rd-place teams are slotted)",
            }

        opponent_group = THIRD_PLACE_R32_BRACKET[group_id]

        # Project the winner of the opponent group
        opp_group_teams = self.groups.get(opponent_group, [])
        if not opp_group_teams:
            return {"team": team, "group": group_id, "opponent_group": opponent_group, "error": "No teams found"}

        # Sort by Elo to estimate group winner
        opp_group_sorted = sorted(
            opp_group_teams,
            key=lambda t: self.elo.get(t, 1500),
            reverse=True,
        )
        projected_winner = opp_group_sorted[0]
        projected_runner_up = opp_group_sorted[1] if len(opp_group_sorted) > 1 else "Unknown"

        # Win probability vs projected winner
        team_elo = self.elo.get(team, 1500)
        winner_elo = self.elo.get(projected_winner, 1500)
        win_prob = self._elo_win_prob(team_elo, winner_elo)

        return {
            "team": team,
            "group": group_id,
            "bracket_slot": f"3rd {group_id}",
            "opponent_group": opponent_group,
            "projected_opponent": projected_winner,
            "projected_opponent_elo": winner_elo,
            "upset_probability": win_prob,
            "opponent_group_teams": opp_group_sorted,
            "r32_matchup": f"{team} (3rd {group_id}) vs {projected_winner} (1st {opponent_group})",
        }


# ===================================================================
#  QUICK TEST
# ===================================================================

def quick_test() -> None:
    """Test the GroupCombinationEngine with 3 representative teams."""
    engine = GroupCombinationEngine()

    test_teams = [
        ("France", "Group I, easy group — likely WW- pattern"),
        ("Croatia", "Group L, hard group — likely LW scenario"),
        ("Morocco", "Group C, medium — 3rd-place candidate"),
    ]

    print("=" * 72)
    print("  WC2026 GROUP STAGE COMBINATION ENGINE — QUICK TEST")
    print("=" * 72)

    for team, description in test_teams:
        print(f"\n{'─' * 72}")
        print(f"  {team} — {description}")
        print(f"{'─' * 72}")

        # 1. Combinations
        combos = engine.generate_team_combinations(team)
        print(f"\n  📊 Result Pattern Probabilities:")
        # Sort by probability descending
        sorted_combos = sorted(combos.items(), key=lambda x: x[1], reverse=True)
        for pattern, prob in sorted_combos:
            pts = engine._pattern_points(pattern) if pattern != "WW-" else 6
            marker = " ◄ MOST LIKELY" if prob == sorted_combos[0][1] else ""
            if pattern == "WW-":
                print(f"    {pattern}: {prob:.1%}  (6 pts after 2 matches){marker}")
            else:
                impl = RESULT_PATTERNS.get(pattern, {}).get("implication", "")
                print(f"    {pattern}: {prob:.1%}  ({pts} pts) — {impl}{marker}")

        # 2. Six points after two
        six = engine.detect_six_points_after_two(team)
        print(f"\n  🎯 Six-Points-After-Two Detection:")
        print(f"    Probability: {six['probability']:.1%}")
        print(f"    Early secure group rate: {six['early_secure_group_rate']:.1%}")
        print(f"    Implication: {six['strategic_implication']}")

        # 3. Must-win match 3
        must = engine.detect_must_win_match3(team)
        print(f"\n  ⚠️  Must-Win Match 3 Analysis:")
        print(f"    Must-win probability: {must['must_win_probability']:.1%}")
        print(f"    Must-not-lose probability: {must['must_not_lose_probability']:.1%}")
        print(f"    Match 3 opponent: {must['match3_opponent']}")
        if must['must_win_scenarios']:
            for p, info in must['must_win_scenarios'].items():
                if info['probability'] > 0.01:
                    print(f"      {p}: {info['probability']:.1%} — {info['description']}")

        # 4. Strategic recommendation (all 3 languages)
        print(f"\n  💡 Strategic Recommendations:")
        for lang, label in [("en", "English"), ("zh_cn", "简体中文"), ("zh_tw", "繁體中文")]:
            rec = engine.project_strategic_recommendation(team, language=lang)
            print(f"    [{label}]")
            for line in rec.split("\n"):
                print(f"      {line.strip()}")

        # 5. Third-place advancement probability
        adv = engine.project_third_place_advancement_probability(team)
        print(f"\n  🏆 Third-Place Advancement Probability:")
        print(f"    P(finish 3rd): {adv['third_place_finish_probability']:.1%}")
        print(f"    P(advance | 3rd): {adv['conditional_advancement_probability']:.1%}")
        print(f"    P(advance as 3rd): {adv['advancement_probability']:.1%}")
        print(f"    {adv['note']}")

        # 6. R32 opponent projection
        r32 = engine.project_r32_opponent_for_third_place(team)
        if "error" in r32:
            print(f"\n  🔄 R32 Opponent (if 3rd place): {r32.get('error', 'N/A')}")
        else:
            print(f"\n  🔄 R32 Opponent (if 3rd place):")
            print(f"    Matchup: {r32['r32_matchup']}")
            print(f"    Projected opponent: {r32['projected_opponent']} (Elo {r32['projected_opponent_elo']})")
            print(f"    Upset probability: {r32['upset_probability']:.1%}")

    # 7. Full third-place rankings
    print(f"\n{'=' * 72}")
    print(f"  THIRD-PLACE RANKINGS (ALL 12 GROUPS)")
    print(f"{'=' * 72}")

    rankings = engine.project_third_place_rankings()
    print(f"\n  {'Rank':<5} {'Team':<28} {'Group':<6} {'Pts':<6} {'GD':<7} {'GF':<6} {'Advances'}")
    print(f"  {'─'*5} {'─'*28} {'─'*6} {'─'*6} {'─'*7} {'─'*6} {'─'*8}")

    for entry in rankings:
        adv_marker = "✅ YES" if entry["advances"] else "❌ NO"
        print(
            f"  {entry['third_place_rank']:<5} "
            f"{entry['team']:<28} "
            f"{entry['group']:<6} "
            f"{entry['expected_points']:<6.1f} "
            f"{entry['expected_gd']:<+7.2f} "
            f"{entry['expected_gf']:<6.1f} "
            f"{adv_marker}"
        )

    print(f"\n  Top 8 3rd-place teams advance to Round of 32.")

    print(f"\n{'=' * 72}")
    print(f"  QUICK TEST COMPLETE")
    print(f"{'=' * 72}")


if __name__ == "__main__":
    quick_test()
