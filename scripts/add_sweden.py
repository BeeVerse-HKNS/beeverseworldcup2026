import json

with open('data/wc2026_player_database.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

sweden = {
    'group': 'F',
    'fifa_ranking': 26,
    'total_market_value_m': 180.0,
    'rank': 26,
    'region': 'UEFA',
    'coach': 'Jon Dahl Tomasson',
    'players': [
        {'name': 'Isak', 'position': 'ST', 'age': 25, 'club': 'Newcastle', 'rating': 85, 'goals': 18, 'assists': 5, 'experience': 4, 'form': 4.2, 'fitness': 88, 'is_xfactor': True, 'market_value_m': 70.0},
        {'name': 'Forsberg', 'position': 'AM', 'age': 32, 'club': 'New York Red Bulls', 'rating': 78, 'goals': 8, 'assists': 7, 'experience': 5, 'form': 3.8, 'fitness': 80, 'is_xfactor': False, 'market_value_m': 3.0},
        {'name': 'Kulusevski', 'position': 'RW', 'age': 24, 'club': 'Tottenham', 'rating': 80, 'goals': 7, 'assists': 9, 'experience': 3, 'form': 4.0, 'fitness': 85, 'is_xfactor': False, 'market_value_m': 35.0},
        {'name': 'Lindelof', 'position': 'CB', 'age': 30, 'club': 'Manchester United', 'rating': 79, 'goals': 1, 'assists': 1, 'experience': 5, 'form': 3.6, 'fitness': 82, 'is_xfactor': False, 'market_value_m': 12.0},
        {'name': 'Olsen', 'position': 'GK', 'age': 34, 'club': 'Aston Villa', 'rating': 76, 'goals': 0, 'assists': 0, 'experience': 5, 'form': 3.5, 'fitness': 78, 'is_xfactor': False, 'market_value_m': 2.0}
    ]
}

db['teams']['Sweden'] = sweden

sweden_xfactors = [p for p in sweden['players'] if p.get('is_xfactor')]
for xf in sweden_xfactors:
    db['xfactor_players'].append({
        'name': xf['name'],
        'team': 'Sweden',
        'rating': xf['rating'],
        'position': xf['position'],
        'identified_at': '2026-05-30T00:00:00.000000'
    })

with open('data/wc2026_player_database.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("Sweden added successfully")
print("Total teams:", len(db['teams']))
print("Sweden players:", [p['name'] for p in sweden['players']])
