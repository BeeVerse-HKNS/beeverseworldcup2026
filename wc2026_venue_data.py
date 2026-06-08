"""
WC2026 Venue Data Module
========================
Comprehensive venue, flight distance, heat risk, altitude, and travel fatigue
data for the 2026 FIFA World Cup across USA, Canada, and Mexico.

All data is based on publicly available information and approximate values
suitable for simulation and analysis purposes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, Tuple


# ---------------------------------------------------------------------------
# 1. VENUES
# ---------------------------------------------------------------------------

VENUE_IDS: List[str] = [
    "nyc", "boston", "philly", "miami", "atlanta",
    "houston", "dallas", "kc", "la", "sf", "seattle",
    "vancouver", "toronto", "mexicocity", "guadalajara", "monterrey",
]

VENUES: Dict[str, dict] = {
    # ── USA (11) ──────────────────────────────────────────────────────────
    "nyc": {
        "name": "MetLife Stadium",
        "city": "East Rutherford",
        "state_country": "NJ, USA",
        "capacity": 87_000,
        "timezone": "ET",
        "timezone_offset": -4,
        "altitude_meters": 10,
        "wbgt_threshold": 28.0,
        "avg_june_temp_c": 27.0,
        "avg_june_humidity": 65,
        "country": "USA",
        "cluster": "East",
    },
    "boston": {
        "name": "Gillette Stadium",
        "city": "Foxborough",
        "state_country": "MA, USA",
        "capacity": 65_000,
        "timezone": "ET",
        "timezone_offset": -4,
        "altitude_meters": 50,
        "wbgt_threshold": 26.0,
        "avg_june_temp_c": 24.0,
        "avg_june_humidity": 60,
        "country": "USA",
        "cluster": "East",
    },
    "philly": {
        "name": "Lincoln Financial Field",
        "city": "Philadelphia",
        "state_country": "PA, USA",
        "capacity": 69_000,
        "timezone": "ET",
        "timezone_offset": -4,
        "altitude_meters": 12,
        "wbgt_threshold": 29.0,
        "avg_june_temp_c": 27.0,
        "avg_june_humidity": 65,
        "country": "USA",
        "cluster": "East",
    },
    "miami": {
        "name": "Hard Rock Stadium",
        "city": "Miami",
        "state_country": "FL, USA",
        "capacity": 65_000,
        "timezone": "ET",
        "timezone_offset": -4,
        "altitude_meters": 3,
        "wbgt_threshold": 31.0,
        "avg_june_temp_c": 30.0,
        "avg_june_humidity": 80,
        "country": "USA",
        "cluster": "South",
    },
    "atlanta": {
        "name": "Mercedes-Benz Stadium",
        "city": "Atlanta",
        "state_country": "GA, USA",
        "capacity": 71_000,
        "timezone": "ET",
        "timezone_offset": -4,
        "altitude_meters": 315,
        "wbgt_threshold": 32.0,
        "avg_june_temp_c": 29.0,
        "avg_june_humidity": 70,
        "country": "USA",
        "cluster": "South",
    },
    "houston": {
        "name": "NRG Stadium",
        "city": "Houston",
        "state_country": "TX, USA",
        "capacity": 72_000,
        "timezone": "CT",
        "timezone_offset": -5,
        "altitude_meters": 15,
        "wbgt_threshold": 34.0,
        "avg_june_temp_c": 33.0,
        "avg_june_humidity": 75,
        "country": "USA",
        "cluster": "South",
        # HIGHEST RISK — 51 days >35 °C WBGT
    },
    "dallas": {
        "name": "AT&T Stadium",
        "city": "Arlington",
        "state_country": "TX, USA",
        "capacity": 80_000,
        "timezone": "CT",
        "timezone_offset": -5,
        "altitude_meters": 180,
        "wbgt_threshold": 33.0,
        "avg_june_temp_c": 33.0,
        "avg_june_humidity": 65,
        "country": "USA",
        "cluster": "South",
        # 31 days >35 °C WBGT
    },
    "kc": {
        "name": "Arrowhead Stadium",
        "city": "Kansas City",
        "state_country": "MO, USA",
        "capacity": 76_000,
        "timezone": "CT",
        "timezone_offset": -5,
        "altitude_meters": 270,
        "wbgt_threshold": 30.0,
        "avg_june_temp_c": 28.0,
        "avg_june_humidity": 65,
        "country": "USA",
        "cluster": "Central",
    },
    "la": {
        "name": "SoFi Stadium",
        "city": "Inglewood",
        "state_country": "CA, USA",
        "capacity": 70_000,
        "timezone": "PT",
        "timezone_offset": -7,
        "altitude_meters": 30,
        "wbgt_threshold": 24.0,
        "avg_june_temp_c": 22.0,
        "avg_june_humidity": 60,
        "country": "USA",
        "cluster": "West",
    },
    "sf": {
        "name": "Levi's Stadium",
        "city": "Santa Clara",
        "state_country": "CA, USA",
        "capacity": 68_000,
        "timezone": "PT",
        "timezone_offset": -7,
        "altitude_meters": 10,
        "wbgt_threshold": 22.0,
        "avg_june_temp_c": 20.0,
        "avg_june_humidity": 55,
        "country": "USA",
        "cluster": "West",
    },
    "seattle": {
        "name": "Lumen Field",
        "city": "Seattle",
        "state_country": "WA, USA",
        "capacity": 69_000,
        "timezone": "PT",
        "timezone_offset": -7,
        "altitude_meters": 10,
        "wbgt_threshold": 21.0,
        "avg_june_temp_c": 19.0,
        "avg_june_humidity": 55,
        "country": "USA",
        "cluster": "West",
    },
    # ── Canada (2) ────────────────────────────────────────────────────────
    "vancouver": {
        "name": "BC Place",
        "city": "Vancouver",
        "state_country": "BC, Canada",
        "capacity": 54_000,
        "timezone": "PT",
        "timezone_offset": -7,
        "altitude_meters": 10,
        "wbgt_threshold": 20.0,
        "avg_june_temp_c": 18.0,
        "avg_june_humidity": 60,
        "country": "Canada",
        "cluster": "West",
    },
    "toronto": {
        "name": "BMO Field",
        "city": "Toronto",
        "state_country": "ON, Canada",
        "capacity": 45_000,
        "timezone": "ET",
        "timezone_offset": -4,
        "altitude_meters": 80,
        "wbgt_threshold": 27.0,
        "avg_june_temp_c": 24.0,
        "avg_june_humidity": 65,
        "country": "Canada",
        "cluster": "East",
    },
    # ── Mexico (3) ────────────────────────────────────────────────────────
    "mexicocity": {
        "name": "Estadio Azteca",
        "city": "Mexico City",
        "state_country": "CDMX, Mexico",
        "capacity": 87_000,
        "timezone": "MCT",
        "timezone_offset": -5,
        "altitude_meters": 2_240,
        "wbgt_threshold": 25.0,
        "avg_june_temp_c": 23.0,
        "avg_june_humidity": 55,
        "country": "Mexico",
        "cluster": "Mexico",
        # ALTITUDE HIGH
    },
    "guadalajara": {
        "name": "Estadio Akron",
        "city": "Guadalajara",
        "state_country": "JAL, Mexico",
        "capacity": 49_000,
        "timezone": "MCT",
        "timezone_offset": -5,
        "altitude_meters": 1_566,
        "wbgt_threshold": 28.0,
        "avg_june_temp_c": 27.0,
        "avg_june_humidity": 60,
        "country": "Mexico",
        "cluster": "Mexico",
    },
    "monterrey": {
        "name": "Estadio BBVA",
        "city": "Monterrey",
        "state_country": "NL, Mexico",
        "capacity": 53_000,
        "timezone": "MCT",
        "timezone_offset": -5,
        "altitude_meters": 530,
        "wbgt_threshold": 33.0,
        "avg_june_temp_c": 32.0,
        "avg_june_humidity": 65,
        "country": "Mexico",
        "cluster": "Mexico",
    },
}


# ---------------------------------------------------------------------------
# 2. FLIGHT_DISTANCE_MATRIX
# ---------------------------------------------------------------------------

# Order matches VENUE_IDS for indexing.
# All distances in statute miles (approximate great-circle flight distances).
#
# Index:  0=nyc  1=boston  2=philly  3=miami  4=atlanta
#         5=houston  6=dallas  7=kc  8=la  9=sf
#        10=seattle  11=vancouver  12=toronto  13=mexicocity  14=guadalajara  15=monterrey

_FLIGHT_DIST: List[List[int]] = [
    #  nyc   boston  philly  miami  atlanta  houston  dallas   kc     la     sf   seattle vancouver toronto mexicocity guadalajara monterrey
    [     0,    190,    90,  1090,    750,   1420,   1370, 1090,  2475, 2570,   2410,    2440,    360,    2090,     2230,     1770],  # nyc
    [   190,      0,   270,  1260,    930,   1600,   1550, 1250,  2600, 2700,   2500,    2530,    430,    2220,     2360,     1950],  # boston
    [    90,    270,     0,  1020,    670,   1340,   1290, 1010,  2400, 2500,   2340,    2370,    330,    2010,     2150,     1690],  # philly
    [  1090,   1260,  1020,     0,    600,    970,   1110, 1240,  2340, 2580,   2730,    2770,   1240,    1290,     1430,      990],  # miami
    [   750,    930,   670,   600,      0,    700,    780,  780,  1940, 2140,   2190,    2230,    740,    1370,     1510,      950],  # atlanta
    [  1420,   1600,  1340,   970,    700,      0,    240,  640,  1370, 1640,   1890,    1940,   1340,     810,      680,      470],  # houston
    [  1370,   1550,  1290,  1110,    780,    240,      0,  460,  1240, 1480,   1680,    1730,   1200,     930,      810,      540],  # dallas
    [  1090,   1250,  1010,  1240,    780,    640,    460,    0,  1360, 1500,   1490,    1530,    810,    1310,     1200,      920],  # kc
    [  2475,   2600,  2400,  2340,   1940,   1370,   1240, 1360,     0,  380,    960,    1080,   2170,    1560,     1370,     1190],  # la
    [  2570,   2700,  2500,  2580,   2140,   1640,   1480, 1500,   380,    0,    680,     800,   2260,    1880,     1700,     1530],  # sf
    [  2410,   2500,  2340,  2730,   2190,   1890,   1680, 1490,   960,  680,      0,     130,   2070,    2330,     2240,     2060],  # seattle
    [  2440,   2530,  2370,  2770,   2230,   1940,   1730, 1530,  1080,  800,    130,       0,   2090,    2410,     2320,     2140],  # vancouver
    [   360,    430,   330,  1240,    740,   1340,   1200,  810,  2170, 2260,   2070,    2090,      0,    2020,     2160,     1700],  # toronto
    [  2090,   2220,  2010,  1290,   1370,    810,    930, 1310,  1560, 1880,   2330,    2410,   2020,       0,      280,      430],  # mexicocity
    [  2230,   2360,  2150,  1430,   1510,    680,    810, 1200,  1370, 1700,   2240,    2320,   2160,     280,        0,      420],  # guadalajara
    [  1770,   1950,  1690,   990,    950,    470,    540,  920,  1190, 1530,   2060,    2140,   1700,     430,      420,        0],  # monterrey
]

FLIGHT_DISTANCE_MATRIX: Dict[str, Dict[str, int]] = {}
for _i, _id_a in enumerate(VENUE_IDS):
    FLIGHT_DISTANCE_MATRIX[_id_a] = {}
    for _j, _id_b in enumerate(VENUE_IDS):
        FLIGHT_DISTANCE_MATRIX[_id_a][_id_b] = _FLIGHT_DIST[_i][_j]


# ---------------------------------------------------------------------------
# 3. HEAT_ACCLIMATIZATION
# ---------------------------------------------------------------------------

HEAT_ACCLIMATIZATION: Dict[str, float] = {
    "africa": 0.85,
    "middle_east": 0.90,
    "central_america_caribbean": 0.80,
    "south_america": 0.75,
    "southern_europe": 0.65,
    "northern_europe": 0.50,
    "east_asia": 0.55,
    "default": 0.60,
}


# ---------------------------------------------------------------------------
# 4. Helper functions
# ---------------------------------------------------------------------------

def get_venue(venue_id: str) -> dict:
    """Return full venue data dict for a given venue_id.

    Args:
        venue_id: One of the keys in VENUES (e.g. "nyc", "la", "dallas").

    Returns:
        Dict with all venue fields.

    Raises:
        KeyError: If venue_id is not found.
    """
    if venue_id not in VENUES:
        raise KeyError(
            f"Unknown venue_id '{venue_id}'. "
            f"Valid IDs: {', '.join(VENUE_IDS)}"
        )
    return VENUES[venue_id]


def get_flight_distance(venue_a: str, venue_b: str) -> float:
    """Return the approximate flight distance in statute miles between two venues.

    Args:
        venue_a: Origin venue_id.
        venue_b: Destination venue_id.

    Returns:
        Distance in statute miles. Returns 0 when both IDs are the same.
    """
    if venue_a not in FLIGHT_DISTANCE_MATRIX:
        raise KeyError(f"Unknown venue_id '{venue_a}'. Valid: {', '.join(VENUE_IDS)}")
    if venue_b not in FLIGHT_DISTANCE_MATRIX[venue_a]:
        raise KeyError(f"Unknown venue_id '{venue_b}'. Valid: {', '.join(VENUE_IDS)}")
    return float(FLIGHT_DISTANCE_MATRIX[venue_a][venue_b])


def get_wbgt_risk(
    venue_id: str,
    match_time: Literal["morning", "afternoon", "evening"] = "afternoon",
) -> dict:
    """Calculate WBGT heat risk for a venue at a given match time.

    The WBGT value is adjusted based on time of day:
      - afternoon: full threshold (peak heat)
      - morning:   threshold − 4 °C
      - evening:   threshold − 2 °C

    Risk levels:
      - low:     WBGT < 25 °C
      - medium:  25 °C ≤ WBGT < 28 °C
      - high:    28 °C ≤ WBGT < 31 °C
      - extreme: WBGT ≥ 31 °C

    Args:
        venue_id: Venue identifier.
        match_time: One of "morning", "afternoon", "evening".

    Returns:
        Dict with keys: risk_level (str), wbgt_adjusted (float).
    """
    venue = get_venue(venue_id)
    base_wbgt = venue["wbgt_threshold"]

    time_offsets = {"morning": -4.0, "afternoon": 0.0, "evening": -2.0}
    offset = time_offsets.get(match_time, 0.0)
    wbgt_adjusted = base_wbgt + offset

    if wbgt_adjusted >= 31.0:
        risk_level = "extreme"
    elif wbgt_adjusted >= 28.0:
        risk_level = "high"
    elif wbgt_adjusted >= 25.0:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {"risk_level": risk_level, "wbgt_adjusted": round(wbgt_adjusted, 1)}


def get_altitude_effect(venue_id: str, team_origin_region: str) -> float:
    """Calculate altitude performance penalty (0–1) for a team at a venue.

    Higher values indicate greater performance degradation. Teams from
    high-altitude regions (e.g. Mexico, Andean countries) receive reduced
    penalties at altitude venues.

    Penalty model:
      - altitude < 500 m:  0.00 (no effect)
      - 500–1000 m:        0.02
      - 1000–1500 m:       0.04
      - 1500–2000 m:       0.07
      - ≥ 2000 m:          0.10

    The penalty is then reduced by the team's heat/acclimatization factor
    if they originate from a high-altitude region.

    Args:
        venue_id: Venue identifier.
        team_origin_region: Region key from HEAT_ACCLIMATIZATION or
            "mexico" / "andean" for high-altitude-acclimated teams.

    Returns:
        Float between 0 and 1 representing the altitude penalty.
    """
    venue = get_venue(venue_id)
    altitude = venue["altitude_meters"]

    # Base penalty by altitude band
    if altitude < 500:
        penalty = 0.00
    elif altitude < 1000:
        penalty = 0.02
    elif altitude < 1500:
        penalty = 0.04
    elif altitude < 2000:
        penalty = 0.07
    else:
        penalty = 0.10

    # Reduce penalty for high-altitude-acclimated teams
    high_alt_regions = {"mexico", "andean", "middle_east", "africa"}
    if team_origin_region in high_alt_regions and penalty > 0:
        penalty *= 0.3  # 70 % reduction for acclimated teams

    return round(penalty, 3)


def get_travel_fatigue(venue_from: str, venue_to: str) -> dict:
    """Calculate travel fatigue metrics between two venues.

    Fatigue score model (0–1 scale):
      - distance component:  min(distance / 3000, 1.0) × 0.50
      - timezone component:  abs(tz_change) / 4 × 0.30
      - border component:    0.20 if crossing USA/Canada/Mexico border

    Args:
        venue_from: Origin venue_id.
        venue_to:   Destination venue_id.

    Returns:
        Dict with keys:
          - distance_miles (float)
          - timezone_change (int): hours difference
          - cross_border (bool): True if countries differ
          - fatigue_score (float): 0–1 composite score
    """
    v_from = get_venue(venue_from)
    v_to = get_venue(venue_to)

    distance = get_flight_distance(venue_from, venue_to)
    tz_change = v_to["timezone_offset"] - v_from["timezone_offset"]
    cross_border = v_from["country"] != v_to["country"]

    # Distance component (0–0.50)
    dist_component = min(distance / 3000.0, 1.0) * 0.50

    # Timezone component (0–0.30)
    tz_component = (abs(tz_change) / 4.0) * 0.30

    # Border-crossing component (0 or 0.20)
    border_component = 0.20 if cross_border else 0.0

    fatigue_score = round(min(dist_component + tz_component + border_component, 1.0), 3)

    return {
        "distance_miles": distance,
        "timezone_change": tz_change,
        "cross_border": cross_border,
        "fatigue_score": fatigue_score,
    }
