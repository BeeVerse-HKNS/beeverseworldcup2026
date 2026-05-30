import json
from pathlib import Path

KNOWN_MARKET_VALUES = {
    "Erling Haaland": 180,
    "Kylian Mbappe": 180,
    "Vinicius Jr": 150,
    "Jude Bellingham": 150,
    "Rodri": 120,
    "Bukayo Saka": 120,
    "Phil Foden": 110,
    "Florian Wirtz": 110,
    "Jamal Musiala": 100,
    "Pedri": 100,
    "Lamine Yamal": 100,
    "Lionel Messi": 30,
    "Cristiano Ronaldo": 15,
}

FIFA_RANKINGS = {
    "Argentina": 1,
    "France": 2,
    "Spain": 3,
    "England": 4,
    "Brazil": 5,
    "Portugal": 6,
    "Netherlands": 7,
    "Belgium": 8,
    "Germany": 9,
    "Italy": 10,
    "Croatia": 11,
    "Uruguay": 12,
    "Colombia": 13,
    "Denmark": 14,
    "Mexico": 15,
    "USA": 16,
    "Switzerland": 17,
    "Senegal": 18,
    "Morocco": 19,
    "Japan": 20,
    "Iran": 21,
    "South Korea": 22,
    "Australia": 23,
    "Egypt": 24,
    "Nigeria": 25,
    "Sweden": 26,
    "Poland": 27,
    "Ukraine": 28,
    "Turkey": 29,
    "Austria": 30,
    "Hungary": 31,
    "Czech Republic": 32,
    "Norway": 33,
    "Scotland": 34,
    "Romania": 35,
    "Canada": 36,
    "Chile": 37,
    "Peru": 38,
    "Venezuela": 39,
    "Ecuador": 40,
    "Paraguay": 41,
    "Bolivia": 42,
    "Saudi Arabia": 43,
    "Qatar": 44,
    "United Arab Emirates": 45,
    "Tunisia": 46,
    "Algeria": 47,
    "Ghana": 48,
    "Cameroon": 49,
    "South Africa": 50,
}

def estimate_market_value(rating: int, age: int = None) -> float:
    if rating >= 90:
        base = 150
    elif rating >= 85:
        base = 75
    elif rating >= 80:
        base = 40
    elif rating >= 75:
        base = 22.5
    elif rating >= 70:
        base = 10
    else:
        base = 3
    
    if age:
        if age > 32:
            age_factor = 0.7
        elif age > 30:
            age_factor = 0.85
        elif age > 28:
            age_factor = 0.95
        else:
            age_factor = 1.0
        base *= age_factor
    
    return round(base, 1)

def main():
    db_path = Path(__file__).parent.parent / "data" / "wc2026_player_database.json"
    
    with open(db_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    stats = {
        "players_updated": 0,
        "teams_updated": 0,
        "total_market_value": 0,
        "known_values_used": 0,
        "estimated_values": 0,
    }
    
    for team_name, team_data in data["teams"].items():
        team_market_value = 0
        
        for player in team_data["players"]:
            player_name = player["name"]
            rating = player.get("rating", 75)
            age = player.get("age")
            
            if player_name in KNOWN_MARKET_VALUES:
                market_value = KNOWN_MARKET_VALUES[player_name]
                stats["known_values_used"] += 1
            else:
                market_value = estimate_market_value(rating, age)
                stats["estimated_values"] += 1
            
            player["market_value_m"] = market_value
            team_market_value += market_value
            stats["players_updated"] += 1
        
        team_data["total_market_value_m"] = round(team_market_value, 1)
        
        if team_name in FIFA_RANKINGS:
            team_data["fifa_ranking"] = FIFA_RANKINGS[team_name]
        else:
            team_data["fifa_ranking"] = 50
        
        stats["teams_updated"] += 1
        stats["total_market_value"] += team_market_value
    
    data["model_version"] = "5.0"
    data["last_updated"] = "2026-05-22"
    
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("=" * 60)
    print("World Cup 2026 Database Update Summary")
    print("=" * 60)
    print(f"Players updated: {stats['players_updated']}")
    print(f"Teams updated: {stats['teams_updated']}")
    print(f"Known market values used: {stats['known_values_used']}")
    print(f"Estimated market values: {stats['estimated_values']}")
    print(f"Total market value: {stats['total_market_value']:.1f}M EUR")
    print(f"Model version: {data['model_version']}")
    print(f"Last updated: {data['last_updated']}")
    print("=" * 60)
    
    print("\nTop 10 Teams by Market Value:")
    team_values = [(name, data["teams"][name]["total_market_value_m"]) for name in data["teams"]]
    team_values.sort(key=lambda x: x[1], reverse=True)
    for i, (name, value) in enumerate(team_values[:10], 1):
        print(f"  {i}. {name}: {value:.1f}M EUR")

if __name__ == "__main__":
    main()
