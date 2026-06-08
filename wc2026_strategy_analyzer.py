"""
WC2026 R32 Knockout Strategy Analyzer — Based on Formula V11.1
==============================================================

Provides detailed strategy analysis for each Round of 32 knockout match,
leveraging the FormulaV11Engine's 16-dimension scoring and 3-engine
fusion (LightDarkBalance, SunTzu, Pratitya) to produce:

  - Key factor identification (which dimension decides the match)
  - Per-team strategy recommendations (depth, heat, X-factor, coaching)
  - Upset potential analysis (LightDarkBalance-driven)
  - X-factor player watch lists
  - Full R32 bracket analysis with markdown reports

Usage:
    from wc2026_strategy_analyzer import WC2026StrategyAnalyzer, quick_test

    analyzer = WC2026StrategyAnalyzer()
    report = analyzer.analyze_match("France", "Brazil")
    print(report)

    # Full R32 report
    markdown = analyzer.generate_report()

Dependencies:
    - formula_v11_emoglyph (FormulaV11Engine, WC2026_GROUPS, and data dicts)
    - No external dependencies beyond standard library
"""

from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Import with fallback — engine works in degraded mode without formula_v11
# ---------------------------------------------------------------------------
try:
    from formula_v11_emoglyph import (
        FormulaV11Engine,
        WC2026_GROUPS,
        COACH_STYLES_2026,
        SQUAD_DEPTH_DATA,
        XFACTOR_DATA,
    )
    _HAS_FORMULA_V11 = True
except ImportError:
    _HAS_FORMULA_V11 = False
    FormulaV11Engine = None  # type: ignore[assignment, misc]
    WC2026_GROUPS = {}  # type: ignore[assignment]
    COACH_STYLES_2026 = {}  # type: ignore[assignment]
    SQUAD_DEPTH_DATA = {}  # type: ignore[assignment]
    XFACTOR_DATA = {}  # type: ignore[assignment]


__all__ = [
    "WC2026StrategyAnalyzer",
    "quick_test",
]


class WC2026StrategyAnalyzer:
    """32強淘汰賽策略分析器 — 基於 Formula V11.1"""

    def __init__(self) -> None:
        if not _HAS_FORMULA_V11:
            raise ImportError(
                "formula_v11_emoglyph is required for WC2026StrategyAnalyzer. "
                "Ensure it is importable from the same directory."
            )
        self.engine: FormulaV11Engine = FormulaV11Engine()
        self.groups: Dict[str, List[str]] = WC2026_GROUPS

    # ------------------------------------------------------------------
    #  Public API
    # ------------------------------------------------------------------

    def analyze_match(self, team_a: str, team_b: str, match_context: Optional[dict] = None) -> dict:
        """Analyze a single knockout match with full breakdown"""
        if match_context is None:
            match_context = {"venue_id": "dallas", "match_time": "afternoon", "stage": "r32", "match_number": 4}

        # Get full prediction
        prediction = self.engine.predict_match(team_a, team_b, match_context)

        # Key factor analysis — which dimension decides the match
        key_factors = self._identify_key_factors(prediction)

        # Strategy recommendations
        strategy_a = self._recommend_strategy(team_a, team_b, prediction)
        strategy_b = self._recommend_strategy(team_b, team_a, prediction)

        # Upset potential
        upset_analysis = self._analyze_upset_potential(prediction)

        # X-factor players to watch
        xfactor_watch = self._identify_xfactor_players(team_a, team_b)

        return {
            "match": f"{team_a} vs {team_b}",
            "prediction": prediction,
            "key_factors": key_factors,
            "strategy_a": strategy_a,
            "strategy_b": strategy_b,
            "upset_analysis": upset_analysis,
            "xfactor_watch": xfactor_watch,
        }

    def analyze_all_r32_matches(self) -> List[dict]:
        """Analyze all potential R32 matchups based on group predictions"""
        # First predict group stage outcomes
        group_rankings = self._predict_group_rankings()

        # Generate R32 bracket
        r32_matches = self._generate_r32_bracket(group_rankings)

        # Analyze each match
        analyses: List[dict] = []
        for match in r32_matches:
            analysis = self.analyze_match(match["team_a"], match["team_b"])
            analyses.append(analysis)

        return analyses

    def generate_report(self, team: Optional[str] = None) -> str:
        """Generate a markdown strategy report"""
        if team:
            # Single team deep analysis
            return self._generate_team_report(team)
        else:
            # Full R32 analysis
            return self._generate_r32_report()

    # ------------------------------------------------------------------
    #  Private: Key Factor Identification
    # ------------------------------------------------------------------

    def _identify_key_factors(self, prediction: dict) -> List[dict]:
        """Identify which dimensions have the largest gap between teams"""
        scores_a = prediction["scores_a"]
        scores_b = prediction["scores_b"]

        gaps: List[dict] = []
        for dim in scores_a:
            gap = scores_a[dim] - scores_b.get(dim, 0)
            weight = self.engine.weights.get(dim, 0)
            impact = abs(gap) * weight
            gaps.append({
                "dimension": dim,
                "team_a_score": round(scores_a[dim], 3),
                "team_b_score": round(scores_b.get(dim, 0), 3),
                "gap": round(gap, 3),
                "weight": weight,
                "impact": round(impact, 4),
                "favors": prediction["team_a"] if gap > 0 else prediction["team_b"],
            })

        # Sort by impact (highest first)
        gaps.sort(key=lambda x: x["impact"], reverse=True)
        return gaps[:5]  # Top 5 deciding factors

    # ------------------------------------------------------------------
    #  Private: Strategy Recommendation
    # ------------------------------------------------------------------

    def _recommend_strategy(self, team: str, opponent: str, prediction: dict) -> dict:
        """Recommend strategy based on team's strengths and opponent's weaknesses"""
        team_scores = prediction["scores_a"] if prediction["team_a"] == team else prediction["scores_b"]
        opp_scores = prediction["scores_b"] if prediction["team_a"] == team else prediction["scores_a"]

        coach = COACH_STYLES_2026.get(team, {"style": "balanced"})
        depth = SQUAD_DEPTH_DATA.get(team, {"sub_teams_available": 1})

        recommendations: List[str] = []

        # If team has depth advantage → recommend rotation/pressing
        if team_scores.get("squad_depth", 0.5) > opp_scores.get("squad_depth", 0.5) + 0.1:
            recommendations.append("Use squad rotation to exploit depth advantage — high press in first 60 min, then fresh legs")

        # If opponent has heat vulnerability → recommend high-tempo
        if opp_scores.get("extreme_heat", 0.5) < 0.5:
            recommendations.append("Exploit opponent's heat vulnerability — high tempo, force them to chase")

        # If team has X-factor advantage → recommend creative freedom
        if team_scores.get("xfactor_players", 0.5) > opp_scores.get("xfactor_players", 0.5) + 0.1:
            recommendations.append("Give X-factor players creative freedom — they can break the deadlock")

        # If opponent has coaching instability → recommend tactical surprises
        opp_coach = COACH_STYLES_2026.get(opponent, {"stability": 0.5})
        if opp_coach.get("stability", 0.5) < 0.5:
            recommendations.append("Exploit opponent's coaching instability — start with unexpected formation")

        # If team is underdog → recommend defensive counter
        if prediction.get("prob_a_win", 0.5) < 0.4 if prediction["team_a"] == team else prediction.get("prob_b_win", 0.5) < 0.4:
            recommendations.append("Play defensive counter-attack — absorb pressure, strike on transition")

        # Default
        if not recommendations:
            recommendations.append(f"Play to coach's {coach.get('style', 'balanced')} strengths — maintain tactical discipline")

        return {
            "team": team,
            "coach_style": coach.get("style", "balanced"),
            "recommendations": recommendations,
            "depth_available": depth.get("sub_teams_available", 1),
        }

    # ------------------------------------------------------------------
    #  Private: Upset Potential Analysis
    # ------------------------------------------------------------------

    def _analyze_upset_potential(self, prediction: dict) -> dict:
        """Analyze upset potential based on LightDarkBalance"""
        ldb_a = prediction.get("ldb_a", {})
        ldb_b = prediction.get("ldb_b", {})

        upset_alert = prediction.get("upset_alert", False)

        # Determine favorite and underdog
        if prediction["prob_a_win"] > prediction["prob_b_win"]:
            favorite = prediction["team_a"]
            underdog = prediction["team_b"]
            fav_prob = prediction["prob_a_win"]
            und_prob = prediction["prob_b_win"]
        else:
            favorite = prediction["team_b"]
            underdog = prediction["team_a"]
            fav_prob = prediction["prob_b_win"]
            und_prob = prediction["prob_a_win"]

        upset_probability = min(0.45, und_prob * 1.3)  # Adjusted for knockout

        return {
            "favorite": favorite,
            "underdog": underdog,
            "favorite_prob": round(fav_prob, 3),
            "underdog_prob": round(und_prob, 3),
            "upset_alert": upset_alert,
            "upset_probability": round(upset_probability, 3),
            "upset_risk_level": "high" if upset_probability > 0.35 else ("medium" if upset_probability > 0.25 else "low"),
            "dark_factors": ldb_b.get("dark", 0) if favorite == prediction["team_a"] else ldb_a.get("dark", 0),
        }

    # ------------------------------------------------------------------
    #  Private: X-Factor Player Identification
    # ------------------------------------------------------------------

    def _identify_xfactor_players(self, team_a: str, team_b: str) -> dict:
        """Identify X-factor players to watch in this match"""
        return {
            team_a: {
                "impact_score": XFACTOR_DATA.get(team_a, {}).get("dribbler_impact", 0.5),
                "key_players": XFACTOR_DATA.get(team_a, {}).get("key_players", []),
            },
            team_b: {
                "impact_score": XFACTOR_DATA.get(team_b, {}).get("dribbler_impact", 0.5),
                "key_players": XFACTOR_DATA.get(team_b, {}).get("key_players", []),
            },
        }

    # ------------------------------------------------------------------
    #  Private: Group Stage Prediction
    # ------------------------------------------------------------------

    def _predict_group_rankings(self) -> Dict[str, List[str]]:
        """Predict group stage rankings for all 12 groups"""
        rankings: Dict[str, List[str]] = {}
        for group_name, teams in self.groups.items():
            team_points: Dict[str, float] = {t: 0.0 for t in teams}
            for i in range(len(teams)):
                for j in range(i + 1, len(teams)):
                    result = self.engine.predict_match(teams[i], teams[j], {"stage": "group", "match_number": 1})
                    if result["prob_a_win"] > result["prob_b_win"] and result["prob_a_win"] > result["prob_draw"]:
                        team_points[teams[i]] += 3
                    elif result["prob_draw"] > result["prob_a_win"] and result["prob_draw"] > result["prob_b_win"]:
                        team_points[teams[i]] += 1
                        team_points[teams[j]] += 1
                    else:
                        team_points[teams[j]] += 3

            sorted_teams = sorted(team_points.items(), key=lambda x: x[1], reverse=True)
            rankings[group_name] = [t[0] for t in sorted_teams]

        return rankings

    # ------------------------------------------------------------------
    #  Private: R32 Bracket Generation
    # ------------------------------------------------------------------

    def _generate_r32_bracket(self, group_rankings: Dict[str, List[str]]) -> List[dict]:
        """Generate R32 matchups from group rankings"""
        matches: List[dict] = []
        group_names = sorted(group_rankings.keys())

        # Simplified bracket: 1st of group A vs 2nd of group B, etc.
        for i in range(0, len(group_names), 2):
            if i + 1 < len(group_names):
                g1 = group_names[i]
                g2 = group_names[i + 1]
                matches.append({
                    "team_a": group_rankings[g1][0],  # 1st place
                    "team_b": group_rankings[g2][1],  # 2nd place
                    "group_a": g1,
                    "group_b": g2,
                })

        return matches

    # ------------------------------------------------------------------
    #  Private: Report Generation
    # ------------------------------------------------------------------

    def _generate_team_report(self, team: str) -> str:
        """Generate deep analysis for a single team"""
        profile = self.engine.get_team_profile(team)
        coach = COACH_STYLES_2026.get(team, {})
        depth = SQUAD_DEPTH_DATA.get(team, {})
        xfactor = XFACTOR_DATA.get(team, {})

        lines: List[str] = [
            f"# {team} — WC2026 Strategy Report",
            "",
            "## Team Profile",
            f"- Elo Rating: {profile.get('elo', 'N/A')}",
            f"- Squad Value: €{profile.get('squad_value_m', 'N/A')}M",
            f"- Coach: {coach.get('coach', 'Unknown')} ({coach.get('style', 'balanced')})",
            f"- Coach Stability: {coach.get('stability', 0.5):.0%}",
            f"- Squad Depth: {depth.get('sub_teams_available', 1)} sub-teams available",
            f"- X-Factor Players: {', '.join(xfactor.get('key_players', []))}",
            "",
            "## Dimension Scores",
        ]

        # Add dimension scores
        for dim, score in profile.get("dimension_scores", {}).items():
            weight = self.engine.weights.get(dim, 0)
            lines.append(f"- {dim}: {score:.3f} (weight: {weight:.0%})")

        return "\n".join(lines)

    def _generate_r32_report(self) -> str:
        """Generate full R32 strategy report"""
        analyses = self.analyze_all_r32_matches()

        lines: List[str] = [
            "# WC2026 R32 Strategy Analysis Report",
            "",
            "## Summary",
            f"- Total R32 Matches: {len(analyses)}",
            f"- Upset Alerts: {sum(1 for a in analyses if a['upset_analysis']['upset_alert'])}",
            "",
        ]

        for i, analysis in enumerate(analyses, 1):
            lines.extend([
                f"## Match {i}: {analysis['match']}",
                f"- Win Probability: {analysis['prediction']['prob_a_win']:.1%} vs {analysis['prediction']['prob_b_win']:.1%}",
                f"- Upset Risk: {analysis['upset_analysis']['upset_risk_level']}",
                f"- Key Factor: {analysis['key_factors'][0]['dimension'] if analysis['key_factors'] else 'N/A'}",
                "",
            ])

        return "\n".join(lines)


# ===================================================================
#  QUICK TEST
# ===================================================================

def quick_test() -> None:
    """Run sample strategy analysis and print results"""
    if not _HAS_FORMULA_V11:
        print("ERROR: formula_v11_emoglyph not found. Cannot run quick_test().")
        return

    analyzer = WC2026StrategyAnalyzer()

    print("=" * 70)
    print("WC2026 R32 Strategy Analyzer — Quick Test")
    print("=" * 70)

    # Test 1: Single match analysis
    print("\n--- Test 1: Single Match Analysis (France vs Brazil) ---")
    analysis = analyzer.analyze_match("France", "Brazil")
    pred = analysis["prediction"]
    print(f"  Match: {analysis['match']}")
    print(f"  Win Prob: {pred['prob_a_win']:.1%} vs {pred['prob_b_win']:.1%} (Draw: {pred['prob_draw']:.1%})")
    print(f"  Upset Alert: {analysis['upset_analysis']['upset_alert']}")
    print(f"  Upset Risk Level: {analysis['upset_analysis']['upset_risk_level']}")

    # Test 2: Key factors
    print("\n--- Test 2: Key Deciding Factors ---")
    for factor in analysis["key_factors"]:
        print(f"  {factor['dimension']:25s}: gap={factor['gap']:+.3f}, "
              f"impact={factor['impact']:.4f}, favors={factor['favors']}")

    # Test 3: Strategy recommendations
    print("\n--- Test 3: Strategy Recommendations ---")
    for side in ("strategy_a", "strategy_b"):
        strat = analysis[side]
        print(f"  {strat['team']} (coach: {strat['coach_style']}, depth: {strat['depth_available']} sub-teams):")
        for rec in strat["recommendations"]:
            print(f"    → {rec}")

    # Test 4: Upset analysis
    print("\n--- Test 4: Upset Analysis ---")
    upset = analysis["upset_analysis"]
    print(f"  Favorite: {upset['favorite']} ({upset['favorite_prob']:.1%})")
    print(f"  Underdog: {upset['underdog']} ({upset['underdog_prob']:.1%})")
    print(f"  Upset Probability: {upset['upset_probability']:.1%}")
    print(f"  Dark Factors: {upset['dark_factors']:.4f}")

    # Test 5: X-factor players
    print("\n--- Test 5: X-Factor Players ---")
    for team, info in analysis["xfactor_watch"].items():
        print(f"  {team}: impact={info['impact_score']:.2f}, players={info['key_players']}")

    # Test 6: Second match — underdog scenario
    print("\n--- Test 6: Underdog Scenario (Mexico vs Spain) ---")
    analysis2 = analyzer.analyze_match("Mexico", "Spain")
    pred2 = analysis2["prediction"]
    print(f"  Match: {analysis2['match']}")
    print(f"  Win Prob: {pred2['prob_a_win']:.1%} vs {pred2['prob_b_win']:.1%}")
    print(f"  Upset Risk: {analysis2['upset_analysis']['upset_risk_level']}")
    for side in ("strategy_a", "strategy_b"):
        strat = analysis2[side]
        print(f"  {strat['team']} strategy:")
        for rec in strat["recommendations"]:
            print(f"    → {rec}")

    # Test 7: Single team report
    print("\n--- Test 7: Single Team Report (Argentina) ---")
    report = analyzer.generate_report(team="Argentina")
    # Print first 15 lines of the report
    for line in report.split("\n")[:15]:
        print(f"  {line}")

    # Test 8: Full R32 report (summary only)
    print("\n--- Test 8: Full R32 Report (summary) ---")
    r32_report = analyzer.generate_report()
    # Print just the summary section
    for line in r32_report.split("\n")[:8]:
        print(f"  {line}")

    print("\n" + "=" * 70)
    print("Quick test complete!")
    print("=" * 70)


if __name__ == "__main__":
    quick_test()
