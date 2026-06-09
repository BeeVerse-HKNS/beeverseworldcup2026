"""
World Cup 2026 Deep Research Data Module
=========================================
Comprehensive research data gathered from worldwide sources (EN/ES/FR/PT/ZH/JA/AR)
covering injuries, weather, coach statements, friendly results, travel, and odds.

Research date: 2026-06-09
Tournament: June 11 - July 19, 2026 (USA/Canada/Mexico)
Teams: 48 | Groups: 12 | Matches: 104

Sources: Chinese sports media (Toutiao/Sohu/163), ESPN, Guardian, FIFA official,
         FIFPro, WWA (World Weather Attribution), Foot Mercato, CBS Sports,
         LiveScore, FourFourTwo, and multilingual news aggregators.
"""

from datetime import datetime
from typing import Dict, List, Any, Tuple


DEEP_RESEARCH_DATA: Dict[str, Any] = {
    "_meta": {
        "research_date": "2026-06-09",
        "tournament_dates": "2026-06-11 to 2026-07-19",
        "host_nations": ["USA", "Canada", "Mexico"],
        "total_teams": 48,
        "total_groups": 12,
        "total_matches": 104,
        "venues_count": 16,
        "data_cutoff": "2026-06-09T08:00:00Z",
        "sources": [
            "Toutiao sports (Chinese)", "Sohu sports (Chinese)", "163.com (Chinese)",
            "ESPN", "The Guardian", "FIFA.com", "FIFPro official",
            "World Weather Attribution (WWA)", "Foot Mercato", "CBS Sports",
            "LiveScore", "FourFourTwo", "ACSM guidelines",
        ],
    },

    # =========================================================================
    # 1. INJURY UPDATES
    # =========================================================================
    "injuries": {
        "_summary": "Major injury crisis across multiple top teams. 16+ key players confirmed out. "
                    "Argentina has 9 players carrying injuries into camp. Netherlands hardest hit "
                    "relative to squad size. Brazil loses two key attackers.",

        "confirmed_out": [
            # Brazil
            {"player": "Rodrygo", "team": "Brazil", "club": "Real Madrid", "position": "FW",
             "injury": "ACL + meniscus tear (right knee)", "impact_level": "high",
             "market_value_eur": 45_000_000, "note": "Devastating loss for Brazil's attack"},

            {"player": "Estevao Willian", "team": "Brazil", "club": "Chelsea/Palmeiras", "position": "FW",
             "injury": "Hamstring tear", "impact_level": "high",
             "market_value_eur": 80_000_000, "note": "19-year-old superstar prospect out"},

            {"player": "Eder Militao", "team": "Brazil", "club": "Real Madrid", "position": "CB",
             "injury": "Hamstring tear", "impact_level": "medium",
             "market_value_eur": 20_000_000, "note": "Key center-back loss"},

            {"player": "Vanderson", "team": "Brazil", "club": "Monaco", "position": "RB",
             "injury": "Thigh injury", "impact_level": "low",
             "market_value_eur": None, "note": "Rotation depth reduced"},

            # France
            {"player": "Hugo Ekitike", "team": "France", "club": "PSG/Rennes", "position": "FW",
             "injury": "Achilles tendon tear", "impact_level": "high",
             "market_value_eur": 80_000_000, "note": "23-year-old Liverpool striker out"},

            # Germany
            {"player": "Serge Gnabry", "team": "Germany", "club": "Bayern Munich", "position": "FW",
             "injury": "Adductor tear", "impact_level": "medium",
             "market_value_eur": 18_000_000, "note": "Most-capped attacker in qualifiers (8 apps)"},

            {"player": "Marc-Andre ter Stegen", "team": "Germany", "club": "Barcelona", "position": "GK",
             "injury": "Thigh injury", "impact_level": "medium",
             "market_value_eur": 400_000, "note": "Neuer (age 40) recalled as #1"},

            {"player": "Lennart Karl", "team": "Germany", "club": "Bayern Munich", "position": "FW",
             "injury": "Training injury", "impact_level": "medium",
             "market_value_eur": 60_000_000, "note": "18-year-old Bayern prospect, speed and creativity loss"},

            # Netherlands
            {"player": "Xavi Simons", "team": "Netherlands", "club": "RB Leipzig", "position": "AM/FW",
             "injury": "ACL tear", "impact_level": "high",
             "market_value_eur": 40_000_000, "note": "Most creative player in Koeman's system"},

            {"player": "Jurrien Timber", "team": "Netherlands", "club": "Arsenal", "position": "FB/CB",
             "injury": "Groin injury (recurrence)", "impact_level": "high",
             "market_value_eur": 70_000_000, "note": "Confirmed out June 9, 7000万欧 Arsenal defender"},

            {"player": "Jerdy Schouten", "team": "Netherlands", "club": "PSV", "position": "CM",
             "injury": "ACL tear", "impact_level": "high",
             "market_value_eur": None, "note": "Midfield anchor lost"},

            {"player": "Matthijs de Ligt", "team": "Netherlands", "club": "Manchester United", "position": "CB",
             "injury": "Back injury", "impact_level": "medium",
             "market_value_eur": 30_000_000, "note": "Key defensive loss alongside Van Dijk"},

            # Japan
            {"player": "Kaoru Mitoma", "team": "Japan", "club": "Brighton", "position": "LW",
             "injury": "Hamstring tear", "impact_level": "high",
             "market_value_eur": 22_000_000, "note": "Japan's most dangerous winger out"},

            {"player": "Takumi Minamino", "team": "Japan", "club": "Monaco", "position": "AM/FW",
             "injury": "ACL tear", "impact_level": "high",
             "market_value_eur": 10_000_000, "note": "Both wings of Japan's attack gone"},

            # Spain
            {"player": "Samu Aghehowa", "team": "Spain", "club": "Porto", "position": "FW",
             "injury": "ACL tear", "impact_level": "medium",
             "market_value_eur": None, "note": "Rotation forward out"},

            {"player": "Fermin Lopez", "team": "Spain", "club": "Barcelona", "position": "CM",
             "injury": "Foot fracture", "impact_level": "medium",
             "market_value_eur": 100_000_000, "note": "Barca and Spain future core out"},

            # Ghana
            {"player": "Mohammed Kudus", "team": "Ghana", "club": "Tottenham", "position": "AM",
             "injury": "Quadriceps (surgery required)", "impact_level": "high",
             "market_value_eur": 50_000_000, "note": "Ghana's only creative engine out since January"},

            {"player": "Alexander Djiku", "team": "Ghana", "club": "Fenerbahce", "position": "CB",
             "injury": "Unknown", "impact_level": "medium",
             "market_value_eur": None, "note": "Experienced center-back out"},

            # Scotland
            {"player": "Billy Gilmour", "team": "Scotland", "club": "Napoli", "position": "CM",
             "injury": "Right knee ligament damage (non-contact)", "impact_level": "high",
             "market_value_eur": None, "note": "Core midfielder out, Scotland's 28-year WC return hurt"},

            # USA
            {"player": "Patrick Agyemang", "team": "USA", "club": "Charlotte FC", "position": "FW",
             "injury": "Achilles tear", "impact_level": "low",
             "market_value_eur": None, "note": "Host nation forward depth reduced"},

            {"player": "Johnny Cardoso", "team": "USA", "club": "Real Betis", "position": "CM",
             "injury": "Ankle sprain", "impact_level": "medium",
             "market_value_eur": None, "note": "Midfield rotation loss"},

            # Canada
            {"player": "Marcelo Flores", "team": "Canada", "club": "Tigres UANL", "position": "FW",
             "injury": "ACL rupture (right knee)", "impact_level": "medium",
             "market_value_eur": None, "note": "Just named to 26-man squad, then injured in Concacaf Champions Cup final"},

            # Mexico
            {"player": "Jesus Orozco Chiquete", "team": "Mexico", "club": "Guadalajara", "position": "DEF",
             "injury": "Ankle injury", "impact_level": "medium",
             "market_value_eur": None, "note": "Defensive depth loss"},

            {"player": "Rodrigo Huescas", "team": "Mexico", "club": "Cruz Azul", "position": "DEF",
             "injury": "Knee injury", "impact_level": "medium",
             "market_value_eur": None, "note": "Defensive depth loss"},

            {"player": "Luis Angel Malagon", "team": "Mexico", "club": "Club America", "position": "GK",
             "injury": "Achilles tear", "impact_level": "medium",
             "market_value_eur": None, "note": "Goalkeeping depth reduced"},

            # Colombia
            {"player": "Yaser Asprilla", "team": "Colombia", "club": "Galatasaray/Girona", "position": "MF",
             "injury": "Knee effusion", "impact_level": "low",
             "market_value_eur": None, "note": "Failed to recover from April knee swelling"},

            {"player": "Cristian Borja", "team": "Colombia", "club": "Club America", "position": "LB",
             "injury": "MCL tear (right knee)", "impact_level": "medium",
             "market_value_eur": None, "note": "Injured in Liga MX playoff first leg"},
        ],

        "doubtful_or_carrying_injury": [
            # Argentina - 9 players with injuries at Kansas City camp
            {"player": "Lionel Messi", "team": "Argentina", "club": "Inter Miami", "position": "FW",
             "injury": "Left hamstring overload", "impact_level": "medium",
             "note": "Will miss Honduras friendly, may appear in 2nd warm-up. Diagnosis: overload only, not a tear"},

            {"player": "Emiliano Martinez", "team": "Argentina", "club": "Aston Villa", "position": "GK",
             "injury": "Right ring finger fracture", "impact_level": "medium",
             "note": "Fractured in Europa League final warm-up, training with splint, may start on bench"},

            {"player": "Gonzalo Montiel", "team": "Argentina", "club": "Flamengo", "position": "RB",
             "injury": "Grade 2 quadriceps tear (left)", "impact_level": "high",
             "note": "Highest risk of replacement among Argentina's 9 injured players"},

            {"player": "Nahuel Molina", "team": "Argentina", "club": "Atletico Madrid", "position": "RB",
             "injury": "Grade 1 hamstring tear (left)", "impact_level": "medium",
             "note": "Both starting RBs injured; Scaloni emergency-called Capaldo"},

            {"player": "Cristian Romero", "team": "Argentina", "club": "Tottenham", "position": "CB",
             "injury": "Right knee lateral ligament", "impact_level": "medium",
             "note": "Recovering well, joined team training, likely for warm-up match"},

            {"player": "Leandro Paredes", "team": "Argentina", "club": "Roma", "position": "CM",
             "injury": "Severe right leg muscle spasm", "impact_level": "low",
             "note": "Initially rumored as hamstring tear, denied. Target: group stage fit"},

            {"player": "Julian Alvarez", "team": "Argentina", "club": "Atletico Madrid", "position": "FW",
             "injury": "Ankle sprain (UCL semifinal)", "impact_level": "low",
             "note": "Season ended early but now in normal training"},

            {"player": "Thiago Almada", "team": "Argentina", "club": "Corinthians", "position": "AM",
             "injury": "Muscle overload", "impact_level": "low",
             "note": "Confirmed resolved"},

            {"player": "Nico Paz", "team": "Argentina", "club": "Torino", "position": "AM/FW",
             "injury": "Left knee contusion", "impact_level": "low",
             "note": "Participating normally in training"},

            # France
            {"player": "William Saliba", "team": "France", "club": "Arsenal", "position": "CB",
             "injury": "Unknown (aggravated in UCL final, played 120 min)", "impact_level": "high",
             "note": "French FA 'deeply concerned'. Konate to deputize. May miss group stage"},

            {"player": "Ibrahima Konate", "team": "France", "club": "Liverpool", "position": "CB",
             "injury": "Minor knocks (end of season)", "impact_level": "medium",
             "note": "Elevated to starter if Saliba out, but himself not 100%"},

            # Spain
            {"player": "Lamine Yamal", "team": "Spain", "club": "Barcelona", "position": "RW",
             "injury": "Muscle tear", "impact_level": "medium",
             "note": "Recovery progressing well, target: Group stage opener vs Cape Verde. De la Fuente confirmed"},

            {"player": "Nico Williams", "team": "Spain", "club": "Athletic Bilbao", "position": "LW",
             "injury": "Grade 1 strain", "impact_level": "low",
             "note": "Near full recovery, same target as Yamal"},

            {"player": "Mikel Merino", "team": "Spain", "club": "Arsenal", "position": "CM",
             "injury": "Stress fracture", "impact_level": "low",
             "note": "Recovery described as 'perfect', to get minutes vs Iraq friendly"},

            # Brazil
            {"player": "Neymar", "team": "Brazil", "club": "Santos", "position": "FW/AM",
             "injury": "Grade 2 calf muscle strain (right)", "impact_level": "high",
             "note": "MRI confirmed partial fiber tear. 2-3 week recovery. Out of both warm-ups. "
                    "Doubtful for opener vs Morocco June 13. Ancelotti won't replace him in squad"},

            # Uruguay
            {"player": "Darwin Nunez", "team": "Uruguay", "club": "Al Hilal", "position": "FW",
             "injury": "No match fitness (no games since Feb 2026)", "impact_level": "high",
             "note": "Removed from Saudi league roster in Feb. 13-match NT goal drought. Bielsa still selected him"},

            {"player": "Giorgian De Arrascaeta", "team": "Uruguay", "club": "Flamengo", "position": "AM",
             "injury": "Right collarbone fracture", "impact_level": "high",
             "note": "Selected with injury, recovery progress critical for Uruguay's attack"},

            {"player": "Federico Valverde", "team": "Uruguay", "club": "Real Madrid", "position": "CM",
             "injury": "Head trauma (conflict with Tchouameni)", "impact_level": "medium",
             "note": "Captain, needs careful pre-tournament assessment"},

            # Belgium
            {"player": "Romelu Lukaku", "team": "Belgium", "club": "Napoli", "position": "FW",
             "injury": "Season-long injury issues", "impact_level": "high",
             "note": "In squad but not match-fit to start. Garcia's 'experience gamble'"},

            # Ivory Coast
            {"player": "Odilon Kossounou", "team": "Ivory Coast", "club": "Atalanta", "position": "CB",
             "injury": "Uncertain fitness", "impact_level": "medium",
             "note": "Key to Fae's 4-3-3 high press defensive depth"},
        ],

        "injury_impact_ranking": [
            {"rank": 1, "team": "France", "note": "Saliba injury most concerning. Konate capable deputy but Saliba-Upamecano partnership was settled"},
            {"rank": 2, "team": "Brazil", "note": "Lost Rodrygo + Estevao. Neymar may miss opener. Attack rotation severely depleted"},
            {"rank": 3, "team": "Argentina", "note": "Longest injury list (9 players) but most injuries are mild. Key axis at risk if RBs don't recover"},
            {"rank": 4, "team": "Netherlands", "note": "Simons + Schouten + De Ligt + Timber = midfield and defense gutted. Worst relative to squad size"},
            {"rank": 5, "team": "Spain", "note": "Yamal and Nico recovering well. Core (Rodri, Pedri, Laporte) all healthy. Least impact among top 5"},
            {"rank": 6, "team": "England", "note": "No core-level injury exits. Foden/Palmer/Arnold/Maguire drops are tactical (Tuchel), not medical"},
            {"rank": 7, "team": "Japan", "note": "Both wing souls (Mitoma + Minamino) gone. Moriyasu must restructure entire tactical framework"},
            {"rank": 8, "team": "Germany", "note": "Gnabry + Karl + ter Stegen out. Musiala returns from injury to fill gap"},
        ],
    },

    # =========================================================================
    # 2. WEATHER FORECASTS
    # =========================================================================
    "weather": {
        "_summary": "2026 WC will be the most heat-threatened tournament in history. WWA predicts 26 of 104 "
                    "matches may hit WBGT>=26C (danger threshold). 5 matches may exceed WBGT 28C (extreme). "
                    "FIFA implementing mandatory 3-min hydration breaks per half for ALL matches — a first.",

        "venue_forecasts": [
            # US venues
            {"venue": "Dallas (Arlington) — AT&T Stadium", "city": "Dallas, TX", "country": "USA",
             "matches": 9, "expected_temp_c_june": 35, "expected_temp_c_july": 37,
             "humidity_pct": "60-80", "wbgt_estimate_c": 28,
             "heat_risk": "extreme",
             "note": "Most matches of any venue. Summer temps regularly exceed 35C. Indoor stadium but field exposed"},

            {"venue": "Miami — Hard Rock Stadium", "city": "Miami, FL", "country": "USA",
             "matches": None, "expected_temp_c_june": 33, "expected_temp_c_july": 34,
             "humidity_pct": "70-85", "wbgt_estimate_c": 29,
             "heat_risk": "extreme",
             "note": "3rd-place match (July 18). Extreme humidity makes WBGT highest of all venues"},

            {"venue": "Atlanta — Mercedes-Benz Stadium", "city": "Atlanta, GA", "country": "USA",
             "matches": None, "expected_temp_c_june": 33, "expected_temp_c_july": 35,
             "humidity_pct": "60-75", "wbgt_estimate_c": 27,
             "heat_risk": "high",
             "note": "Semifinal host. Hot and humid summer climate"},

            {"venue": "Houston — NRG Stadium", "city": "Houston, TX", "country": "USA",
             "matches": None, "expected_temp_c_june": 34, "expected_temp_c_july": 36,
             "humidity_pct": "65-80", "wbgt_estimate_c": 28,
             "heat_risk": "extreme",
             "note": "Central division, extreme heat + humidity combination"},

            {"venue": "Kansas City — Arrowhead Stadium", "city": "Kansas City, MO", "country": "USA",
             "matches": None, "expected_temp_c_june": 31, "expected_temp_c_july": 34,
             "humidity_pct": "55-70", "wbgt_estimate_c": 26,
             "heat_risk": "high",
             "note": "Argentina group stage base. Netherlands team doctor specifically flagged this venue"},

            {"venue": "Los Angeles — SoFi Stadium", "city": "Los Angeles, CA", "country": "USA",
             "matches": None, "expected_temp_c_june": 28, "expected_temp_c_july": 30,
             "humidity_pct": "40-55", "wbgt_estimate_c": 22,
             "heat_risk": "moderate",
             "note": "Western division, dry heat, more manageable"},

            {"venue": "San Francisco Bay Area — Levi's Stadium", "city": "Santa Clara, CA", "country": "USA",
             "matches": None, "expected_temp_c_june": 24, "expected_temp_c_july": 26,
             "humidity_pct": "45-60", "wbgt_estimate_c": 19,
             "heat_risk": "low",
             "note": "Cool coastal climate, 72km from SF downtown"},

            {"venue": "Seattle — Lumen Field", "city": "Seattle, WA", "country": "USA",
             "matches": None, "expected_temp_c_june": 22, "expected_temp_c_july": 25,
             "humidity_pct": "50-65", "wbgt_estimate_c": 18,
             "heat_risk": "low",
             "note": "One of the coolest venues, minimal heat concern"},

            {"venue": "New York/New Jersey — MetLife Stadium", "city": "East Rutherford, NJ", "country": "USA",
             "matches": None, "expected_temp_c_june": 28, "expected_temp_c_july": 31,
             "humidity_pct": "55-70", "wbgt_estimate_c": 24,
             "heat_risk": "moderate",
             "note": "Final match venue (July 19). Can be humid in July"},

            {"venue": "Philadelphia — Lincoln Financial Field", "city": "Philadelphia, PA", "country": "USA",
             "matches": None, "expected_temp_c_june": 28, "expected_temp_c_july": 31,
             "humidity_pct": "55-70", "wbgt_estimate_c": 24,
             "heat_risk": "moderate",
             "note": "Similar to NYC climate"},

            {"venue": "Boston — Gillette Stadium", "city": "Foxborough, MA", "country": "USA",
             "matches": None, "expected_temp_c_june": 26, "expected_temp_c_july": 29,
             "humidity_pct": "55-65", "wbgt_estimate_c": 22,
             "heat_risk": "low",
             "note": "Northern venue, relatively cool"},

            # Canadian venues
            {"venue": "Toronto — BMO Field", "city": "Toronto, ON", "country": "Canada",
             "matches": None, "expected_temp_c_june": 24, "expected_temp_c_july": 27,
             "humidity_pct": "50-65", "wbgt_estimate_c": 20,
             "heat_risk": "low",
             "note": "Cool climate advantage for teams based here"},

            {"venue": "Vancouver — BC Place", "city": "Vancouver, BC", "country": "Canada",
             "matches": None, "expected_temp_c_june": 21, "expected_temp_c_july": 24,
             "humidity_pct": "50-65", "wbgt_estimate_c": 17,
             "heat_risk": "very_low",
             "note": "Coolest venue of the tournament"},

            # Mexican venues
            {"venue": "Mexico City — Estadio Azteca", "city": "Mexico City", "country": "Mexico",
             "matches": None, "expected_temp_c_june": 26, "expected_temp_c_july": 24,
             "humidity_pct": "45-60", "wbgt_estimate_c": 20,
             "heat_risk": "moderate",
             "note": "Opening match (June 11). Altitude 2240m is the bigger factor than heat"},

            {"venue": "Monterrey — Estadio BBVA", "city": "Monterrey", "country": "Mexico",
             "matches": None, "expected_temp_c_june": 35, "expected_temp_c_july": 36,
             "humidity_pct": "50-65", "wbgt_estimate_c": 27,
             "heat_risk": "high",
             "note": "Very hot, less humid than Dallas but still dangerous"},

            {"venue": "Guadalajara — Estadio Akron", "city": "Guadalajara", "country": "Mexico",
             "matches": None, "expected_temp_c_june": 31, "expected_temp_c_july": 29,
             "humidity_pct": "45-60", "wbgt_estimate_c": 23,
             "heat_risk": "moderate",
             "note": "Warm but manageable"},
        ],

        "high_risk_groups": [
            {"group": "K", "teams": ["Portugal", "..."], "venue": "Dallas",
             "wbgt_over_26_probability": 0.80,
             "note": "Portugal's 3 group matches ALL in Dallas. 80% chance of WBGT>=26C for each match"},

            {"group": "J", "teams": ["Argentina", "Algeria", "Austria", "Jordan"],
             "venues": ["Kansas City", "Dallas"],
             "wbgt_over_26_probability": 0.74,
             "note": "Argentina plays Algeria in KC, Austria and Jordan in Dallas"},

            {"group": "L", "teams": ["England", "Croatia", "Ghana", "Panama"],
             "venue": "Dallas (2 matches)",
             "wbgt_over_26_probability": 0.70,
             "note": "England has 2 group matches in Dallas"},

            {"cool_advantage_groups": [
                {"teams": ["Canada", "Switzerland", "Bosnia-Herzegovina"],
                 "note": "All group matches in cool Canadian cities, zero heat threat"},
            ]},
        ],

        "fifa_heat_protocols": {
            "mandatory_hydration_breaks": "3 minutes per half for ALL matches (first in WC history)",
            "wbgte_28_threshold": "Evaluate adjusting kickoff time",
            "wbgte_32_threshold": "Match postponement or relocation (extreme protocol)",
            "bench_air_conditioning": "Air-conditioned substitute benches at outdoor venues",
            "fan_zones": "Misting systems and free water stations",
            "scientist_warning": "20+ scientists from Imperial College London signed open letter: "
                                "WBGT>28 should trigger postponement, hydration breaks should be 6 min not 3",
        },
    },

    # =========================================================================
    # 3. COACH STATEMENTS / TACTICAL HINTS
    # =========================================================================
    "coach_statements": [
        {"team": "Netherlands", "coach": "Ronald Koeman", "tactical_hint": "4-3-3 restructure needed",
         "statement": "Simons was a key piece of our tactical system. His absence forces us to rethink central attack patterns. "
                      "Gravenberch will take on more progression responsibility; Gakpo may drop deeper to participate in build-up.",
         "source": "Pre-tournament press conference", "date": "2026-06-08"},

        {"team": "Spain", "coach": "Luis de la Fuente", "tactical_hint": "Yamal recovery on track, no Real Madrid players",
         "statement": "Yamal's recovery plan is progressing ideally. Our target is the Cape Verde opener. "
                      "The 26-man list has zero Real Madrid players — a first in Spain's WC history.",
         "source": "Squad announcement press conference", "date": "2026-05-25"},

        {"team": "France", "coach": "Didier Deschamps", "tactical_hint": "Midfield age concerns, Konate elevated",
         "statement": "When asked about aging midfield (Kante 35), Deschamps defended selections but Rabiot admitted "
                      "post-Ivory Coast loss that 'midfield coordination is not yet fluent'.",
         "source": "Post-friendly press conference", "date": "2026-06-07"},

        {"team": "Brazil", "coach": "Carlo Ancelotti", "tactical_hint": "Neymar won't be replaced despite injury",
         "statement": "Ancelotti confirmed he will NOT replace Neymar in the squad despite Grade 2 calf strain. "
                      "Neymar (34) will carry extra creative burden with Rodrygo and Estevao out.",
         "source": "Squad announcement", "date": "2026-05-19"},

        {"team": "Argentina", "coach": "Lionel Scaloni", "tactical_hint": "Optimistic on all 9 injured players; no squad changes",
         "statement": "Scaloni expressed optimism all 9 injured players can recover before the Algeria opener (June 16). "
                      "Plans no roster changes. Emergency-called Capaldo due to both RBs injured.",
         "source": "Kansas City camp briefing", "date": "2026-06-06"},

        {"team": "Germany", "coach": "Julian Nagelsmann", "tactical_hint": "Must-rebound mentality, Musiala fills Gnabry gap",
         "statement": "After two consecutive group-stage exits, Germany carries 'must-rebound' pressure. "
                      "Musiala returning from injury to fill Gnabry's right-sided role.",
         "source": "Squad announcement press conference", "date": "2026-05-21"},

        {"team": "England", "coach": "Thomas Tuchel", "tactical_hint": "Bold drops of established stars",
         "statement": "Tuchel dropped Foden, Palmer, Alexander-Arnold, and Maguire from the 26-man squad — "
                      "tactical choices, not injuries. Key risk: managing these stars' morale on the bench if recalled.",
         "source": "Squad announcement", "date": "2026-05-22"},

        {"team": "Uruguay", "coach": "Marcelo Bielsa", "tactical_hint": "Trust in Nunez despite 4-month layoff",
         "statement": "Bielsa selected Nunez despite no club matches since February and a 13-match NT goal drought. "
                      "Hopes he can 'quickly regain form before the World Cup'.",
         "source": "Squad announcement", "date": None},

        {"team": "Netherlands", "coach": "Team doctor Edwin Terwindt", "tactical_hint": "Heat acclimatization protocol",
         "statement": "The real challenge is not high temperature but high humidity — it prevents the body from cooling "
                      "through sweat. Team plans sauna training and a 3-stage route: Netherlands -> New York -> Kansas City "
                      "for gradual acclimatization.",
         "source": "Medical briefing", "date": None},

        {"team": "Belgium", "coach": "Rudi Garcia", "tactical_hint": "Experience gamble on Lukaku",
         "statement": "Garcia selected injured Lukaku as Belgium's only target-man option. Described as the ultimate "
                      "'experience is king' gamble.",
         "source": "Squad announcement", "date": "2026-05-15"},
    ],

    # =========================================================================
    # 4. FRIENDLY MATCH RESULTS (Warm-up Games)
    # =========================================================================
    "friendly_results": [
        {"team1": "France", "team2": "Ivory Coast", "score": "1-2",
         "date": "2026-06-05", "venue": "France",
         "note": "Major upset. France lost at home. 19-year-old Diomande (Bundesburg) scored and assisted. "
                 "French defense exposed. Rabiot admitted midfield coordination issues."},

        {"team1": "France", "team2": "Northern Ireland", "score": "3-1",
         "date": "2026-06-09", "venue": "Lille, Pierre Mauroy Stadium",
         "note": "Olise hat-trick. France bounced back but against weak opposition. Mbappe active."},

        {"team1": "Spain", "team2": "Iraq", "score": "1-1",
         "date": "2026-06-07", "venue": None,
         "note": "Draw. Spain testing tactics vs Saudi-style opponent. Zero Real Madrid players in squad. "
                 "4 UCL finalists returned late, not fully fit. Iraq played well under WCQ pressure."},

        {"team1": "Sweden", "team2": "Greece", "score": "2-2",
         "date": "2026-06-07", "venue": None,
         "note": "Sweden came back from 0-1 down. Isak + Gyokeres started and scored. "
                 "Late equalizer in stoppage time. Coach still deciding starting XI for tournament."},

        {"team1": "China", "team2": "Thailand", "score": "0-0",
         "date": "2026-06-09", "venue": "Jinhua Sports Center",
         "note": "Friendly. Zhang Yuning hit the post in first half. No goals in second half."},

        {"team1": "USA", "team2": "Ecuador", "score": None,
         "date": "2025-10", "venue": "Q2 Stadium, Austin TX",
         "note": "October FIFA date friendly. Part of US build-up as host nation."},

        {"team1": "Brazil", "team2": "Japan", "score": None,
         "date": None, "venue": None,
         "note": "Friendly match previewed as part of both nations' WC preparation. Both already qualified."},
    ],

    # =========================================================================
    # 5. TRAVEL UPDATES
    # =========================================================================
    "travel_updates": [
        {"team": "Argentina", "base_camp": "Kansas City", "country": "USA",
         "group_venues": ["Kansas City", "Dallas"],
         "travel_note": "9 injured players arrived at KC training base. Scaloni plans no roster changes. "
                        "Group J: Algeria (KC June 16), Austria (Dallas June 22), Jordan (Dallas June 27). "
                        "Dallas-KC distance ~800km. Heat acclimatization critical for Dallas matches."},

        {"team": "Netherlands", "base_camp": "New York (transit) -> Kansas City",
         "country": "USA",
         "group_venues": ["Kansas City", "Dallas"],
         "travel_note": "3-stage acclimatization route: Netherlands -> New York -> Kansas City. "
                        "Team doctor specifically designed gradual heat exposure. "
                        "Sauna training in Netherlands before departure."},

        {"team": "Portugal", "base_camp": "Dallas area", "country": "USA",
         "group_venues": ["Dallas (all 3 group matches)"],
         "travel_note": "All 3 group matches in Dallas — highest WBGT risk (80% chance >=26C). "
                        "Cristiano Ronaldo (41) playing in 6th WC faces extreme heat challenge."},

        {"team": "England", "base_camp": None, "country": "USA",
         "group_venues": ["Dallas (2 matches)"],
         "travel_note": "Group L with Croatia, Ghana, Panama. 2 matches in Dallas (~70% heat risk)."},

        {"team": "Canada", "base_camp": "Toronto/Vancouver", "country": "Canada",
         "group_venues": ["Toronto", "Vancouver"],
         "travel_note": "Cool climate advantage. All group matches in Canadian cities."},

        {"team": "Mexico", "base_camp": "Mexico City", "country": "Mexico",
         "group_venues": ["Mexico City", "Guadalajara"],
         "travel_note": "Home advantage. Azteca altitude (2240m) is bigger factor than heat for visiting teams."},
    ],

    # =========================================================================
    # 6. ODDS MOVEMENTS
    # =========================================================================
    "odds_movements": {
        "_summary": "Spain and France lead as co-favorites. Brazil's odds drifted after Rodrygo/Estevao injuries. "
                    "Netherlands odds lengthened significantly. Norway emerged as dark horse.",

        "outright_winner_odds": [
            {"team": "Spain", "odds": 4.00, "movement": "stable",
             "note": "Top favorite. Core squad healthy. Yamal recovery on track"},

            {"team": "France", "odds": 4.30, "movement": "slight_drift",
             "note": "Drifted after Ivory Coast friendly loss and Saliba injury concern"},

            {"team": "England", "odds": 5.00, "movement": "stable",
             "note": "Tuchel's bold squad selection. No injury hits. Highest squad completeness"},

            {"team": "Brazil", "odds": 6.25, "movement": "drifted_out",
             "note": "Significant drift after Rodrygo ACL + Estevao hamstring. Neymar doubtful for opener"},

            {"team": "Argentina", "odds": 6.25, "movement": "slight_drift",
             "note": "9 injuries at camp but most mild. Messi confirmed participating"},

            {"team": "Portugal", "odds": 8.25, "movement": "stable",
             "note": "All 3 group matches in Dallas heat (80% WBGT risk). Ronaldo 6th WC at age 41"},

            {"team": "Germany", "odds": 9.00, "movement": "slight_drift",
             "note": "Gnabry/Karl/ter Stegen losses. Must-rebound from 2 group-stage exits"},

            {"team": "Netherlands", "odds": 7.00, "movement": "drifted_out",
             "note": "Significant drift after Simons/De Ligt/Schouten/Timber injuries. Midfield gutted"},

            {"team": "Norway", "odds": None, "movement": "shortened",
             "note": "Dark horse. Haaland + Odegaard. Shortened from long odds after strong qualifying"},

            {"team": "Belgium", "odds": 20.00, "movement": "stable",
             "note": "Lukaku injury gamble. De Bruyne (Napoli) captain. Outside chance"},
        ],

        "key_market_movements": [
            {"market": "Brazil outright", "direction": "drifted", "trigger": "Rodrygo ACL + Estevao out",
             "magnitude": "significant", "date": "2026-05-19"},

            {"market": "Netherlands outright", "direction": "drifted", "trigger": "Simons ACL + Timber groin",
             "magnitude": "significant", "date": "2026-06-09"},

            {"market": "France outright", "direction": "slight_drift", "trigger": "Saliba injury + Ivory Coast loss",
             "magnitude": "moderate", "date": "2026-06-07"},

            {"market": "Norway outright", "direction": "shortened", "trigger": "Strong qualifying + Haaland form",
             "magnitude": "moderate", "date": None},

            {"market": "Group K - Portugal heat risk", "direction": "under_performance_expected",
             "trigger": "80% WBGT>=26C for all 3 group matches in Dallas",
             "magnitude": "notable", "date": None},
        ],
    },

    # =========================================================================
    # 7. SQUAD ANNOUNCEMENTS (Confirmed 26-man lists)
    # =========================================================================
    "squad_announcements": {
        "Spain": {"coach": "Luis de la Fuente", "announcement_date": "2026-05-25",
                  "note": "Zero Real Madrid players — first in Spain WC history. Yamal (18, 180M EUR) headline star"},
        "France": {"coach": "Didier Deschamps", "announcement_date": "2026-05-15",
                   "note": "Mbappe, Dembele, Olise headline. Kante (35) selected. Saliba concern"},
        "England": {"coach": "Thomas Tuchel", "announcement_date": "2026-05-22",
                    "note": "Foden, Palmer, Alexander-Arnold, Maguire DROPPED (tactical). Bellingham, Rice core"},
        "Brazil": {"coach": "Carlo Ancelotti", "announcement_date": "2026-05-19",
                   "note": "Neymar returns at 34. Vinicius + Raphinha lead attack. Rodrygo initially listed then injured"},
        "Argentina": {"coach": "Lionel Scaloni", "announcement_date": "2026-05-30 (projected)",
                      "note": "55-player preliminary list. 9 injured at camp. Messi confirmed for WC"},
        "Portugal": {"coach": "Roberto Martinez", "announcement_date": "2026-05-19",
                     "note": "Cristiano Ronaldo (41) 6th World Cup. All group matches in Dallas"},
        "Germany": {"coach": "Julian Nagelsmann", "announcement_date": "2026-05-21",
                    "note": "Neuer (40) recalled as #1 GK. Wirtz + Musiala lead new generation"},
        "Netherlands": {"coach": "Ronald Koeman", "announcement_date": "2026-05-27",
                        "note": "Van Dijk, Gakpo, De Jong core. Simons confirmed OUT before announcement"},
        "Norway": {"coach": "Stale Solbakken", "announcement_date": "2026-05-22",
                   "note": "Haaland + Odegaard headline. Dark horse of the tournament"},
        "Belgium": {"coach": "Rudi Garcia", "announcement_date": "2026-05-15",
                    "note": "De Bruyne captain. Lukaku selected despite injury. Courtois in goal"},
    },
}


def get_research_summary() -> Dict[str, Any]:
    """
    Generate a structured summary of all research findings.

    Returns:
        Dict with sections: overview, key_injuries, weather_risks, tactical_insights,
        friendly_surprises, odds_shifts, and critical_watch_items.
    """
    data = DEEP_RESEARCH_DATA

    confirmed_out = data["injuries"]["confirmed_out"]
    doubtful = data["injuries"]["doubtful_or_carrying_injury"]

    # Count injuries by team
    injury_counts: Dict[str, int] = {}
    for p in confirmed_out:
        injury_counts[p["team"]] = injury_counts.get(p["team"], 0) + 1
    for p in doubtful:
        injury_counts[p["team"]] = injury_counts.get(p["team"], 0) + 1

    # High-impact injuries
    high_impact_confirmed = [p for p in confirmed_out if p["impact_level"] == "high"]
    high_impact_doubtful = [p for p in doubtful if p["impact_level"] == "high"]

    # Extreme heat venues
    extreme_venues = [v for v in data["weather"]["venue_forecasts"] if v["heat_risk"] in ("extreme",)]

    return {
        "overview": {
            "tournament": "FIFA World Cup 2026 (USA/Canada/Mexico)",
            "dates": "June 11 - July 19, 2026",
            "teams": 48,
            "matches": 104,
            "research_date": data["_meta"]["research_date"],
        },

        "key_injuries": {
            "total_confirmed_out": len(confirmed_out),
            "total_doubtful": len(doubtful),
            "high_impact_confirmed": len(high_impact_confirmed),
            "high_impact_doubtful": len(high_impact_doubtful),
            "worst_affected_teams": sorted(injury_counts.items(), key=lambda x: -x[1])[:8],
            "biggest_single_losses": [
                "Rodrygo (Brazil, ACL) — attack destroyed",
                "Xavi Simons (Netherlands, ACL) — creativity hub gone",
                "Hugo Ekitike (France, Achilles) — 80M EUR striker out",
                "Kaoru Mitoma (Japan, hamstring) — wing threat eliminated",
                "Mohammed Kudus (Ghana, quad surgery) — only creative engine out",
            ],
        },

        "weather_risks": {
            "matches_with_wbgt_over_26": 26,
            "matches_with_wbgt_over_28": 5,
            "extreme_heat_venues": [v["venue"] for v in extreme_venues],
            "highest_risk_group": "Group K (Portugal) — 80% WBGT>=26C probability",
            "fifa_first": "Mandatory 3-min hydration breaks per half for ALL matches",
            "scientist_warning": "20+ scientists demand 6-min breaks and postponement at WBGT>28",
        },

        "tactical_insights": [
            "Netherlands: 4-3-3 restructure without Simons; Gravenberch elevated, Gakpo drops deeper",
            "Spain: Zero Real Madrid players — unprecedented; Yamal (18) as focal point",
            "France: Midfield age concern (Kante 35); Saliba absence may force defensive reshuffle",
            "England: Tuchel's bold drops (Foden/Palmer) — locker room management is key risk",
            "Brazil: Neymar must carry extra load with Rodrygo/Estevao out; may miss opener",
            "Argentina: 9 injuries but mostly mild; both RBs injured is biggest structural risk",
            "Uruguay: Nunez has 4-month match drought + 13-game NT goal drought — Bielsa's biggest gamble",
            "Germany: Must-rebound from 2 group-stage exits; Musiala fills Gnabry gap",
        ],

        "friendly_surprises": [
            "France 1-2 Ivory Coast — major upset, defensive frailty exposed",
            "Spain 1-1 Iraq — draw against lower-ranked opponent, testing Saudi-style tactics",
            "France 3-1 Northern Ireland — Olise hat-trick bounce-back (weak opposition)",
            "Sweden 2-2 Greece — late comeback, Isak+Gyokeres both scored",
        ],

        "odds_shifts": {
            "biggest_drift": "Brazil (6.25, drifted after Rodrygo/Estevao injuries)",
            "second_drift": "Netherlands (7.00, drifted after Simons/Timber injuries)",
            "shortened": "Norway (dark horse, Haaland+Odegaard factor)",
            "favorites": "Spain (4.00) and France (4.30) co-favorites",
        },

        "critical_watch_items": [
            "Saliba (France) — MRI result pending, could miss group stage",
            "Neymar (Brazil) — 2-3 week recovery, opener vs Morocco June 13 in doubt",
            "Nunez (Uruguay) — 4 months no matches, form unknown",
            "Messi (Argentina) — hamstring overload, skipping warm-ups",
            "Lukaku (Belgium) — not match-fit, only target-man option",
            "De Arrascaeta (Uruguay) — collarbone fracture, recovery progress",
            "FIFA 24-hour replacement rule — last-minute squad changes still possible",
        ],
    }


def apply_research_to_engine() -> Dict[str, Any]:
    """
    Translate research findings into actionable adjustments for a prediction engine.

    Returns:
        Dict with:
        - elo_adjustments: per-team ELO delta based on injury/weather/coach factors
        - squad_depth_changes: per-team depth rating change (0-1 scale)
        - heat_advantage_matrix: per-team heat adaptation bonus for specific venues
        - tactical_flags: per-team tactical risk/opportunity flags
    """
    data = DEEP_RESEARCH_DATA

    # -------------------------------------------------------------------------
    # ELO adjustments based on injuries (negative = team weakened)
    # -------------------------------------------------------------------------
    elo_adjustments: Dict[str, float] = {}

    # France: Saliba doubtful + Ekitike out + poor friendly form
    elo_adjustments["France"] = -25

    # Brazil: Rodrygo + Estevao + Militao out; Neymar doubtful for opener
    elo_adjustments["Brazil"] = -35

    # Netherlands: Simons + Schouten + De Ligt + Timber all out
    elo_adjustments["Netherlands"] = -40

    # Argentina: 9 injuries but mostly mild; Messi confirmed
    elo_adjustments["Argentina"] = -10

    # Spain: Fermin + Aghehowa out but core intact; Yamal recovering
    elo_adjustments["Spain"] = -5

    # England: No injury hits; Tuchel tactical risk
    elo_adjustments["England"] = 0

    # Germany: Gnabry + Karl + ter Stegen out; must-rebound pressure
    elo_adjustments["Germany"] = -20

    # Japan: Both wings (Mitoma + Minamino) gone
    elo_adjustments["Japan"] = -30

    # Ghana: Kudus + Djiku out
    elo_adjustments["Ghana"] = -25

    # Portugal: All group matches in extreme heat
    elo_adjustments["Portugal"] = -15

    # Uruguay: Nunez 4-month drought + De Arrascaeta injury
    elo_adjustments["Uruguay"] = -20

    # Belgium: Lukaku not match-fit
    elo_adjustments["Belgium"] = -10

    # Scotland: Gilmour out
    elo_adjustments["Scotland"] = -20

    # USA: Host advantage + Agyemang/Cardoso out
    elo_adjustments["USA"] = +10

    # Canada: Cool venue advantage + home support
    elo_adjustments["Canada"] = +10

    # Mexico: Home advantage + altitude
    elo_adjustments["Mexico"] = +15

    # Norway: Dark horse momentum
    elo_adjustments["Norway"] = +5

    # -------------------------------------------------------------------------
    # Squad depth changes (0 = no change, negative = depth reduced)
    # Scale: -1.0 (catastrophic) to +0.5 (boosted)
    # -------------------------------------------------------------------------
    squad_depth_changes: Dict[str, float] = {
        "Netherlands": -0.35,   # Midfield and defense gutted
        "Brazil": -0.30,        # Attack rotation destroyed
        "Japan": -0.30,         # Both wings gone
        "Ghana": -0.25,         # Creative engine + CB out
        "France": -0.20,        # Striker out, CB doubtful
        "Germany": -0.15,       # Attack depth reduced
        "Scotland": -0.20,      # Core midfielder out
        "Argentina": -0.10,     # 9 injuries but mostly mild
        "Spain": -0.05,         # Rotation players out, core intact
        "Uruguay": -0.15,       # Nunez form unknown, De Arrascaeta injured
        "Belgium": -0.10,       # Only target-man not fit
        "Mexico": -0.10,        # 3 players out including GK
        "Colombia": -0.05,      # Asprilla + Borja out
        "England": 0.0,         # No injury losses
        "USA": -0.05,           # Minor depth loss
        "Canada": -0.05,        # Flores out
        "Portugal": 0.0,        # Full squad available
        "Norway": 0.0,          # Full squad available
    }

    # -------------------------------------------------------------------------
    # Heat advantage matrix: bonus/penalty when playing at specific venues
    # Positive = team has advantage, negative = disadvantage
    # Based on climate origin (tropical/subtropical vs temperate)
    # -------------------------------------------------------------------------
    heat_advantage_matrix: Dict[str, Dict[str, float]] = {}

    # Tropical/subtropical teams get heat bonus
    heat_adapted_teams = ["Brazil", "Mexico", "Saudi Arabia", "Ivory Coast", "Ghana",
                          "Panama", "Cape Verde", "Morocco", "Algeria", "Jordan",
                          "Ecuador", "Colombia", "Paraguay", "Uruguay"]
    # Temperate teams get heat penalty
    heat_vulnerable_teams = ["Netherlands", "Germany", "England", "Belgium", "Sweden",
                             "Norway", "Switzerland", "Bosnia-Herzegovina", "Croatia",
                             "Czech Republic", "Scotland", "Austria", "France", "Spain",
                             "Portugal"]

    extreme_venue_names = ["Dallas", "Houston", "Miami", "Atlanta", "Monterrey", "Kansas City"]
    moderate_venue_names = ["Los Angeles", "New York/New Jersey", "Philadelphia",
                            "Mexico City", "Guadalajara"]
    cool_venue_names = ["San Francisco", "Seattle", "Boston", "Toronto", "Vancouver"]

    for team in heat_adapted_teams:
        heat_advantage_matrix[team] = {}
        for venue in extreme_venue_names:
            heat_advantage_matrix[team][venue] = 0.08
        for venue in moderate_venue_names:
            heat_advantage_matrix[team][venue] = 0.03
        for venue in cool_venue_names:
            heat_advantage_matrix[team][venue] = 0.0

    for team in heat_vulnerable_teams:
        heat_advantage_matrix[team] = {}
        for venue in extreme_venue_names:
            heat_advantage_matrix[team][venue] = -0.10
        for venue in moderate_venue_names:
            heat_advantage_matrix[team][venue] = -0.03
        for venue in cool_venue_names:
            heat_advantage_matrix[team][venue] = 0.0

    # Special cases
    heat_advantage_matrix.setdefault("Argentina", {})["Dallas"] = -0.06  # 2 matches in Dallas
    heat_advantage_matrix.setdefault("Argentina", {})["Kansas City"] = -0.04
    heat_advantage_matrix.setdefault("Japan", {})["Dallas"] = -0.08
    heat_advantage_matrix.setdefault("USA", {})["Dallas"] = 0.05  # Home + heat-acclimated

    # -------------------------------------------------------------------------
    # Tactical flags
    # -------------------------------------------------------------------------
    tactical_flags: Dict[str, List[Dict[str, str]]] = {
        "Netherlands": [
            {"flag": "midfield_rebuild", "risk": "high",
             "detail": "4-3-3 system must be restructured without Simons and Schouten"},
        ],
        "Brazil": [
            {"flag": "attack_depth_crisis", "risk": "high",
             "detail": "Neymar (34) must overperform with Rodrygo and Estevao out"},
        ],
        "France": [
            {"flag": "defensive_instability", "risk": "high",
             "detail": "Saliba doubtful, Konate not 100%. May face Germany in R16 with reshuffled defense"},
            {"flag": "midfield_age", "risk": "medium",
             "detail": "Kante (35) in starting XI. Ivory Coast loss exposed coordination issues"},
        ],
        "Argentina": [
            {"flag": "right_back_crisis", "risk": "high",
             "detail": "Both Montiel and Molina injured. Emergency Capaldo call-up"},
            {"flag": "messi_load_management", "risk": "medium",
             "detail": "Skipping warm-ups. Must be managed through group stage"},
        ],
        "Spain": [
            {"flag": "no_real_madrid", "risk": "low",
             "detail": "First WC with zero RM players. New identity. Yamal as focal point"},
        ],
        "England": [
            {"flag": "locker_room_risk", "risk": "medium",
             "detail": "Tuchel dropped Foden/Palmer/Alexander-Arnold. Morale management critical in knockout"},
        ],
        "Uruguay": [
            {"flag": "nunez_form_crisis", "risk": "high",
             "detail": "4 months no matches. 13-game NT goal drought. Bielsa's biggest gamble"},
        ],
        "Germany": [
            {"flag": "must_rebound_pressure", "risk": "medium",
             "detail": "2 consecutive group-stage exits. Psychological pressure is immense"},
        ],
        "Portugal": [
            {"flag": "extreme_heat_group", "risk": "high",
             "detail": "All 3 group matches in Dallas. 80% WBGT>=26C. Ronaldo (41) most affected"},
        ],
        "Japan": [
            {"flag": "tactical_framework_collapse", "risk": "high",
             "detail": "Both wing threats gone. Moriyasu must rebuild entire counter-attacking system"},
        ],
    }

    return {
        "elo_adjustments": elo_adjustments,
        "squad_depth_changes": squad_depth_changes,
        "heat_advantage_matrix": heat_advantage_matrix,
        "tactical_flags": tactical_flags,
        "_methodology": {
            "elo_adjustments": "Negative delta = team weakened. Range: -40 to +15. "
                               "Based on: confirmed injuries, doubtful players, friendly form, "
                               "and home/heat advantage.",
            "squad_depth_changes": "Scale -1.0 to +0.5. Measures impact on positional coverage "
                                   "and rotation quality relative to pre-injury baseline.",
            "heat_advantage_matrix": "Per-team per-venue adjustment. Tropical teams get +0.08 at "
                                     "extreme venues; temperate teams get -0.10. Based on WWA data "
                                     "and ACSM guidelines.",
            "tactical_flags": "Qualitative risk assessments from coach statements and squad analysis.",
        },
    }


# =============================================================================
# Utility functions
# =============================================================================

def get_team_injury_report(team_name: str) -> Dict[str, Any]:
    """Get detailed injury report for a specific team."""
    data = DEEP_RESEARCH_DATA
    confirmed = [p for p in data["injuries"]["confirmed_out"] if p["team"] == team_name]
    doubtful = [p for p in data["injuries"]["doubtful_or_carrying_injury"] if p["team"] == team_name]
    impact_ranking = None
    for entry in data["injuries"]["injury_impact_ranking"]:
        if entry["team"] == team_name:
            impact_ranking = entry
            break

    return {
        "team": team_name,
        "confirmed_out": confirmed,
        "doubtful": doubtful,
        "total_affected": len(confirmed) + len(doubtful),
        "high_impact_count": len([p for p in confirmed + doubtful if p["impact_level"] == "high"]),
        "impact_ranking": impact_ranking,
    }


def get_venue_weather_report(venue_name: str) -> Dict[str, Any]:
    """Get weather/heat risk data for a specific venue."""
    data = DEEP_RESEARCH_DATA
    for venue in data["weather"]["venue_forecasts"]:
        if venue_name.lower() in venue["venue"].lower():
            return venue
    return {"error": f"Venue '{venue_name}' not found"}


def get_heat_adjusted_elo(base_elo: float, team: str, venue: str) -> float:
    """
    Calculate heat-adjusted ELO for a team at a specific venue.

    Args:
        base_elo: Team's base ELO rating
        team: Team name
        venue: Venue city name (e.g., "Dallas", "Miami")

    Returns:
        Adjusted ELO accounting for heat advantage/disadvantage
    """
    adjustments = apply_research_to_engine()
    heat_matrix = adjustments["heat_advantage_matrix"]
    elo_adj = adjustments["elo_adjustments"]

    total_adjustment = 0.0

    # Base injury adjustment (converted to ELO scale)
    total_adjustment += elo_adj.get(team, 0.0)

    # Heat adjustment (converted from probability scale to ELO)
    team_heat = heat_matrix.get(team, {})
    heat_adj = team_heat.get(venue, 0.0)
    total_adjustment += heat_adj * 100  # Scale: 0.10 probability = 10 ELO points

    return base_elo + total_adjustment


if __name__ == "__main__":
    # Print research summary
    summary = get_research_summary()
    print("=" * 70)
    print("WORLD CUP 2026 DEEP RESEARCH SUMMARY")
    print("=" * 70)
    print(f"\nTournament: {summary['overview']['tournament']}")
    print(f"Dates: {summary['overview']['dates']}")
    print(f"Teams: {summary['overview']['teams']} | Matches: {summary['overview']['matches']}")
    print(f"Research date: {summary['overview']['research_date']}")

    print(f"\n--- KEY INJURIES ---")
    print(f"Confirmed OUT: {summary['key_injuries']['total_confirmed_out']}")
    print(f"Doubtful: {summary['key_injuries']['total_doubtful']}")
    print(f"High-impact confirmed: {summary['key_injuries']['high_impact_confirmed']}")
    print(f"High-impact doubtful: {summary['key_injuries']['high_impact_doubtful']}")
    print("Worst affected teams:")
    for team, count in summary["key_injuries"]["worst_affected_teams"]:
        print(f"  {team}: {count} players affected")

    print(f"\n--- WEATHER RISKS ---")
    print(f"Matches with WBGT>=26C: {summary['weather_risks']['matches_with_wbgt_over_26']}/104")
    print(f"Matches with WBGT>=28C: {summary['weather_risks']['matches_with_wbgt_over_28']}/104")
    print(f"Extreme heat venues: {summary['weather_risks']['extreme_heat_venues']}")
    print(f"Highest risk: {summary['weather_risks']['highest_risk_group']}")

    print(f"\n--- ODDS SHIFTS ---")
    print(f"Biggest drift: {summary['odds_shifts']['biggest_drift']}")
    print(f"Shortened: {summary['odds_shifts']['shortened']}")
    print(f"Favorites: {summary['odds_shifts']['favorites']}")

    print(f"\n--- ENGINE ADJUSTMENTS ---")
    engine = apply_research_to_engine()
    print("ELO adjustments:")
    for team, adj in sorted(engine["elo_adjustments"].items(), key=lambda x: x[1]):
        print(f"  {team}: {adj:+.0f}")
