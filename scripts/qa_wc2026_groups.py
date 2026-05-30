import json

DB_PATH = r"d:\My_Code_Projects\Harnessing\projects\world-2026\data\wc2026_player_database.json"

with open(DB_PATH, "r", encoding="utf-8") as f:
    db = json.load(f)

print("Valid JSON: OK")
teams = db["teams"]
print(f"Total teams: {len(teams)}")
print(f"Version: {db.get('version', '?')}")
print(f"Model version: {db.get('model_version', '?')}")
print(f"Last updated: {db.get('last_updated', '?')}")
print(f"Tournament info: {'tournament_info' in db}")
print(f"Teams with group: {sum(1 for t in teams.values() if 'group' in t)}")

missing_group = [n for n, t in teams.items() if "group" not in t]
print(f"Teams missing group: {missing_group}")

for g_letter in "ABCDEFGHIJKL":
    g_teams = sorted([n for n, t in teams.items() if t.get("group") == g_letter])
    print(f"  Group {g_letter} ({len(g_teams)}): {', '.join(g_teams)}")

new_teams = ["South Africa", "Czech Republic", "Bosnia", "Qatar", "Haiti", "Scotland",
             "Paraguay", "Curacao", "Cape Verde", "Uzbekistan", "Congo DR", "Jordan",
             "Algeria", "Austria", "Iraq", "Norway", "New Zealand"]
for nt in new_teams:
    if nt in teams:
        t = teams[nt]
        p_count = len(t.get("players", []))
        has_group = "group" in t
        print(f"  {nt}: {p_count} players, group={'Y' if has_group else 'N'}")
    else:
        print(f"  {nt}: MISSING!")

ti = db.get("tournament_info", {})
print(f"\nTournament info:")
print(f"  Year: {ti.get('year')}")
print(f"  Host: {ti.get('host')}")
print(f"  Teams count: {ti.get('teams_count')}")
print(f"  Format: {ti.get('format')}")
print(f"  Start: {ti.get('start_date')}")
print(f"  Final: {ti.get('final_date')}")
print(f"  Opta probabilities: {ti.get('opta_win_probability')}")
