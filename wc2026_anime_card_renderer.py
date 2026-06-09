"""
Captain Tsubasa / Blue Lock Inspired Player Card HTML/SVG Generator

Generates stylized player cards for a Streamlit app using
st.markdown(..., unsafe_allow_html=True).
"""

# ---------------------------------------------------------------------------
# Position → Color mapping
# ---------------------------------------------------------------------------
POSITION_COLORS = {
    "GK": "#2196F3",
    # DEF
    "CB": "#4CAF50",
    "RB": "#4CAF50",
    "LB": "#4CAF50",
    "LWB": "#4CAF50",
    "RWB": "#4CAF50",
    # MID
    "CDM": "#FFB300",
    "CM": "#FFB300",
    "CAM": "#FFB300",
    "LM": "#FFB300",
    "RM": "#FFB300",
    # FWD
    "ST": "#F44336",
    "CF": "#F44336",
    "LW": "#F44336",
    "RW": "#F44336",
}

# ---------------------------------------------------------------------------
# Position → Aura gradient colours (lighter / more saturated for glow)
# ---------------------------------------------------------------------------
POSITION_AURAS = {
    "GK": ("#64B5F6", "#1E88E5"),
    # DEF
    "CB": ("#81C784", "#43A047"),
    "RB": ("#81C784", "#43A047"),
    "LB": ("#81C784", "#43A047"),
    "LWB": ("#81C784", "#43A047"),
    "RWB": ("#81C784", "#43A047"),
    # MID
    "CDM": ("#FFD54F", "#FFA000"),
    "CM": ("#FFD54F", "#FFA000"),
    "CAM": ("#FFD54F", "#FFA000"),
    "LM": ("#FFD54F", "#FFA000"),
    "RM": ("#FFD54F", "#FFA000"),
    # FWD
    "ST": ("#EF9A9A", "#E53935"),
    "CF": ("#EF9A9A", "#E53935"),
    "LW": ("#EF9A9A", "#E53935"),
    "RW": ("#EF9A9A", "#E53935"),
}

# ---------------------------------------------------------------------------
# Attribute key → Weapon display name  (Blue Lock style)
# ---------------------------------------------------------------------------
WEAPON_LABELS = {
    "pace": "SPEED",
    "shooting": "FIRE",
    "passing": "VISION",
    "defending": "WALL",
    "dribbling_skill": "DRIBBLE",
    "fitness_level": "STAMINA",
}

# Attribute keys used for the mini-bars (in display order)
_ATTR_KEYS = ["pace", "shooting", "passing", "defending", "dribbling_skill", "fitness_level"]

# Short display names for the mini-bars
_ATTR_SHORT = {
    "pace": "PAC",
    "shooting": "SHO",
    "passing": "PAS",
    "defending": "DEF",
    "dribbling_skill": "DRI",
    "fitness_level": "FIT",
}


def _pos_color(pos: str) -> str:
    """Return the hex colour for a position, defaulting to gold."""
    return POSITION_COLORS.get(pos.upper(), "#FFB300")


def _pos_aura(pos: str) -> tuple:
    """Return (outer, inner) aura colours for a position."""
    return POSITION_AURAS.get(pos.upper(), ("#FFD54F", "#FFA000"))


def _top_attribute(player_data: dict) -> tuple:
    """Return (key, value) of the player's highest combat attribute."""
    best_key, best_val = "pace", 0
    for k in _ATTR_KEYS:
        v = player_data.get(k, 0)
        if v > best_val:
            best_key, best_val = k, v
    return best_key, best_val


# ---------------------------------------------------------------------------
# Single card generator
# ---------------------------------------------------------------------------
def generate_player_card_html(
    player_data: dict,
    team_name: str = "",
    team_color: str = "#4CAF50",
) -> str:
    """Generate a single anime-style player card as an inline-styled HTML string."""

    name = player_data.get("name", "Unknown")
    position = player_data.get("position", "CM").upper()
    age = player_data.get("age", 0)
    club = player_data.get("club", "")
    rating = player_data.get("rating", 50)
    pace = player_data.get("pace", 50)
    is_xfactor = player_data.get("is_xfactor", False)

    pos_color = _pos_color(position)
    aura_outer, aura_inner = _pos_aura(position)

    # --- X-Factor unique id for CSS animation scoping ---
    card_uid = f"card_{name.replace(' ', '_').lower()}_{id(player_data)}"

    # --- Speed lines (Captain Tsubasa style) when pace > 80 ---
    speed_lines_css = ""
    if pace > 80:
        speed_lines_css = f"""
        #{card_uid} .speed-lines {{
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            border-radius: 12px;
            overflow: hidden;
            pointer-events: none;
            opacity: 0.12;
            background: repeating-linear-gradient(
                -45deg,
                transparent,
                transparent 8px,
                {pos_color} 8px,
                {pos_color} 10px
            );
        }}
        """

    # --- X-Factor animation CSS ---
    xfactor_css = ""
    xfactor_overlay = ""
    if is_xfactor:
        xfactor_css = f"""
        @keyframes xfactor_pulse_{card_uid} {{
            0%, 100% {{ box-shadow: 0 0 8px 2px #FFD700, 0 0 20px 4px rgba(255,215,0,0.3); }}
            50% {{ box-shadow: 0 0 16px 6px #FFD700, 0 0 40px 10px rgba(255,215,0,0.5); }}
        }}
        #{card_uid} .card-body {{
            animation: xfactor_pulse_{card_uid} 1.8s ease-in-out infinite;
            border: 2px solid #FFD700;
        }}
        """
        xfactor_overlay = f"""
        <div style="position:absolute;top:6px;right:6px;z-index:5;filter:drop-shadow(0 0 4px #FFD700);">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="#FFD700">
                <path d="M7 2v11h3v9l7-12h-4l4-8z"/>
            </svg>
        </div>
        """

    # --- Weapon label (Blue Lock style) ---
    weapon_key, weapon_val = _top_attribute(player_data)
    weapon_label = WEAPON_LABELS.get(weapon_key, weapon_key.upper())

    # --- Attribute bars ---
    bars_html = ""
    for ak in _ATTR_KEYS:
        av = player_data.get(ak, 0)
        av_clamped = max(0, min(100, av))
        short = _ATTR_SHORT.get(ak, ak[:3].upper())
        bar_pct = av_clamped
        # colour gradient: low=red, mid=yellow, high=green tinted by position
        if av_clamped >= 80:
            bar_fill = pos_color
        elif av_clamped >= 60:
            bar_fill = "#FFB300"
        else:
            bar_fill = "#E57373"
        bars_html += f"""
        <div style="display:flex;align-items:center;gap:4px;margin-bottom:2px;">
            <span style="color:#aaa;font-size:8px;width:24px;text-align:right;font-family:monospace;">{short}</span>
            <div style="flex:1;height:5px;background:#2a2a3e;border-radius:2px;overflow:hidden;">
                <div style="width:{bar_pct}%;height:100%;background:{bar_fill};border-radius:2px;"></div>
            </div>
            <span style="color:#ccc;font-size:7px;width:18px;font-family:monospace;">{av_clamped}</span>
        </div>
        """

    # --- Compose full card HTML ---
    html = f"""
    <style>
        #{card_uid} .card-aura {{
            position: absolute;
            top: -12px; left: -12px; right: -12px; bottom: -12px;
            border-radius: 20px;
            background: radial-gradient(circle at 50% 40%, {aura_outer}44, {aura_inner}22 50%, transparent 75%);
            z-index: 0;
            pointer-events: none;
        }}
        #{card_uid} .card-body {{
            position: relative;
            width: 200px;
            height: 280px;
            background: linear-gradient(160deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border-radius: 12px;
            border: 1px solid {pos_color}55;
            box-shadow: 0 0 8px 1px {pos_color}33;
            overflow: hidden;
            z-index: 1;
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        #{card_uid} .pos-badge {{
            position: absolute;
            top: 8px; left: 8px;
            width: 38px; height: 38px;
            background: linear-gradient(135deg, {pos_color}, {pos_color}cc);
            clip-path: polygon(15% 0%, 100% 0%, 85% 100%, 0% 100%);
            display: flex; align-items: center; justify-content: center;
            z-index: 3;
        }}
        #{card_uid} .pos-badge span {{
            color: #fff;
            font-weight: 900;
            font-size: 13px;
            text-shadow: 0 0 4px rgba(0,0,0,0.6);
            letter-spacing: 1px;
        }}
        #{card_uid} .rating {{
            position: absolute;
            top: 6px; right: 10px;
            font-size: 48px;
            font-weight: 900;
            color: {pos_color};
            text-shadow: 0 0 12px {pos_color}88, 0 2px 4px rgba(0,0,0,0.5);
            z-index: 3;
            line-height: 1;
        }}
        #{card_uid} .name-plate {{
            position: absolute;
            top: 100px; left: 0; right: 0;
            text-align: center;
            z-index: 3;
        }}
        #{card_uid} .name-plate .name {{
            color: #fff;
            font-size: 14px;
            font-weight: 700;
            text-shadow: 0 0 8px {pos_color}66, 0 2px 3px rgba(0,0,0,0.7);
            letter-spacing: 0.5px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            padding: 0 10px;
        }}
        #{card_uid} .name-plate .club {{
            color: #888;
            font-size: 10px;
            margin-top: 2px;
        }}
        #{card_uid} .weapon-label {{
            position: absolute;
            bottom: 82px; left: 0; right: 0;
            z-index: 3;
            display: flex;
            justify-content: center;
        }}
        #{card_uid} .weapon-label .weapon-inner {{
            background: linear-gradient(135deg, {pos_color}dd, {pos_color}99);
            clip-path: polygon(8% 0%, 92% 0%, 100% 50%, 92% 100%, 8% 100%, 0% 50%);
            padding: 3px 18px;
            text-align: center;
        }}
        #{card_uid} .weapon-label .weapon-inner span {{
            color: #fff;
            font-size: 9px;
            font-weight: 900;
            letter-spacing: 2px;
            text-shadow: 0 0 6px rgba(0,0,0,0.5);
        }}
        #{card_uid} .attr-bars {{
            position: absolute;
            bottom: 8px; left: 10px; right: 10px;
            z-index: 3;
        }}
        #{card_uid} .diagonal-accent {{
            position: absolute;
            top: 55px; left: -30px;
            width: 120px; height: 50px;
            background: {pos_color}18;
            transform: skewY(-12deg);
            z-index: 1;
            pointer-events: none;
        }}
        {speed_lines_css}
        {xfactor_css}
    </style>

    <div id="{card_uid}" style="position:relative;display:inline-block;margin:4px;">
        <div class="card-aura"></div>
        <div class="card-body">
            <div class="diagonal-accent"></div>
            <div class="pos-badge"><span>{position}</span></div>
            <div class="rating">{rating}</div>
            {xfactor_overlay}
            <div class="name-plate">
                <div class="name">{name}</div>
                <div class="club">{club}</div>
            </div>
            <div class="weapon-label">
                <div class="weapon-inner">
                    <span>WEAPON: {weapon_label}</span>
                </div>
            </div>
            <div class="attr-bars">
                {bars_html}
            </div>
            {"<div class='speed-lines'></div>" if pace > 80 else ""}
        </div>
    </div>
    """
    return html


# ---------------------------------------------------------------------------
# Team grid generator
# ---------------------------------------------------------------------------
def generate_team_cards_html(
    players: list,
    team_name: str = "",
    team_color: str = "#4CAF50",
) -> str:
    """Generate a CSS Grid layout of player cards sorted by rating descending."""

    sorted_players = sorted(players, key=lambda p: p.get("rating", 0), reverse=True)

    cards = []
    for p in sorted_players:
        cards.append(generate_player_card_html(p, team_name, team_color))

    cards_joined = "\n".join(cards)

    header = ""
    if team_name:
        header = f"""
        <div style="text-align:center;margin-bottom:12px;">
            <span style="color:{team_color};font-size:20px;font-weight:900;
                          text-shadow:0 0 10px {team_color}66;
                          letter-spacing:3px;font-family:'Segoe UI',Arial,sans-serif;">
                {team_name}
            </span>
        </div>
        """

    html = f"""
    <div style="font-family:'Segoe UI',Arial,sans-serif;">
        {header}
        <div style="display:grid;
                    grid-template-columns:repeat(auto-fill, minmax(200px, 1fr));
                    gap:16px;
                    justify-items:center;">
            {cards_joined}
        </div>
    </div>
    """
    return html


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------
def quick_test() -> None:
    """Create sample cards and print HTML length for sanity check."""

    sample_players = [
        {
            "name": "Lionel Messi",
            "position": "CF",
            "age": 38,
            "club": "Inter Miami",
            "rating": 94,
            "pace": 70,
            "shooting": 92,
            "passing": 93,
            "defending": 35,
            "dribbling_skill": 95,
            "fitness_level": 75,
            "is_xfactor": True,
            "market_value_m": 50.0,
        },
        {
            "name": "Kylian Mbappe",
            "position": "ST",
            "age": 27,
            "club": "Real Madrid",
            "rating": 93,
            "pace": 97,
            "shooting": 90,
            "passing": 78,
            "defending": 36,
            "dribbling_skill": 92,
            "fitness_level": 88,
            "is_xfactor": True,
            "market_value_m": 180.0,
        },
        {
            "name": "Virgil van Dijk",
            "position": "CB",
            "age": 33,
            "club": "Liverpool",
            "rating": 89,
            "pace": 72,
            "shooting": 55,
            "passing": 70,
            "defending": 91,
            "dribbling_skill": 60,
            "fitness_level": 82,
            "is_xfactor": False,
            "market_value_m": 45.0,
        },
        {
            "name": "Kevin De Bruyne",
            "position": "CAM",
            "age": 33,
            "club": "Manchester City",
            "rating": 91,
            "pace": 72,
            "shooting": 86,
            "passing": 94,
            "defending": 58,
            "dribbling_skill": 87,
            "fitness_level": 72,
            "is_xfactor": False,
            "market_value_m": 60.0,
        },
        {
            "name": "Alisson Becker",
            "position": "GK",
            "age": 31,
            "club": "Liverpool",
            "rating": 89,
            "pace": 48,
            "shooting": 20,
            "passing": 55,
            "defending": 40,
            "dribbling_skill": 30,
            "fitness_level": 78,
            "is_xfactor": False,
            "market_value_m": 50.0,
        },
    ]

    # Single card test
    single = generate_player_card_html(sample_players[0])
    print(f"Single card HTML length: {len(single)} chars")

    # Team grid test
    team = generate_team_cards_html(sample_players, team_name="WORLD XI", team_color="#FFD700")
    print(f"Team grid HTML length:  {len(team)} chars")
    print(f"Players in team grid:   {len(sample_players)}")


if __name__ == "__main__":
    quick_test()
