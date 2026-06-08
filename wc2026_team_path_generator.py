"""
World Cup 2026 Team Path Generator
===================================
Generates per-team path/strategy analysis for all 48 teams using FormulaV11Engine.

Provides:
  - Group stage match-by-match analysis with win/draw/loss probabilities
  - Structural advantage assessment (can team rest in match 3?)
  - Projected knockout path (R32 → R16 → QF → SF → Final)
  - Light-Dark Balance assessment
  - X-Factor player identification
  - Best/worst case scenarios
  - Tri-lingual strategy text (EN / 簡中 / 繁中)
"""

from typing import Dict, List, Optional

from formula_v11_emoglyph import (
    FormulaV11Engine,
    WC2026_GROUPS,
    ELO_RATINGS,
    COACH_STYLES_2026,
    XFACTOR_DATA,
    GROUP_STRENGTH_DATA,
    SQUAD_DEPTH_DATA,
    MENTAL_DATA,
    TOURNAMENT_EXPERIENCE,
    HOST_NATIONS,
)


# ===================================================================
#  R32 Bracket Seeding — simplified mapping
# ===================================================================

R32_BRACKET = {
    # 1st place teams → opponent slot description
    "A1": {"vs": "B2/C2/D2", "bracket_pos": 1},
    "B1": {"vs": "A2/C3/D3/E3", "bracket_pos": 2},
    "C1": {"vs": "D3/E3/F3", "bracket_pos": 3},
    "D1": {"vs": "E2/F2/G2", "bracket_pos": 4},
    "E1": {"vs": "F3/G3/H3", "bracket_pos": 5},
    "F1": {"vs": "G2/H2/I2", "bracket_pos": 6},
    "G1": {"vs": "H3/I3/J3", "bracket_pos": 7},
    "H1": {"vs": "I2/J2/K2", "bracket_pos": 8},
    "I1": {"vs": "J3/K3/L3", "bracket_pos": 9},
    "J1": {"vs": "K2/L2/A2", "bracket_pos": 10},
    "K1": {"vs": "L3/A3/B3", "bracket_pos": 11},
    "L1": {"vs": "B2/C2/D2", "bracket_pos": 12},
}

# Mapping from group winner slot to most-likely 3rd/2nd place opponent group
# Used to pick the most likely opponent team from the bracket description
R32_OPPONENT_GROUP_HINTS = {
    "A1": ["B", "C", "D"],       # 2nd place from B/C/D
    "B1": ["A", "C", "D", "E"],  # 2nd/3rd from A/C/D/E
    "C1": ["D", "E", "F"],       # 3rd from D/E/F
    "D1": ["E", "F", "G"],       # 2nd from E/F/G
    "E1": ["F", "G", "H"],       # 3rd from F/G/H
    "F1": ["G", "H", "I"],       # 2nd from G/H/I
    "G1": ["H", "I", "J"],       # 3rd from H/I/J
    "H1": ["I", "J", "K"],       # 2nd from I/J/K
    "I1": ["J", "K", "L"],       # 3rd from J/K/L
    "J1": ["K", "L", "A"],       # 2nd from K/L/A
    "K1": ["L", "A", "B"],       # 3rd from L/A/B
    "L1": ["B", "C", "D"],       # 2nd from B/C/D
}


# ===================================================================
#  X-Factor Player Names — 2-3 key players per team
# ===================================================================

XFACTOR_PLAYERS_NAMES: Dict[str, List[str]] = {
    # Tier 1 — Elite
    "France": ["Mbappe", "Griezmann", "Tchouameni"],
    "Argentina": ["Messi", "Alvarez", "Mac Allister"],
    "Spain": ["Yamal", "Pedri", "Rodri"],
    "England": ["Bellingham", "Saka", "Kane"],
    "Brazil": ["Vinicius Jr", "Rodrygo", "Bruno Guimaraes"],
    "Portugal": ["Leao", "Bruno Fernandes", "Dias"],
    # Tier 2 — Contenders
    "Germany": ["Wirtz", "Musiala", "Rudiger"],
    "Netherlands": ["Simons", "Gakpo", "van Dijk"],
    "Belgium": ["De Bruyne", "Doku", "Lukaku"],
    "Croatia": ["Modric", "Kramaric", "Gvardiol"],
    "Uruguay": ["Nunez", "Valverde", "Araujo"],
    # Tier 3 — Dark Horses
    "Colombia": ["Diaz", "James Rodriguez", "Lerma"],
    "Switzerland": ["Xhaka", "Akanji", "Kobel"],
    "USA": ["Pulisic", "Reyna", "McKennie"],
    "Mexico": ["Jimenez", "Lozano", "Ochoa"],
    "Japan": ["Kubo", "Mitoma", "Endo"],
    "Morocco": ["Hakimi", "Ziyech", "Amrabat"],
    "Senegal": ["Mane", "Sarr", "Kouyate"],
    "Australia": ["Kewell Jr", "Irvine", "Ryan"],
    "Turkey": ["Calhanoglu", "Guler", "Kokcu"],
    "Austria": ["Sabitzer", "Arnautovic", "Laimer"],
    "Sweden": ["Isak", "Kulusevski", "Lindelof"],
    # Tier 4 — Competitive
    "Ecuador": ["Valencia", "Caicedo", "Estupinan"],
    "Ivory Coast": ["Kessie", "Pepe", "Hall"],
    "Ghana": ["Kudus", "Partey", "Ayew"],
    "South Korea": ["Son", "Lee Kang-in", "Kim Min-jae"],
    "Paraguay": ["Almiron", "Enciso", "Gomez"],
    "Egypt": ["Salah", "Trezeguet", "El Shenawy"],
    "Algeria": ["Mahrez", "Brahimi", "Bensebaini"],
    "Scotland": ["Robertson", "McTominay", "McGregor"],
    "Norway": ["Haaland", "Odegaard", "Ryerson"],
    "Czech Republic": ["Soucek", "Schick", "Coufal"],
    "Iran": ["Taremi", "Azmoun", "Jahanbakhsh"],
    "Tunisia": ["Khazri", "Brahimi", "Dahmen"],
    "Panama": ["Torres", "Davis", "Cooper"],
    "Iraq": ["Hussein", "Ali", "Ataa"],
    # Tier 5 — Debutants / Minnows
    "Bosnia and Herzegovina": ["Dzeko", "Pjanic", "Kolasinac"],
    "Qatar": ["Almoez Ali", "Afif", "Hassan"],
    "Saudi Arabia": ["Al-Dawsari", "Al-Shehri", "Al-Owais"],
    "Uzbekistan": ["Shomurodov", "Masharipov", "Saidov"],
    "Jordan": ["Al-Naimat", "Al-Rashdan", "Al-Mardi"],
    "New Zealand": ["Wood", "Boxall", "Roche"],
    "Haiti": ["Duckens Nazon", "Joseph", "Placide"],
    "DR Congo": ["Bakambu", "Kakuta", "Mbayo"],
    "Cape Verde": ["Mendes", "Soares", "Vozinha"],
    "Curacao": ["Bacuna", "Martina", "Cuypers"],
    # Additional
    "South Africa": ["Modise", "Zungu", "Williams"],
    "Canada": ["Davies", "David", "Borjan"],
}


# ===================================================================
#  Strategy Templates — tri-lingual
# ===================================================================

STRATEGY_TEMPLATES = {
    "dominant_attack": {
        "en": "Attack from start, use squad depth",
        "zh_cn": "开局强攻，利用阵容深度",
        "zh_tw": "開局強攻，利用陣容深度",
    },
    "controlled_possession": {
        "en": "Control possession, manage tempo",
        "zh_cn": "控制球权，掌控节奏",
        "zh_tw": "控球權，掌控節奏",
    },
    "defensive_counter": {
        "en": "Sit deep, hit on counter-attack",
        "zh_cn": "收缩防守，伺机反击",
        "zh_tw": "收縮防守，伺機反擊",
    },
    "high_press": {
        "en": "Press high, force mistakes",
        "zh_cn": "高位逼抢，迫使失误",
        "zh_tw": "高位逼搶，迫使失誤",
    },
    "pragmatic_control": {
        "en": "Stay organized, take no risks",
        "zh_cn": "保持阵型，稳中求胜",
        "zh_tw": "保持陣型，穩中求勝",
    },
    "rotation_rest": {
        "en": "Rotate squad, key players rest",
        "zh_cn": "轮换阵容，核心球员休息",
        "zh_tw": "輪換陣容，核心球員休息",
    },
    "must_win": {
        "en": "All-out attack, must-win scenario",
        "zh_cn": "全力进攻，必须取胜",
        "zh_tw": "全力進攻，必須取勝",
    },
    "underdog_defend": {
        "en": "Defend compactly, hope for a moment",
        "zh_cn": "密集防守，等待机会",
        "zh_tw": "密集防守，等待機會",
    },
    "balanced_approach": {
        "en": "Balanced approach, adapt to opponent",
        "zh_cn": "攻守平衡，随机应变",
        "zh_tw": "攻守平衡，隨機應變",
    },
}

KNOCKOUT_STRATEGY_TEMPLATES = {
    "squad_depth": {
        "en": "Use depth to overwhelm tired opponent",
        "zh_cn": "用阵容深度压倒疲惫对手",
        "zh_tw": "用陣容深度壓倒疲憊對手",
    },
    "tactical_mastery": {
        "en": "Out-coach the opponent tactically",
        "zh_cn": "战术上压制对手",
        "zh_tw": "戰術上壓制對手",
    },
    "xfactor_moment": {
        "en": "Rely on X-factor players for magic",
        "zh_cn": "依靠X因子球员创造奇迹",
        "zh_tw": "依靠X因子球員創造奇蹟",
    },
    "defensive_wall": {
        "en": "Build defensive wall, survive and advance",
        "zh_cn": "筑起防守长城，坚守晋级",
        "zh_tw": "築起防守長城，堅守晉級",
    },
    "mental_toughness": {
        "en": "Mental toughness to handle pressure",
        "zh_cn": "心理素质扛住压力",
        "zh_tw": "心理素質扛住壓力",
    },
    "counter_punch": {
        "en": "Absorb pressure, strike on counter",
        "zh_cn": "吸收压力，反击制胜",
        "zh_tw": "吸收壓力，反擊制勝",
    },
    "experience_edge": {
        "en": "Use tournament experience to navigate",
        "zh_cn": "用赛事经验化解危机",
        "zh_tw": "用賽事經驗化解危機",
    },
    "youth_energy": {
        "en": "Let young talent play with freedom",
        "zh_cn": "让年轻天才自由发挥",
        "zh_tw": "讓年輕天才自由發揮",
    },
    "balanced_approach": {
        "en": "Balanced approach, adapt to the game",
        "zh_cn": "攻守平衡，随机应变",
        "zh_tw": "攻守平衡，隨機應變",
    },
}


# ===================================================================
#  TeamPathGenerator
# ===================================================================

class TeamPathGenerator:
    """Generates per-team path/strategy analysis for all 48 WC2026 teams."""

    def __init__(self):
        self.engine = FormulaV11Engine()
        self._group_lookup = self._build_group_lookup()
        self._all_teams = self._build_all_teams_list()

    # ----------------------------------------------------------------
    #  Helpers
    # ----------------------------------------------------------------

    def _build_group_lookup(self) -> Dict[str, str]:
        """Map team name → group letter."""
        lookup = {}
        for group_name, teams in WC2026_GROUPS.items():
            for team in teams:
                lookup[team] = group_name
        return lookup

    def _build_all_teams_list(self) -> List[str]:
        """Flat list of all 48 teams."""
        teams = []
        for group_teams in WC2026_GROUPS.values():
            teams.extend(group_teams)
        return teams

    def _get_group(self, team: str) -> str:
        return self._group_lookup.get(team, "?")

    def _get_group_teammates(self, team: str) -> List[str]:
        group = self._get_group(team)
        return [t for t in WC2026_GROUPS.get(group, []) if t != team]

    def _elo_rank_in_group(self, team: str) -> int:
        """1 = highest Elo in group."""
        group = self._get_group(team)
        group_elos = sorted(
            [(t, ELO_RATINGS.get(t, 1500)) for t in WC2026_GROUPS.get(group, [])],
            key=lambda x: x[1],
            reverse=True,
        )
        for rank, (t, _) in enumerate(group_elos, 1):
            if t == team:
                return rank
        return 4

    def _projected_group_finish(self, team: str) -> str:
        rank = self._elo_rank_in_group(team)
        return {1: "1st", 2: "2nd", 3: "3rd", 4: "4th"}.get(rank, "4th")

    def _group_finish_confidence(self, team: str) -> float:
        """Confidence in projected group finish (0-1)."""
        group = self._get_group(team)
        group_teams = WC2026_GROUPS.get(group, [])
        team_elo = ELO_RATINGS.get(team, 1500)
        group_elos = sorted([ELO_RATINGS.get(t, 1500) for t in group_teams], reverse=True)

        rank = self._elo_rank_in_group(team)
        if rank == 1:
            gap = team_elo - group_elos[1] if len(group_elos) > 1 else 200
            return min(0.95, 0.55 + gap / 500)
        elif rank == 2:
            gap_above = group_elos[0] - team_elo
            gap_below = team_elo - group_elos[2] if len(group_elos) > 2 else 50
            return min(0.85, 0.40 + gap_below / 400 - gap_above / 800)
        elif rank == 3:
            gap_above = group_elos[1] - team_elo if len(group_elos) > 1 else 50
            gap_below = team_elo - group_elos[3] if len(group_elos) > 3 else 0
            return min(0.70, 0.25 + gap_below / 500)
        else:
            return 0.15

    def _structural_advantage(self, team: str) -> dict:
        """Calculate structural advantage label, score, and reason."""
        ctx = {"stage": "group", "match_number": 1}
        score = self.engine.score_structural_advantage(team, ctx)

        group = self._get_group(team)
        group_data = GROUP_STRENGTH_DATA.get(group, {})
        is_dominant = group_data.get("dominant_team") == team
        early_secure = group_data.get("early_secure_prob", 0.50)

        if score >= 0.70:
            label = "HIGH"
        elif score >= 0.45:
            label = "MEDIUM"
        else:
            label = "LOW"

        if is_dominant and early_secure >= 0.75:
            reason = "Dominant team, can secure in 2 matches, rest in 3rd"
        elif is_dominant:
            reason = "Likely group winner, may rotate in match 3"
        elif score >= 0.45:
            reason = "Competitive group, must fight all 3 matches"
        else:
            reason = "Underdog in group, every match is a battle"

        return {"label": label, "score": round(score, 2), "reason": reason}

    def _pick_strategy_for_group_match(self, team: str, opponent: str, match_num: int, is_dominant: bool) -> str:
        """Pick a strategy template key for a group stage match."""
        team_elo = ELO_RATINGS.get(team, 1500)
        opp_elo = ELO_RATINGS.get(opponent, 1500)
        style = COACH_STYLES_2026.get(team, {}).get("style", "balanced")

        # Match 3 rotation for dominant teams
        if match_num == 3 and is_dominant:
            return "rotation_rest"

        # Must-win for underdogs in later matches
        if match_num >= 2 and team_elo < opp_elo - 100:
            return "must_win"

        # Style-based strategy
        if style == "attacking":
            return "dominant_attack" if team_elo > opp_elo else "counter_punch"
        elif style == "possession":
            return "controlled_possession"
        elif style == "defensive":
            return "defensive_counter"
        elif style == "high_press":
            return "high_press"
        elif style == "counter_attack":
            return "defensive_counter" if team_elo > opp_elo else "counter_punch"
        elif style == "pragmatic":
            return "pragmatic_control"
        else:
            return "balanced_approach"

    def _pick_knockout_strategy_key(self, team: str, opponent: str) -> str:
        """Pick a knockout strategy template key."""
        depth = SQUAD_DEPTH_DATA.get(team, {"bench_ratio": 0.5})
        bench = depth.get("bench_ratio", 0.5) if isinstance(depth, dict) else 0.5
        mental = MENTAL_DATA["knockout_pressure_resistance"].get(team, 0.5)
        exp = TOURNAMENT_EXPERIENCE.get(team, 0.3)
        xfac = XFACTOR_DATA.get(team, {"young_talent": 0.5})
        youth = xfac.get("young_talent", 0.5) if isinstance(xfac, dict) else 0.5
        style = COACH_STYLES_2026.get(team, {}).get("style", "balanced")

        # Pick the strongest factor
        candidates = [
            (bench, "squad_depth"),
            (mental, "mental_toughness"),
            (exp, "experience_edge"),
            (youth, "youth_energy"),
        ]
        if style == "defensive":
            candidates.append((0.8, "defensive_wall"))
        if style == "counter_attack":
            candidates.append((0.8, "counter_punch"))

        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    def _pick_knockout_key_factor(self, team: str) -> str:
        """Identify the key factor for knockout strategy."""
        depth = SQUAD_DEPTH_DATA.get(team, {"bench_ratio": 0.5})
        bench = depth.get("bench_ratio", 0.5) if isinstance(depth, dict) else 0.5
        mental = MENTAL_DATA["knockout_pressure_resistance"].get(team, 0.5)
        exp = TOURNAMENT_EXPERIENCE.get(team, 0.3)

        if bench >= 0.70:
            return "squad_depth"
        if mental >= 0.75:
            return "mental_toughness"
        if exp >= 0.70:
            return "tournament_experience"
        return "xfactor_players"

    def _most_likely_r32_opponent(self, team: str) -> dict:
        """Determine the most likely R32 opponent based on group finish and bracket."""
        group = self._get_group(team)
        rank = self._elo_rank_in_group(team)

        if rank == 1:
            slot = f"{group}1"
            bracket_info = R32_BRACKET.get(slot)
            if not bracket_info:
                return {"projected_opponent": "TBD", "opponent_team": "TBD"}

            hint_groups = R32_OPPONENT_GROUP_HINTS.get(slot, [])
            # Pick the strongest 2nd/3rd place team from hint groups
            best_team = None
            best_elo = 0
            for hg in hint_groups:
                hg_teams = WC2026_GROUPS.get(hg, [])
                # Get 2nd/3rd strongest in that group
                sorted_teams = sorted(
                    [(t, ELO_RATINGS.get(t, 1500)) for t in hg_teams],
                    key=lambda x: x[1],
                    reverse=True,
                )
                # Skip if this team is in the same group
                candidates = [t for t, _ in sorted_teams[1:3]]  # 2nd and 3rd
                for c in candidates:
                    c_elo = ELO_RATINGS.get(c, 1500)
                    if c_elo > best_elo:
                        best_elo = c_elo
                        best_team = c

            return {
                "projected_opponent": bracket_info["vs"],
                "opponent_team": best_team or "TBD",
            }

        elif rank == 2:
            # 2nd place teams face specific 1st place or other 2nd place teams
            # Simplified: face the 1st place of a nearby group
            group_idx = ord(group) - ord("A")
            # Face the 1st place of the previous or next group
            target_group_idx = (group_idx + 1) % 12
            target_group = chr(ord("A") + target_group_idx)
            target_teams = WC2026_GROUPS.get(target_group, [])
            sorted_teams = sorted(
                [(t, ELO_RATINGS.get(t, 1500)) for t in target_teams],
                key=lambda x: x[1],
                reverse=True,
            )
            return {
                "projected_opponent": f"1st place Group {target_group}",
                "opponent_team": sorted_teams[0][0] if sorted_teams else "TBD",
            }

        else:
            # 3rd place: harder to predict exact bracket position
            return {
                "projected_opponent": "1st place (group winner)",
                "opponent_team": "TBD",
            }

    def _project_knockout_path(self, team: str) -> List[dict]:
        """Project the full knockout path from R32 to Final."""
        path = []
        stages = [
            ("R32", "r32"),
            ("R16", "r16"),
            ("QF", "qf"),
            ("SF", "sf"),
            ("Final", "final"),
        ]

        current_team = team
        r32_info = self._most_likely_r32_opponent(team)

        for i, (stage_label, stage_key) in enumerate(stages):
            if i == 0:
                opponent = r32_info["opponent_team"]
                projected_opponent = r32_info["projected_opponent"]
            else:
                # For later rounds, pick a likely opponent based on overall strength
                opponent = self._likely_later_opponent(team, stage_key)
                projected_opponent = f"Likely {stage_label} opponent"

            if opponent == "TBD" or opponent == current_team:
                opponent = self._fallback_opponent(team, stage_key)
                projected_opponent = f"Projected {stage_label} opponent"

            ctx = {"stage": stage_key, "venue_id": "nyc", "match_time": "afternoon"}
            prediction = self.engine.predict_match(current_team, opponent, ctx)
            win_prob = prediction["prob_a_win"]

            strategy_key = self._pick_knockout_strategy_key(current_team, opponent)
            key_factor = self._pick_knockout_key_factor(current_team)

            strategy_tpl = KNOCKOUT_STRATEGY_TEMPLATES.get(strategy_key, KNOCKOUT_STRATEGY_TEMPLATES["balanced_approach"])

            path.append({
                "stage": stage_label,
                "projected_opponent": projected_opponent,
                "opponent_team": opponent,
                "win_prob": round(win_prob, 2),
                "key_factor": key_factor,
                "strategy_en": strategy_tpl["en"],
                "strategy_zh_cn": strategy_tpl["zh_cn"],
                "strategy_zh_tw": strategy_tpl["zh_tw"],
            })

            # If win probability is very low, stop projecting deeper
            if win_prob < 0.15 and i >= 1:
                break

        return path

    def _likely_later_opponent(self, team: str, stage: str) -> str:
        """Pick a plausible opponent for later knockout rounds."""
        # Use top teams as likely opponents, excluding the team itself
        top_teams = sorted(
            [(t, ELO_RATINGS.get(t, 1500)) for t in self._all_teams if t != team],
            key=lambda x: x[1],
            reverse=True,
        )

        stage_idx = {"r32": 0, "r16": 1, "qf": 2, "sf": 3, "final": 4}.get(stage, 0)
        # Deeper rounds → stronger opponents
        offset = min(stage_idx * 2, len(top_teams) - 1)
        return top_teams[offset][0]

    def _fallback_opponent(self, team: str, stage: str) -> str:
        """Fallback when primary opponent lookup fails."""
        top_teams = sorted(
            [(t, ELO_RATINGS.get(t, 1500)) for t in self._all_teams if t != team],
            key=lambda x: x[1],
            reverse=True,
        )
        return top_teams[0][0] if top_teams else "TBD"

    def _calculate_overall_win_probability(self, team: str) -> float:
        """Estimate overall tournament win probability using Elo + dimension scores."""
        team_elo = ELO_RATINGS.get(team, 1500)
        profile = self.engine.get_team_profile(team)
        weighted_total = profile["weighted_total"]

        # Blend Elo-based probability with dimension-based score
        # Elo probability: logistic vs average field
        avg_elo = sum(ELO_RATINGS.values()) / len(ELO_RATINGS)
        elo_prob = 1 / (1 + 10 ** ((avg_elo - team_elo) / 400))
        # Scale to tournament (48 teams)
        elo_tournament_prob = elo_prob / 10  # Rough scaling

        # Dimension-based adjustment
        dim_prob = weighted_total ** 3 * 0.5  # Non-linear scaling

        blended = elo_tournament_prob * 0.6 + dim_prob * 0.4
        return min(0.25, max(0.001, blended))

    def _critical_risk(self, team: str) -> str:
        """Identify the most critical risk for a team."""
        coach_inst = MENTAL_DATA["new_coach_instability"].get(team, 0.2)
        coach_name = COACH_STYLES_2026.get(team, {}).get("coach", "the coach")
        depth = SQUAD_DEPTH_DATA.get(team, {"bench_ratio": 0.5})
        bench = depth.get("bench_ratio", 0.5) if isinstance(depth, dict) else 0.5
        mental = MENTAL_DATA["knockout_pressure_resistance"].get(team, 0.5)
        expectation = MENTAL_DATA["national_expectation_pressure"].get(team, 0.4)

        risks = []
        if coach_inst >= 0.35:
            risks.append(f"New coach instability if {coach_name} experiments")
        if bench < 0.45:
            risks.append("Thin squad depth could be exposed in knockout rounds")
        if mental < 0.40:
            risks.append("Mental fragility under high-pressure situations")
        if expectation > 0.70:
            risks.append("Heavy national expectation pressure")

        return risks[0] if risks else "No major red flags identified"

    def _best_case_scenario(self, team: str) -> str:
        rank = self._elo_rank_in_group(team)
        if rank == 1:
            return "Win group comfortably, favorable bracket, reach Final"
        elif rank == 2:
            return "Advance as 2nd, upset in knockout, reach SF"
        elif rank == 3:
            return "Sneak through as 3rd-place, surprise run to QF"
        else:
            return "Fight for 3rd-place spot, dream of R32 upset"

    def _worst_case_scenario(self, team: str) -> str:
        rank = self._elo_rank_in_group(team)
        coach_inst = MENTAL_DATA["new_coach_instability"].get(team, 0.2)
        if rank <= 2 and coach_inst >= 0.30:
            return "Coach instability derails campaign, upset in group or R32"
        elif rank <= 2:
            return "Squad fatigue from club season, upset in QF"
        elif rank == 3:
            return "Fail to advance, lose critical 3rd match"
        else:
            return "Eliminated in group stage with zero points"

    # ----------------------------------------------------------------
    #  Public API
    # ----------------------------------------------------------------

    def generate_team_path(self, team_name: str) -> dict:
        """Generate a complete path analysis for one team."""
        if team_name not in self._group_lookup:
            raise ValueError(f"Unknown team: {team_name}. Must be one of the 48 WC2026 teams.")

        group = self._get_group(team_name)
        teammates = self._get_group_teammates(team_name)
        struct = self._structural_advantage(team_name)
        group_data = GROUP_STRENGTH_DATA.get(group, {})
        is_dominant = group_data.get("dominant_team") == team_name

        # Group matches
        group_matches = []
        for match_num, opponent in enumerate(teammates, 1):
            ctx = {"stage": "group", "match_number": match_num, "venue_id": "nyc", "match_time": "afternoon"}
            prediction = self.engine.predict_match(team_name, opponent, ctx)

            strategy_key = self._pick_strategy_for_group_match(team_name, opponent, match_num, is_dominant)
            strategy_tpl = STRATEGY_TEMPLATES.get(strategy_key, STRATEGY_TEMPLATES["balanced_approach"])

            group_matches.append({
                "match": match_num,
                "opponent": opponent,
                "win_prob": round(prediction["prob_a_win"], 2),
                "draw_prob": round(prediction["prob_draw"], 2),
                "loss_prob": round(prediction["prob_b_win"], 2),
                "recommended_approach_en": strategy_tpl["en"],
                "recommended_approach_zh_cn": strategy_tpl["zh_cn"],
                "recommended_approach_zh_tw": strategy_tpl["zh_tw"],
            })

        # Projected group finish
        projected_finish = self._projected_group_finish(team_name)
        finish_confidence = self._group_finish_confidence(team_name)

        # Knockout path
        knockout_path = self._project_knockout_path(team_name)

        # Overall win probability
        overall_win_prob = self._calculate_overall_win_probability(team_name)

        # Light-Dark Balance
        default_opp = teammates[0] if teammates else "balanced_opponent"
        ctx = {"stage": "group", "venue_id": "nyc", "match_time": "afternoon"}
        ldb_result = self.engine.calculate_light_dark_balance(team_name, default_opp, ctx)

        # X-Factor players
        xfactor_players = XFACTOR_PLAYERS_NAMES.get(team_name, XFACTOR_DATA.get(team_name, {}).get("key_players", []))

        return {
            "team": team_name,
            "group": group,
            "group_teammates": teammates,
            "structural_advantage": struct["label"],
            "structural_advantage_score": struct["score"],
            "structural_advantage_reason": struct["reason"],
            "group_matches": group_matches,
            "projected_group_finish": projected_finish,
            "projected_group_finish_confidence": round(finish_confidence, 2),
            "knockout_path": knockout_path,
            "overall_win_probability": round(overall_win_prob, 3),
            "light_dark_balance": {
                "ldb": ldb_result["ldb"],
                "light": ldb_result["light"],
                "dark": ldb_result["dark"],
                "confidence": ldb_result["confidence"],
            },
            "xfactor_players": xfactor_players,
            "critical_risk": self._critical_risk(team_name),
            "best_case_scenario": self._best_case_scenario(team_name),
            "worst_case_scenario": self._worst_case_scenario(team_name),
        }

    def generate_all_team_paths(self) -> dict:
        """Generate paths for all 48 teams, keyed by team name."""
        return {team: self.generate_team_path(team) for team in self._all_teams}

    def explain_formula_human_readable(self, language: str = "en") -> str:
        """Return human-readable formula explanation.

        Args:
            language: "en", "zh_cn", or "zh_tw"
        """
        if language == "zh_cn":
            return (
                "🏆 2026世界杯AI预测 — 原理揭秘\n"
                "\n"
                "我们的AI分析17个关键因素：\n"
                "\n"
                "外部因素 (36%):\n"
                "  🔋 休息恢复 (12%) — 球队有多新鲜？\n"
                "  🌡️ 极端高温 (5%) — 能扛住夏天酷热吗？\n"
                "  ✈️ 旅途疲劳 (4%) — 飞了多远？\n"
                "  🏟️ 主场优势 (4%) — 主场作战？\n"
                "  ⛰️ 海拔效应 (3%) — 墨西哥城空气稀薄\n"
                "  🍀 运气因子 (2%) — 不可预测的元素\n"
                "  📅 赛程密度 (1%) — 比赛有多密集？\n"
                "  🏗️ 结构优势 (3%) — 新！第三场能否轮换休息？\n"
                "\n"
                "内部因素 (64%):\n"
                "  📊 球队评级 (10%) — 历史实力如何？\n"
                "  📈 近期状态 (8%) — 最近赢球了吗？\n"
                "  👥 阵容深度 (10%) — 替补席能顶上吗？\n"
                "  🧠 教练水平 (8%) — 战术大师？\n"
                "  ⭐ X因子球员 (8%) — 改变比赛的球员\n"
                "  💪 心理素质 (5%) — 能扛住压力吗？\n"
                "  💰 阵容身价 (7%) — 有多少天赋？\n"
                "  🏅 赛事经验 (5%) — 以前来过吗？\n"
                "  ⚔️ 战术对位 (5%) — 风格相克？\n"
                "\n"
                "AI运行5000+次模拟，预测每支球队的晋级之路！"
            )
        elif language == "zh_tw":
            return (
                "🏆 2026世界盃AI預測 — 原理揭秘\n"
                "\n"
                "我們的AI分析17個關鍵因素：\n"
                "\n"
                "外部因素 (36%):\n"
                "  🔋 休息恢復 (12%) — 球隊有幾新鮮？\n"
                "  🌡️ 極端高溫 (5%) — 能扛住夏天酷熱嗎？\n"
                "  ✈️ 旅途疲勞 (4%) — 飛咗幾遠？\n"
                "  🏟️ 主場優勢 (4%) — 主場作戰？\n"
                "  ⛰️ 海拔效應 (3%) — 墨西哥城空氣稀薄\n"
                "  🍀 運氣因子 (2%) — 不可預測嘅元素\n"
                "  📅 賽程密度 (1%) — 比賽有幾密集？\n"
                "  🏗️ 結構優勢 (3%) — 新！第三場可否輪換休息？\n"
                "\n"
                "內部因素 (64%):\n"
                "  📊 球隊評級 (10%) — 歷史實力如何？\n"
                "  📈 近期狀態 (8%) — 最近贏波未？\n"
                "  👥 陣容深度 (10%) — 後備席頂得順嗎？\n"
                "  🧠 教練水平 (8%) — 戰術大師？\n"
                "  ⭐ X因子球員 (8%) — 改變比賽嘅球員\n"
                "  💪 心理素質 (5%) — 能扛住壓力嗎？\n"
                "  💰 陣容身價 (7%) — 有幾多天賦？\n"
                "  🏅 賽事經驗 (5%) — 以前嚟過未？\n"
                "  ⚔️ 戰術對位 (5%) — 風格相剋？\n"
                "\n"
                "AI運行5000+次模擬，預測每支球隊嘅晉級之路！"
            )
        else:
            return (
                "🏆 World Cup 2026 AI Prediction — How It Works\n"
                "\n"
                "Our AI analyzes 17 key factors for each team:\n"
                "\n"
                "EXTERNAL FACTORS (36%):\n"
                "  🔋 Rest & Recovery (12%) — How fresh is the team?\n"
                "  🌡️ Extreme Heat (5%) — Can they handle the summer heat?\n"
                "  ✈️ Travel Fatigue (4%) — How far did they fly?\n"
                "  🏟️ Home Advantage (4%) — Playing on home soil?\n"
                "  ⛰️ Altitude (3%) — Mexico City's thin air\n"
                "  🍀 Luck Factor (2%) — The unpredictable element\n"
                "  📅 Schedule Density (1%) — How tight are the matches?\n"
                "  🏗️ Structural Advantage (3%) — NEW! Can they rest in match 3?\n"
                "\n"
                "INTERNAL FACTORS (64%):\n"
                "  📊 Team Rating (10%) — How strong historically?\n"
                "  📈 Recent Form (8%) — Are they winning lately?\n"
                "  👥 Squad Depth (10%) — Can the bench deliver?\n"
                "  🧠 Coaching (8%) — Tactical mastermind?\n"
                "  ⭐ X-Factor Players (8%) — Game-changers\n"
                "  💪 Mental Strength (5%) — Can they handle pressure?\n"
                "  💰 Squad Value (7%) — How much talent?\n"
                "  🏅 Tournament Experience (5%) — Been here before?\n"
                "  ⚔️ Tactical Matchup (5%) — Style vs style\n"
                "\n"
                "The AI runs 5000+ simulations to predict each team's path!"
            )


# ===================================================================
#  Quick Test
# ===================================================================

if __name__ == "__main__":
    gen = TeamPathGenerator()

    # Test with a top team
    path = gen.generate_team_path("France")
    print(f"France: Group {path['group']}, Structural: {path['structural_advantage']}, Win: {path['overall_win_probability']:.1%}")
    print(f"R32 opponent: {path['knockout_path'][0]['opponent_team']}")
    print(f"Formula EN: {gen.explain_formula_human_readable('en')[:100]}...")

    print()

    # Test with an underdog
    path2 = gen.generate_team_path("Uzbekistan")
    print(f"Uzbekistan: Group {path2['group']}, Structural: {path2['structural_advantage']}, Advancement: {path2['projected_group_finish_confidence']:.1%}")
