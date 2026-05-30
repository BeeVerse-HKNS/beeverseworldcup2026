import json

DB_PATH = r"d:\My_Code_Projects\Harnessing\projects\world-2026\data\wc2026_player_database.json"

TEAM_GROUPS = {
    "Mexico": "A", "South Korea": "A", "South Africa": "A", "Czech Republic": "A",
    "Canada": "B", "Switzerland": "B", "Bosnia": "B", "Qatar": "B",
    "Brazil": "C", "Morocco": "C", "Haiti": "C", "Scotland": "C",
    "USA": "D", "Australia": "D", "Paraguay": "D", "Poland": "D",
    "Germany": "E", "Curacao": "E", "Denmark": "E", "Italy": "E",
    "Netherlands": "F", "Japan": "F", "Tunisia": "F",
    "Belgium": "G", "Egypt": "G", "Iran": "G", "New Zealand": "G",
    "Spain": "H", "Saudi Arabia": "H", "Uruguay": "H", "Cape Verde": "H",
    "France": "I", "Senegal": "I", "Iraq": "I", "Norway": "I",
    "Argentina": "J", "Jordan": "J", "Algeria": "J", "Austria": "J",
    "Portugal": "K", "Colombia": "K", "Uzbekistan": "K", "Congo DR": "K",
    "England": "L", "Croatia": "L", "Ghana": "L", "Nigeria": "L",
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

with open(DB_PATH, "r", encoding="utf-8") as f:
    db = json.load(f)

for team_name, group in TEAM_GROUPS.items():
    if team_name in db["teams"]:
        db["teams"][team_name]["group"] = group
    else:
        print(f"WARNING: Team '{team_name}' not found in database!")

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
