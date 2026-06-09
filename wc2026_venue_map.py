"""
WC2026 3D Interactive Venue Map
================================
Plotly-based 3D map for all 16 World Cup 2026 venues with flight distance
arcs, heat-risk colouring, and team-group highlighting.
"""

from __future__ import annotations

from itertools import combinations
from typing import Dict, List, Optional

import plotly.graph_objects as go

from wc2026_venue_data import VENUES, VENUE_IDS, get_flight_distance, get_wbgt_risk
from formula_v11_emoglyph import WC2026_GROUPS

# ---------------------------------------------------------------------------
# 1. VENUE COORDINATES
# ---------------------------------------------------------------------------

VENUE_COORDS: Dict[str, Dict[str, float]] = {
    "nyc":         {"lat": 40.8135,  "lon": -74.0745},
    "boston":      {"lat": 42.0909,  "lon": -71.2643},
    "philly":      {"lat": 39.9008,  "lon": -75.1674},
    "miami":       {"lat": 25.9580,  "lon": -80.2389},
    "atlanta":     {"lat": 33.7555,  "lon": -84.4000},
    "houston":     {"lat": 29.6847,  "lon": -95.4107},
    "dallas":      {"lat": 32.7493,  "lon": -97.0925},
    "kc":          {"lat": 39.0489,  "lon": -94.4839},
    "la":          {"lat": 33.9535,  "lon": -118.3387},
    "sf":          {"lat": 37.4032,  "lon": -121.9698},
    "seattle":     {"lat": 47.5952,  "lon": -122.3316},
    "vancouver":   {"lat": 49.2768,  "lon": -123.1120},
    "toronto":     {"lat": 43.6392,  "lon": -79.4286},
    "mexicocity":  {"lat": 19.3022,  "lon": -99.1506},
    "guadalajara": {"lat": 20.5767,  "lon": -103.3286},
    "monterrey":   {"lat": 25.6538,  "lon": -100.3994},
}

# ---------------------------------------------------------------------------
# 2. GROUP → VENUE ASSIGNMENTS
# ---------------------------------------------------------------------------

GROUP_VENUE_ASSIGNMENTS: Dict[str, List[str]] = {
    "A":  ["mexicocity", "guadalajara", "monterrey"],
    "B":  ["toronto", "vancouver", "boston"],
    "C":  ["la", "sf", "seattle"],
    "D":  ["atlanta", "miami", "houston"],
    "E":  ["nyc", "philly", "boston"],
    "F":  ["dallas", "houston", "kc"],
    "G":  ["la", "seattle", "vancouver"],
    "H":  ["atlanta", "miami", "dallas"],
    "I":  ["nyc", "philly", "miami"],
    "J":  ["kc", "dallas", "houston"],
    "K":  ["la", "sf", "seattle"],
    "L":  ["toronto", "boston", "nyc"],
}

# ---------------------------------------------------------------------------
# 3. RISK COLOURS
# ---------------------------------------------------------------------------

RISK_COLORS: Dict[str, str] = {
    "low":    "green",
    "medium": "yellow",
    "high":   "orange",
    "extreme": "red",
}

# ---------------------------------------------------------------------------
# 4. MAIN MAP FUNCTION
# ---------------------------------------------------------------------------

def create_venue_map_3d(selected_team: Optional[str] = None) -> go.Figure:
    """Create a 3D Plotly map of all WC2026 venues.

    Args:
        selected_team: Optional team name. When provided, the team's group
            venues are highlighted with larger markers and flight arcs with
            distance labels are drawn between them.

    Returns:
        A Plotly Figure object.
    """

    # -- Determine highlighted venues (if a team is selected) ---------------
    highlight_venues: set[str] = set()
    highlight_group: Optional[str] = None

    if selected_team:
        for group_letter, teams in WC2026_GROUPS.items():
            if selected_team in teams:
                highlight_group = group_letter
                highlight_venues = set(GROUP_VENUE_ASSIGNMENTS.get(group_letter, []))
                break

    # -- Capacity range for marker-size scaling ----------------------------
    capacities = [VENUES[vid]["capacity"] for vid in VENUE_IDS]
    cap_min, cap_max = min(capacities), max(capacities)

    def _marker_size(capacity: int) -> float:
        if cap_max == cap_min:
            return 17.5
        return 10 + (capacity - cap_min) / (cap_max - cap_min) * 15

    # -- Build per-venue data arrays ---------------------------------------
    lats, lons, texts, sizes, colors = [], [], [], [], []

    for vid in VENUE_IDS:
        v = VENUES[vid]
        coord = VENUE_COORDS[vid]
        risk = get_wbgt_risk(vid, "afternoon")

        lats.append(coord["lat"])
        lons.append(coord["lon"])
        sizes.append(_marker_size(v["capacity"]))
        colors.append(RISK_COLORS.get(risk["risk_level"], "gray"))

        texts.append(
            f"Venue: {v['name']}\n"
            f"City: {v['city']}\n"
            f"Capacity: {v['capacity']:,}\n"
            f"WBGT: {risk['wbgt_adjusted']}°C\n"
            f"Altitude: {v['altitude_meters']}m\n"
            f"Risk: {risk['risk_level']}"
        )

    # -- Base venue markers ------------------------------------------------
    fig = go.Figure()

    # Non-highlighted venues (or all if no team selected)
    if highlight_venues:
        idx_regular = [i for i, vid in enumerate(VENUE_IDS) if vid not in highlight_venues]
        idx_highlight = [i for i, vid in enumerate(VENUE_IDS) if vid in highlight_venues]
    else:
        idx_regular = list(range(len(VENUE_IDS)))
        idx_highlight = []

    if idx_regular:
        fig.add_trace(go.Scattergeo(
            lat=[lats[i] for i in idx_regular],
            lon=[lons[i] for i in idx_regular],
            text=[texts[i] for i in idx_regular],
            hoverinfo="text",
            mode="markers",
            marker=dict(
                size=[sizes[i] for i in idx_regular],
                color=[colors[i] for i in idx_regular],
                opacity=0.75,
                line=dict(width=1, color="white"),
            ),
            name="Venues",
        ))

    # Highlighted venues (larger, diamond symbol)
    if idx_highlight:
        fig.add_trace(go.Scattergeo(
            lat=[lats[i] for i in idx_highlight],
            lon=[lons[i] for i in idx_highlight],
            hovertext=[texts[i] for i in idx_highlight],
            hoverinfo="text",
            mode="markers+text",
            textposition="top center",
            text=[VENUE_IDS[i].upper() for i in idx_highlight],
            marker=dict(
                size=[sizes[i] * 1.5 for i in idx_highlight],
                color=[colors[i] for i in idx_highlight],
                symbol="diamond",
                opacity=1.0,
                line=dict(width=2, color="cyan"),
            ),
            name=f"Group {highlight_group} Venues",
        ))

    # -- Flight arcs between highlighted venues ----------------------------
    if highlight_venues and len(highlight_venues) >= 2:
        hv_list = sorted(highlight_venues)
        for va, vb in combinations(hv_list, 2):
            coord_a, coord_b = VENUE_COORDS[va], VENUE_COORDS[vb]
            dist = get_flight_distance(va, vb)

            # Arc via a midpoint lifted in latitude for visual curvature
            mid_lon = (coord_a["lon"] + coord_b["lon"]) / 2
            mid_lat = (coord_a["lat"] + coord_b["lat"]) / 2 + 2.0

            fig.add_trace(go.Scattergeo(
                lat=[coord_a["lat"], mid_lat, coord_b["lat"]],
                lon=[coord_a["lon"], mid_lon, coord_b["lon"]],
                mode="lines+text",
                text=["", f"{dist:.0f} mi", ""],
                textposition="middle center",
                textfont=dict(size=9, color="cyan"),
                line=dict(width=1.5, color="cyan", dash="dot"),
                hoverinfo="skip",
                showlegend=False,
            ))

    # -- Layout ------------------------------------------------------------
    title_text = "WC2026 Venue Map"
    if selected_team and highlight_group:
        title_text += f" — {selected_team} (Group {highlight_group})"

    fig.update_layout(
        title=dict(text=title_text, font=dict(size=18, color="white")),
        geo=dict(
            scope="north america",
            projection_type="albers usa",
            showland=True,
            landcolor="#2a2a2a",
            showocean=True,
            oceancolor="#1a1a2e",
            showlakes=True,
            lakecolor="#1a1a2e",
            showcountries=True,
            countrycolor="#444444",
            showsubunits=True,
            subunitcolor="#444444",
            coastlinecolor="#444444",
        ),
        paper_bgcolor="#121212",
        font_color="white",
        height=600,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(
            bgcolor="#1e1e1e",
            font=dict(color="white"),
        ),
    )

    return fig


# ---------------------------------------------------------------------------
# 5. HELPER
# ---------------------------------------------------------------------------

def get_team_venues(team: str) -> List[str]:
    """Return the list of venue_ids where a team's group plays.

    Args:
        team: Team name as it appears in WC2026_GROUPS.

    Returns:
        List of venue_id strings. Empty list if the team is not found.
    """
    for group_letter, teams in WC2026_GROUPS.items():
        if team in teams:
            return list(GROUP_VENUE_ASSIGNMENTS.get(group_letter, []))
    return []


# ---------------------------------------------------------------------------
# 6. QUICK TEST
# ---------------------------------------------------------------------------

def quick_test() -> None:
    """Create the venue map and print figure info."""
    fig = create_venue_map_3d()
    print(f"Figure type: {type(fig).__name__}")
    print(f"Number of traces: {len(fig.data)}")
    print(f"Layout title: {fig.layout.title.text}")
    print("Quick test passed — map created successfully.")

    # Also test with a selected team
    fig2 = create_venue_map_3d(selected_team="USA")
    print(f"\nWith team='USA': {len(fig2.data)} traces")
    venues = get_team_venues("USA")
    print(f"USA venues: {venues}")


if __name__ == "__main__":
    quick_test()
