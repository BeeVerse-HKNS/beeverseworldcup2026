"""
WC2026 Recovery Data Module
============================
Recovery and rest time data for all 48 qualified teams.
Calculates recovery coefficients based on league end dates,
CL final participation, and in-season status.
"""

from datetime import datetime, date
from typing import Dict, Optional, Any


WC_START_DATE = "2026-06-11"

LEAGUE_END_DATES = {
    "premier_league": "2026-05-24",
    "la_liga": "2026-05-24",
    "serie_a": "2026-05-24",
    "bundesliga": "2026-05-16",
    "ligue_1": "2026-05-23",
    "champions_league_final": "2026-05-30",
    "europa_league_final": "2026-05-27",
    "conference_league_final": "2026-05-25",
    "saudi_pro_league": "2026-04-25",
    "mls": "in_season",
    "liga_mx": "in_season",
    "j_league": "in_season",
    "k_league": "in_season",
    "a_league": "2026-05-10",
    "chinese_super_league": "in_season",
    "brazilian_serie_a": "in_season",
    "argentine_primera": "2026-05-18",
    "turkish_super_lig": "2026-05-18",
    "eredivisie": "2026-05-10",
    "primeira_liga": "2026-05-18",
    "scottish_premiership": "2026-05-18",
    "austrian_bundesliga": "2026-05-18",
    "czech_first_league": "2026-05-18",
    "norwegian_eliteserien": "in_season",
    "swedish_allsvenskan": "in_season",
    "swiss_super_league": "2026-05-18",
    "belgian_pro_league": "2026-05-18",
    "croatian_first_league": "2026-05-18",
    "ecuadorian_serie_a": "in_season",
    "paraguayan_primera": "in_season",
    "ivorian_ligue_1": "2026-05-15",
    "ghanaian_premier_league": "in_season",
    "egyptian_premier_league": "in_season",
    "algerian_ligue_1": "2026-05-15",
    "tunisian_ligue_1": "2026-05-15",
    "iraqi_premier_league": "2026-05-10",
    "iranian_pro_league": "2026-05-15",
    "jordanian_pro_league": "2026-04-30",
    "uzbek_super_league": "2026-05-10",
    "new_zealand_football_championship": "2026-04-30",
    "haitian_ligue_haïtienne": "2026-05-10",
    "dr_congo_linafoot": "2026-05-10",
    "cape_verdean_championship": "2026-05-10",
    "curacao_league": "2026-05-10",
    "bosnian_premier_league": "2026-05-18",
    "qatar_stars_league": "2026-04-20",
    "panamanian_lpf": "in_season",
    "senegalese_ligue_1": "2026-05-15",
}

# Map each team to their primary league(s)
TEAM_LEAGUE_MAPPING = {
    "Mexico": ["liga_mx"],
    "South Africa": ["premier_league"],  # Most players abroad
    "South Korea": ["k_league"],
    "Czech Republic": ["czech_first_league"],
    "Canada": ["mls"],
    "Bosnia and Herzegovina": ["bosnian_premier_league"],
    "Qatar": ["qatar_stars_league"],
    "Switzerland": ["swiss_super_league"],
    "Brazil": ["brazilian_serie_a"],
    "Morocco": ["la_liga"],  # Most players in European leagues
    "Haiti": ["haitian_ligue_haïtienne"],
    "Scotland": ["scottish_premiership"],
    "USA": ["mls"],
    "Paraguay": ["paraguayan_primera"],
    "Australia": ["a_league"],
    "Turkey": ["turkish_super_lig"],
    "Germany": ["bundesliga"],
    "Curacao": ["curacao_league"],
    "Ivory Coast": ["ivorian_ligue_1"],
    "Ecuador": ["ecuadorian_serie_a"],
    "Netherlands": ["eredivisie"],
    "Japan": ["j_league"],
    "Sweden": ["swedish_allsvenskan"],
    "Tunisia": ["tunisian_ligue_1"],
    "Belgium": ["belgian_pro_league"],
    "Egypt": ["egyptian_premier_league"],
    "Iran": ["iranian_pro_league"],
    "New Zealand": ["new_zealand_football_championship"],
    "Spain": ["la_liga"],
    "Cape Verde": ["cape_verdean_championship"],
    "Saudi Arabia": ["saudi_pro_league"],
    "Uruguay": ["argentine_primera"],  # Most players abroad
    "France": ["ligue_1"],
    "Senegal": ["senegalese_ligue_1"],
    "Iraq": ["iraqi_premier_league"],
    "Norway": ["norwegian_eliteserien"],
    "Argentina": ["argentine_primera"],
    "Algeria": ["algerian_ligue_1"],
    "Austria": ["austrian_bundesliga"],
    "Jordan": ["jordanian_pro_league"],
    "Portugal": ["primeira_liga"],
    "DR Congo": ["dr_congo_linafoot"],
    "Uzbekistan": ["uzbek_super_league"],
    "Colombia": ["brazilian_serie_a"],  # Most players abroad
    "England": ["premier_league"],
    "Croatia": ["croatian_first_league"],
    "Ghana": ["ghanaian_premier_league"],
    "Panama": ["panamanian_lpf"],
}

# Teams with CL final players (estimated)
CL_FINAL_TEAMS = {
    "Arsenal": {"league": "premier_league", "cl_final_date": "2026-05-30", "estimated_players": 8},
    "PSG": {"league": "ligue_1", "cl_final_date": "2026-05-30", "estimated_players": 7},
}

# Teams that have CL final players in their national squad
# (estimated based on likely national team call-ups)
TEAM_CL_FINAL_PLAYERS = {
    "France": 4,      # PSG players in France squad
    "England": 5,     # Arsenal players in England squad
    "Spain": 2,       # Arsenal/PSG Spanish players
    "Brazil": 2,      # Arsenal/PSG Brazilian players
    "Netherlands": 1, # Arsenal Dutch player
    "Portugal": 1,    # PSG Portuguese player
    "Morocco": 1,     # PSG Moroccan player
    "Germany": 1,     # Arsenal German player
    "Italy": 1,       # PSG Italian player (not qualified but player may be in squad)
}


def _calculate_days_rest(league_end_date_str: str) -> int:
    """Calculate days between league end and WC start"""
    if league_end_date_str == "in_season":
        return 0
    try:
        league_end = datetime.strptime(league_end_date_str, "%Y-%m-%d").date()
        wc_start = datetime.strptime(WC_START_DATE, "%Y-%m-%d").date()
        return max(0, (wc_start - league_end).days)
    except ValueError:
        return 14  # Default 2 weeks


def calculate_recovery_coefficient(team_name: str) -> float:
    """
    Calculate recovery coefficient for a team (0.0-1.0).

    Factors:
    - Days rest from league end to WC start
    - CL final player penalty
    - In-season bonus (fitness maintained)
    - Saudi league bonus (extra rest)
    """
    leagues = TEAM_LEAGUE_MAPPING.get(team_name, [])
    if not leagues:
        return 0.70  # Default

    primary_league = leagues[0]
    league_end = LEAGUE_END_DATES.get(primary_league, "2026-05-18")

    # Base recovery from days rest
    if league_end == "in_season":
        base_recovery = 0.70  # In-season: fitness good but no camp
        in_season = True
    else:
        days_rest = _calculate_days_rest(league_end)
        base_recovery = min(1.0, days_rest / 28.0)
        in_season = False

    # CL final penalty
    cl_players = TEAM_CL_FINAL_PLAYERS.get(team_name, 0)
    cl_penalty = cl_players * 0.03  # 3% penalty per CL final player

    # Saudi league bonus (extra rest)
    saudi_bonus = 0.15 if primary_league == "saudi_pro_league" else 0.0

    # In-season fitness bonus
    fitness_bonus = 0.10 if in_season else 0.0

    # Calculate final coefficient
    coefficient = base_recovery - cl_penalty + saudi_bonus + fitness_bonus

    return max(0.30, min(1.0, coefficient))


def get_team_recovery(team_name: str) -> Dict[str, Any]:
    """Get full recovery data for a team"""
    leagues = TEAM_LEAGUE_MAPPING.get(team_name, [])
    primary_league = leagues[0] if leagues else "unknown"
    league_end = LEAGUE_END_DATES.get(primary_league, "2026-05-18")

    days_rest = _calculate_days_rest(league_end) if league_end != "in_season" else 0
    cl_players = TEAM_CL_FINAL_PLAYERS.get(team_name, 0)
    in_season = league_end == "in_season"
    coefficient = calculate_recovery_coefficient(team_name)

    return {
        "team": team_name,
        "primary_league": primary_league,
        "league_end_date": league_end,
        "days_rest_before_wc": days_rest,
        "cl_final_players": cl_players,
        "cl_final_penalty": round(cl_players * 0.03, 3),
        "in_season_during_wc": in_season,
        "recovery_coefficient": round(coefficient, 4),
    }


def get_fatigue_risk_level(team_name: str) -> str:
    """Get fatigue risk level for a team"""
    coefficient = calculate_recovery_coefficient(team_name)
    if coefficient >= 0.85:
        return "low"
    elif coefficient >= 0.70:
        return "medium"
    elif coefficient >= 0.55:
        return "high"
    else:
        return "extreme"


def get_match_recovery(team_name: str, days_since_last_match: int) -> float:
    """Get recovery factor for a specific match based on days since last match"""
    base = calculate_recovery_coefficient(team_name)
    match_recovery = min(1.0, days_since_last_match / 4.0)
    return base * 0.6 + match_recovery * 0.4
