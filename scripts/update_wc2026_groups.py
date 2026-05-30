import json
import sys

DB_PATH = r"d:\My_Code_Projects\Harnessing\projects\world-2026\data\wc2026_player_database.json"

EXISTING_TEAM_GROUPS = {
    "Mexico": "A", "South Korea": "A",
    "Canada": "B", "Switzerland": "B",
    "Brazil": "C", "Morocco": "C",
    "USA": "D", "Australia": "D", "Poland": "D",
    "Germany": "E", "Denmark": "E", "Italy": "E",
    "Netherlands": "F", "Japan": "F", "Tunisia": "F",
    "Belgium": "G", "Egypt": "G", "Iran": "G",
    "Spain": "H", "Saudi Arabia": "H", "Uruguay": "H",
    "France": "I", "Senegal": "I",
    "Argentina": "J",
    "Portugal": "K", "Colombia": "K",
    "England": "L", "Croatia": "L", "Ghana": "L", "Nigeria": "L",
    "Qatar": "B",
}

NEW_TEAMS = {
    "South Africa": {
        "rank": 58, "region": "CAF", "coach": "Hugo Broos",
        "players": [
            {"name": "Mokoena", "position": "MF", "age": 27, "club": "Sundowns", "rating": 72, "goals": 5, "assists": 8, "experience": 2, "form": 3.5, "fitness": 85, "is_xfactor": False, "market_value_m": 3.0},
            {"name": "Modise", "position": "MF", "age": 29, "club": "Orlando Pirates", "rating": 70, "goals": 3, "assists": 6, "experience": 2, "form": 3.3, "fitness": 82, "is_xfactor": False, "market_value_m": 2.0},
            {"name": "Pienaar", "position": "MF", "age": 26, "club": "Sundowns", "rating": 71, "goals": 4, "assists": 7, "experience": 1, "form": 3.4, "fitness": 88, "is_xfactor": False, "market_value_m": 2.5},
            {"name": "Furman", "position": "DM", "age": 32, "club": "SuperSport Utd", "rating": 68, "goals": 1, "assists": 3, "experience": 3, "form": 3.0, "fitness": 78, "is_xfactor": False, "market_value_m": 1.0},
            {"name": "Khune", "position": "GK", "age": 34, "club": "Kaizer Chiefs", "rating": 69, "goals": 0, "assists": 0, "experience": 4, "form": 3.2, "fitness": 75, "is_xfactor": False, "market_value_m": 1.0},
        ],
    },
    "Czech Republic": {
        "group": "A", "fifa_ranking": 42, "total_market_value_m": 120.0,
        "rank": 42, "region": "UEFA", "coach": "Ivan Hasek",
        "players": [
            {"name": "Soucek", "position": "CM", "age": 29, "club": "West Ham", "rating": 79, "goals": 8, "assists": 5, "experience": 3, "form": 3.8, "fitness": 90, "is_xfactor": True, "market_value_m": 25.0},
            {"name": "Schick", "position": "ST", "age": 28, "club": "Leverkusen", "rating": 78, "goals": 18, "assists": 4, "experience": 3, "form": 4.0, "fitness": 85, "is_xfactor": True, "market_value_m": 22.0},
            {"name": "Barak", "position": "AM", "age": 28, "club": "Fiorentina", "rating": 75, "goals": 6, "assists": 8, "experience": 2, "form": 3.5, "fitness": 87, "is_xfactor": False, "market_value_m": 12.0},
            {"name": "Coufal", "position": "RB", "age": 29, "club": "West Ham", "rating": 74, "goals": 1, "assists": 4, "experience": 3, "form": 3.4, "fitness": 88, "is_xfactor": False, "market_value_m": 8.0},
            {"name": "Vaclik", "position": "GK", "age": 33, "club": "Sevilla", "rating": 73, "goals": 0, "assists": 0, "experience": 3, "form": 3.3, "fitness": 82, "is_xfactor": False, "market_value_m": 3.0},
        ],
    },
    "Bosnia": {
        "group": "B", "fifa_ranking": 61, "total_market_value_m": 55.0,
        "rank": 61, "region": "UEFA", "coach": "Sergej Barbarez",
        "players": [
            {"name": "Dzeko", "position": "ST", "age": 38, "club": "Fenerbahce", "rating": 74, "goals": 15, "assists": 5, "experience": 5, "form": 3.5, "fitness": 75, "is_xfactor": True, "market_value_m": 3.0},
            {"name": "Pjanic", "position": "CM", "age": 33, "club": "Sharjah FC", "rating": 73, "goals": 3, "assists": 8, "experience": 4, "form": 3.3, "fitness": 78, "is_xfactor": False, "market_value_m": 4.0},
            {"name": "Kolasinac", "position": "CB", "age": 30, "club": "Atalanta", "rating": 74, "goals": 1, "assists": 2, "experience": 3, "form": 3.4, "fitness": 85, "is_xfactor": False, "market_value_m": 5.0},
            {"name": "Begovic", "position": "GK", "age": 35, "club": "Everton", "rating": 70, "goals": 0, "assists": 0, "experience": 4, "form": 3.0, "fitness": 72, "is_xfactor": False, "market_value_m": 1.5},
            {"name": "Visca", "position": "RW", "age": 31, "club": "Trabzonspor", "rating": 72, "goals": 8, "assists": 6, "experience": 3, "form": 3.3, "fitness": 80, "is_xfactor": False, "market_value_m": 3.0},
        ],
    },
    "Haiti": {
        "group": "C", "fifa_ranking": 78, "total_market_value_m": 18.0,
        "rank": 78, "region": "CONCACAF", "coach": "Gabriel Calderon",
        "players": [
            {"name": "Duckens", "position": "ST", "age": 28, "club": "Cercle Brugge", "rating": 70, "goals": 10, "assists": 3, "experience": 2, "form": 3.4, "fitness": 86, "is_xfactor": True, "market_value_m": 3.0},
            {"name": "Nazon", "position": "LW", "age": 27, "club": "KV Kortrijk", "rating": 68, "goals": 6, "assists": 4, "experience": 2, "form": 3.1, "fitness": 83, "is_xfactor": False, "market_value_m": 2.0},
            {"name": "Pierrot", "position": "ST", "age": 25, "club": "LASK", "rating": 67, "goals": 7, "assists": 2, "experience": 1, "form": 3.0, "fitness": 88, "is_xfactor": False, "market_value_m": 2.0},
            {"name": "Etienne", "position": "MF", "age": 26, "club": "Bordeaux", "rating": 66, "goals": 2, "assists": 3, "experience": 1, "form": 2.8, "fitness": 82, "is_xfactor": False, "market_value_m": 1.5},
            {"name": "Placide", "position": "GK", "age": 33, "club": "Free Agent", "rating": 65, "goals": 0, "assists": 0, "experience": 3, "form": 2.8, "fitness": 75, "is_xfactor": False, "market_value_m": 0.5},
        ],
    },
    "Scotland": {
        "group": "C", "fifa_ranking": 39, "total_market_value_m": 110.0,
        "rank": 39, "region": "UEFA", "coach": "Steve Clarke",
        "players": [
            {"name": "Robertson", "position": "LB", "age": 30, "club": "Liverpool", "rating": 81, "goals": 2, "assists": 8, "experience": 4, "form": 3.8, "fitness": 88, "is_xfactor": True, "market_value_m": 20.0},
            {"name": "McGinn", "position": "CM", "age": 29, "club": "Aston Villa", "rating": 77, "goals": 7, "assists": 5, "experience": 3, "form": 3.6, "fitness": 87, "is_xfactor": False, "market_value_m": 12.0},
            {"name": "Tierney", "position": "CB", "age": 27, "club": "Arsenal", "rating": 78, "goals": 1, "assists": 3, "experience": 3, "form": 3.5, "fitness": 82, "is_xfactor": True, "market_value_m": 18.0},
            {"name": "McTominay", "position": "CM", "age": 27, "club": "Man United", "rating": 77, "goals": 8, "assists": 3, "experience": 3, "form": 3.7, "fitness": 90, "is_xfactor": False, "market_value_m": 15.0},
            {"name": "Adams", "position": "ST", "age": 27, "club": "Southampton", "rating": 73, "goals": 10, "assists": 4, "experience": 2, "form": 3.4, "fitness": 86, "is_xfactor": False, "market_value_m": 8.0},
        ],
    },
    "Paraguay": {
        "group": "D", "fifa_ranking": 52, "total_market_value_m": 65.0,
        "rank": 52, "region": "CONMEBOL", "coach": "Gustavo Alfaro",
        "players": [
            {"name": "Almiron", "position": "RW", "age": 28, "club": "Newcastle", "rating": 77, "goals": 8, "assists": 6, "experience": 3, "form": 3.6, "fitness": 89, "is_xfactor": True, "market_value_m": 15.0},
            {"name": "Romero", "position": "ST", "age": 27, "club": "Alanyaspor", "rating": 72, "goals": 10, "assists": 3, "experience": 2, "form": 3.3, "fitness": 85, "is_xfactor": False, "market_value_m": 4.0},
            {"name": "Cardozo", "position": "ST", "age": 29, "club": "Olympiacos", "rating": 71, "goals": 8, "assists": 2, "experience": 2, "form": 3.2, "fitness": 83, "is_xfactor": False, "market_value_m": 3.5},
            {"name": "Gomez", "position": "MF", "age": 26, "club": "Dinamo Moscow", "rating": 70, "goals": 3, "assists": 5, "experience": 1, "form": 3.1, "fitness": 87, "is_xfactor": False, "market_value_m": 3.0},
            {"name": "Silva", "position": "GK", "age": 30, "club": "Libertad", "rating": 69, "goals": 0, "assists": 0, "experience": 3, "form": 3.0, "fitness": 82, "is_xfactor": False, "market_value_m": 2.0},
        ],
    },
    "Curacao": {
        "group": "E", "fifa_ranking": 72, "total_market_value_m": 30.0,
        "rank": 72, "region": "CONCACAF", "coach": "Remko Bicentini",
        "players": [
            {"name": "Babel", "position": "LW", "age": 35, "club": "Free Agent", "rating": 70, "goals": 5, "assists": 4, "experience": 4, "form": 3.0, "fitness": 72, "is_xfactor": False, "market_value_m": 1.0},
            {"name": "Promes", "position": "ST", "age": 30, "club": "Spartak Moscow", "rating": 72, "goals": 10, "assists": 5, "experience": 3, "form": 3.3, "fitness": 80, "is_xfactor": True, "market_value_m": 3.0},
            {"name": "Kluivert", "position": "RW", "age": 24, "club": "Nice", "rating": 71, "goals": 4, "assists": 6, "experience": 2, "form": 3.2, "fitness": 86, "is_xfactor": False, "market_value_m": 4.0},
            {"name": "Martina", "position": "RB", "age": 32, "club": "Free Agent", "rating": 67, "goals": 0, "assists": 2, "experience": 3, "form": 2.8, "fitness": 74, "is_xfactor": False, "market_value_m": 0.8},
            {"name": "Cuypers", "position": "MF", "age": 25, "club": "Gent", "rating": 69, "goals": 3, "assists": 4, "experience": 1, "form": 3.0, "fitness": 84, "is_xfactor": False, "market_value_m": 2.0},
        ],
    },
    "Cape Verde": {
        "group": "H", "fifa_ranking": 65, "total_market_value_m": 28.0,
        "rank": 65, "region": "CAF", "coach": "Bubista",
        "players": [
            {"name": "Mendes", "position": "ST", "age": 28, "club": "Vitoria SC", "rating": 72, "goals": 9, "assists": 3, "experience": 2, "form": 3.4, "fitness": 86, "is_xfactor": True, "market_value_m": 4.0},
            {"name": "Soares", "position": "MF", "age": 27, "club": "Braga", "rating": 70, "goals": 4, "assists": 5, "experience": 2, "form": 3.2, "fitness": 84, "is_xfactor": False, "market_value_m": 3.0},
            {"name": "Tavares", "position": "CB", "age": 26, "club": "Famalicao", "rating": 69, "goals": 1, "assists": 1, "experience": 1, "form": 3.0, "fitness": 87, "is_xfactor": False, "market_value_m": 2.5},
            {"name": "Lima", "position": "MF", "age": 29, "club": "Arouca", "rating": 68, "goals": 3, "assists": 4, "experience": 2, "form": 3.0, "fitness": 82, "is_xfactor": False, "market_value_m": 1.5},
            {"name": "Vozinha", "position": "GK", "age": 31, "club": "AEL Limassol", "rating": 68, "goals": 0, "assists": 0, "experience": 3, "form": 3.0, "fitness": 80, "is_xfactor": False, "market_value_m": 1.0},
        ],
    },
    "Uzbekistan": {
        "group": "K", "fifa_ranking": 55, "total_market_value_m": 35.0,
        "rank": 55, "region": "AFC", "coach": "Srecko Katanec",
        "players": [
            {"name": "Shomurodov", "position": "ST", "age": 27, "club": "Cagliari", "rating": 73, "goals": 10, "assists": 4, "experience": 3, "form": 3.5, "fitness": 86, "is_xfactor": True, "market_value_m": 5.0},
            {"name": "Masharipov", "position": "LW", "age": 28, "club": "Al-Nassr", "rating": 71, "goals": 5, "assists": 7, "experience": 2, "form": 3.3, "fitness": 84, "is_xfactor": False, "market_value_m": 3.0},
            {"name": "Sergeev", "position": "MF", "age": 26, "club": "Pakhtakor", "rating": 69, "goals": 4, "assists": 3, "experience": 2, "form": 3.1, "fitness": 85, "is_xfactor": False, "market_value_m": 2.0},
            {"name": "Ismailov", "position": "CB", "age": 29, "club": "Pakhtakor", "rating": 68, "goals": 1, "assists": 1, "experience": 3, "form": 3.0, "fitness": 83, "is_xfactor": False, "market_value_m": 1.5},
            {"name": "Yatimov", "position": "GK", "age": 27, "club": "Nasaf", "rating": 68, "goals": 0, "assists": 0, "experience": 2, "form": 3.0, "fitness": 85, "is_xfactor": False, "market_value_m": 1.0},
        ],
    },
    "Congo DR": {
        "group": "K", "fifa_ranking": 68, "total_market_value_m": 40.0,
        "rank": 68, "region": "CAF", "coach": "Sebastien Desabre",
        "players": [
            {"name": "Mbeba", "position": "CB", "age": 26, "club": "Metz", "rating": 70, "goals": 1, "assists": 1, "experience": 2, "form": 3.1, "fitness": 86, "is_xfactor": False, "market_value_m": 3.0},
            {"name": "Kakuta", "position": "AM", "age": 30, "club": "Lens", "rating": 72, "goals": 5, "assists": 7, "experience": 3, "form": 3.3, "fitness": 82, "is_xfactor": True, "market_value_m": 4.0},
            {"name": "Bokila", "position": "ST", "age": 28, "club": "Petrolul", "rating": 68, "goals": 7, "assists": 2, "experience": 2, "form": 3.0, "fitness": 84, "is_xfactor": False, "market_value_m": 2.0},
            {"name": "Mputu", "position": "MF", "age": 34, "club": "TP Mazembe", "rating": 67, "goals": 3, "assists": 4, "experience": 4, "form": 2.8, "fitness": 72, "is_xfactor": False, "market_value_m": 1.0},
            {"name": "Kinkela", "position": "LW", "age": 25, "club": "Anderlecht", "rating": 69, "goals": 4, "assists": 3, "experience": 1, "form": 3.0, "fitness": 87, "is_xfactor": False, "market_value_m": 2.5},
        ],
    },
    "Jordan": {
        "group": "J", "fifa_ranking": 70, "total_market_value_m": 20.0,
        "rank": 70, "region": "AFC", "coach": "Hussein Ammouta",
        "players": [
            {"name": "Al-Naimat", "position": "ST", "age": 26, "club": "Al-Arabi", "rating": 72, "goals": 10, "assists": 4, "experience": 2, "form": 3.5, "fitness": 87, "is_xfactor": True, "market_value_m": 3.0},
            {"name": "Al-Rashdan", "position": "MF", "age": 27, "club": "Al-Faisaly", "rating": 69, "goals": 3, "assists": 5, "experience": 2, "form": 3.1, "fitness": 84, "is_xfactor": False, "market_value_m": 1.5},
            {"name": "Al-Mardi", "position": "CB", "age": 28, "club": "Al-Faisaly", "rating": 68, "goals": 1, "assists": 1, "experience": 2, "form": 3.0, "fitness": 83, "is_xfactor": False, "market_value_m": 1.0},
            {"name": "Al-Arab", "position": "CB", "age": 26, "club": "Al-Wehdat", "rating": 67, "goals": 0, "assists": 0, "experience": 1, "form": 2.9, "fitness": 85, "is_xfactor": False, "market_value_m": 0.8},
            {"name": "Shafi", "position": "GK", "age": 30, "club": "Al-Wehdat", "rating": 69, "goals": 0, "assists": 0, "experience": 3, "form": 3.1, "fitness": 82, "is_xfactor": False, "market_value_m": 1.0},
        ],
    },
    "Algeria": {
        "group": "J", "fifa_ranking": 36, "total_market_value_m": 130.0,
        "rank": 36, "region": "CAF", "coach": "Vladimir Petkovic",
        "players": [
            {"name": "Mahrez", "position": "RW", "age": 33, "club": "Al-Ahli", "rating": 82, "goals": 10, "assists": 12, "experience": 4, "form": 3.8, "fitness": 84, "is_xfactor": True, "market_value_m": 18.0},
            {"name": "Bennacer", "position": "CM", "age": 26, "club": "AC Milan", "rating": 79, "goals": 2, "assists": 8, "experience": 3, "form": 3.6, "fitness": 86, "is_xfactor": True, "market_value_m": 22.0},
            {"name": "Bounou", "position": "GK", "age": 32, "club": "Al-Hilal", "rating": 80, "goals": 0, "assists": 0, "experience": 4, "form": 3.7, "fitness": 85, "is_xfactor": True, "market_value_m": 15.0},
            {"name": "Belmadi", "position": "MF", "age": 28, "club": "Nice", "rating": 73, "goals": 4, "assists": 5, "experience": 2, "form": 3.3, "fitness": 87, "is_xfactor": False, "market_value_m": 6.0},
            {"name": "Feghouli", "position": "RW", "age": 34, "club": "Free Agent", "rating": 70, "goals": 3, "assists": 4, "experience": 4, "form": 2.8, "fitness": 72, "is_xfactor": False, "market_value_m": 1.5},
        ],
    },
    "Austria": {
        "group": "J", "fifa_ranking": 25, "total_market_value_m": 220.0,
        "rank": 25, "region": "UEFA", "coach": "Ralf Rangnick",
        "players": [
            {"name": "Sabitzer", "position": "CM", "age": 28, "club": "Dortmund", "rating": 79, "goals": 7, "assists": 8, "experience": 3, "form": 3.8, "fitness": 89, "is_xfactor": True, "market_value_m": 18.0},
            {"name": "Alaba", "position": "CB", "age": 31, "club": "Real Madrid", "rating": 82, "goals": 2, "assists": 4, "experience": 5, "form": 3.7, "fitness": 78, "is_xfactor": True, "market_value_m": 25.0},
            {"name": "Lainer", "position": "RB", "age": 29, "club": "Monchengladbach", "rating": 74, "goals": 1, "assists": 3, "experience": 3, "form": 3.3, "fitness": 85, "is_xfactor": False, "market_value_m": 6.0},
            {"name": "Baumgartner", "position": "AM", "age": 24, "club": "Leipzig", "rating": 77, "goals": 8, "assists": 6, "experience": 2, "form": 3.6, "fitness": 90, "is_xfactor": True, "market_value_m": 20.0},
            {"name": "Lindner", "position": "GK", "age": 30, "club": "Union Berlin", "rating": 73, "goals": 0, "assists": 0, "experience": 3, "form": 3.2, "fitness": 84, "is_xfactor": False, "market_value_m": 4.0},
        ],
    },
    "Iraq": {
        "group": "I", "fifa_ranking": 59, "total_market_value_m": 22.0,
        "rank": 59, "region": "AFC", "coach": "Jesus Casas",
        "players": [
            {"name": "Hussein", "position": "ST", "age": 27, "club": "Al-Quwa Al-Jawiya", "rating": 71, "goals": 9, "assists": 3, "experience": 2, "form": 3.3, "fitness": 85, "is_xfactor": True, "market_value_m": 2.5},
            {"name": "Ali", "position": "MF", "age": 26, "club": "Al-Shorta", "rating": 69, "goals": 4, "assists": 5, "experience": 2, "form": 3.1, "fitness": 84, "is_xfactor": False, "market_value_m": 1.5},
            {"name": "Atwan", "position": "MF", "age": 28, "club": "Zakho FC", "rating": 67, "goals": 2, "assists": 3, "experience": 2, "form": 2.9, "fitness": 82, "is_xfactor": False, "market_value_m": 1.0},
            {"name": "Abbas", "position": "CB", "age": 25, "club": "Al-Zawraa", "rating": 66, "goals": 0, "assists": 0, "experience": 1, "form": 2.8, "fitness": 86, "is_xfactor": False, "market_value_m": 0.8},
            {"name": "Hameed", "position": "GK", "age": 30, "club": "Al-Shorta", "rating": 68, "goals": 0, "assists": 0, "experience": 3, "form": 3.0, "fitness": 80, "is_xfactor": False, "market_value_m": 1.0},
        ],
    },
    "Norway": {
        "group": "I", "fifa_ranking": 33, "total_market_value_m": 280.0,
        "rank": 33, "region": "UEFA", "coach": "Stale Solbakken",
        "players": [
            {"name": "Haaland", "position": "ST", "age": 25, "club": "Man City", "rating": 93, "goals": 45, "assists": 8, "experience": 3, "form": 4.8, "fitness": 94, "is_xfactor": True, "market_value_m": 170.0},
            {"name": "Odegaard", "position": "AM", "age": 25, "club": "Arsenal", "rating": 87, "goals": 10, "assists": 15, "experience": 4, "form": 4.2, "fitness": 88, "is_xfactor": True, "market_value_m": 80.0},
            {"name": "Sander", "position": "CB", "age": 26, "club": "Nice", "rating": 74, "goals": 1, "assists": 2, "experience": 2, "form": 3.3, "fitness": 87, "is_xfactor": False, "market_value_m": 8.0},
            {"name": "Ajer", "position": "CB", "age": 26, "club": "Brentford", "rating": 73, "goals": 1, "assists": 1, "experience": 2, "form": 3.2, "fitness": 86, "is_xfactor": False, "market_value_m": 7.0},
            {"name": "Nyland", "position": "GK", "age": 30, "club": "Sevilla", "rating": 72, "goals": 0, "assists": 0, "experience": 3, "form": 3.2, "fitness": 83, "is_xfactor": False, "market_value_m": 3.0},
        ],
    },
    "New Zealand": {
        "group": "G", "fifa_ranking": 90, "total_market_value_m": 15.0,
        "rank": 90, "region": "OFC", "coach": "Danny Hay",
        "players": [
            {"name": "Wood", "position": "ST", "age": 30, "club": "Nottingham Forest", "rating": 76, "goals": 14, "assists": 3, "experience": 4, "form": 3.7, "fitness": 86, "is_xfactor": True, "market_value_m": 8.0},
            {"name": "Rojas", "position": "LW", "age": 29, "club": "Free Agent", "rating": 68, "goals": 4, "assists": 5, "experience": 3, "form": 3.0, "fitness": 78, "is_xfactor": False, "market_value_m": 1.0},
            {"name": "Reid", "position": "CB", "age": 33, "club": "Free Agent", "rating": 67, "goals": 0, "assists": 0, "experience": 4, "form": 2.8, "fitness": 72, "is_xfactor": False, "market_value_m": 0.5},
            {"name": "Smith", "position": "MF", "age": 26, "club": "Sacramento Rep", "rating": 66, "goals": 2, "assists": 3, "experience": 1, "form": 2.9, "fitness": 84, "is_xfactor": False, "market_value_m": 1.0},
            {"name": "Marinovic", "position": "GK", "age": 29, "club": "Free Agent", "rating": 65, "goals": 0, "assists": 0, "experience": 2, "form": 2.8, "fitness": 78, "is_xfactor": False, "market_value_m": 0.5},
        ],
    },
}

TOURNAMENT_INFO = {
    "year": 2026,
    "host": ["USA", "Canada", "Mexico"],
    "teams_count": 48,
    "groups_count": 12,
    "teams_per_group": 4,
    "knockout_teams": 32,
    "format": "12 groups of 4, top 2 + 8 best 3rd advance",
    "start_date": "2026-06-11",
    "final_date": "2026-07-19",
    "opta_win_probability": {
        "Spain": 18.3,
        "Argentina": 16.1,
        "France": 14.5,
        "England": 12.8,
        "Brazil": 11.2,
        "Portugal": 7.5,
        "Germany": 6.8,
        "Netherlands": 5.2,
    },
}


def main():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)

    for team_name, group in EXISTING_TEAM_GROUPS.items():
        if team_name in db["teams"]:
            db["teams"][team_name]["group"] = group
        else:
            print(f"WARNING: Existing team '{team_name}' not found in database!")

    for team_name, team_data in NEW_TEAMS.items():
        if team_name in db["teams"]:
            db["teams"][team_name]["group"] = team_data["group"]
            print(f"Updated group for existing team '{team_name}': {team_data['group']}")
        else:
            db["teams"][team_name] = team_data

    db["tournament_info"] = TOURNAMENT_INFO
    db["last_updated"] = "2026-05-29"
    db["model_version"] = "5.1"

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

    total_teams = len(db["teams"])
    teams_with_group = sum(1 for t in db["teams"].values() if "group" in t)
    print(f"Total teams: {total_teams}")
    print(f"Teams with group field: {teams_with_group}")
    print(f"Tournament info added: {'tournament_info' in db}")
    print(f"Last updated: {db['last_updated']}")
    print(f"Model version: {db['model_version']}")

    groups = {}
    for name, team in db["teams"].items():
        g = team.get("group", "?")
        if g not in groups:
            groups[g] = []
        groups[g].append(name)

    print(f"\nGroup distribution:")
    for g in sorted(groups.keys()):
        print(f"  Group {g}: {', '.join(sorted(groups[g]))} ({len(groups[g])} teams)")

    missing_group = [name for name, team in db["teams"].items() if "group" not in team]
    if missing_group:
        print(f"\nWARNING: Teams missing group: {missing_group}")
    else:
        print(f"\nAll {total_teams} teams have group field assigned.")


if __name__ == "__main__":
    main()
