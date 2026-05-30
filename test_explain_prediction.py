import json
from formula_v9_ultimate import FormulaV9

engine = FormulaV9('data/wc2026_player_database.json')

print('=== World Cup 2026 Prediction Explanation Test ===')
print(f'Loaded {len(engine.players)} players from {len(engine.teams)} teams')
print()

result = engine.explain_prediction('Brazil', 'Argentina', 2.0, 3.2, 3.5)

if result['success']:
    pred = result['prediction']
    exp = result['explanation']
    
    print('=== Prediction Result ===')
    print(f"Match: {pred['home_team']} vs {pred['away_team']}")
    print(f"Home Win: {pred['home_win_probability']:.2%}")
    print(f"Draw: {pred['draw_probability']:.2%}")
    print(f"Away Win: {pred['away_win_probability']:.2%}")
    print(f"Predicted: {pred['predicted_result']}")
    print(f"Confidence: {pred['confidence']}%")
    print()
    
    print('=== Explanation Summary ===')
    print(exp['summary'])
    print()
    
    print('=== Key Factors ===')
    print(f"Top 3: {', '.join(exp['key_factors'])}")
    print()
    
    print('=== 7 Factors Detail ===')
    for factor_key, detail in exp['factors_detail'].items():
        print(f"\n[{detail['name']}]")
        print(f"  Home: {detail['home_value']:.4f} | Away: {detail['away_value']:.4f} | Diff: {detail['diff']:.4f}")
        print(f"  Contribution: {detail['contribution']:.1f}%")
        print(f"  Explanation: {detail['explanation']}")
        print(f"  Calculation: {detail['calculation']}")
    
    print()
    print('=== Confidence Explanation ===')
    print(exp['confidence_explanation'])
    print()
    
    print('=== Winner Analysis ===')
    wa = exp['winner_analysis']
    print(f"Predicted Winner: {wa['predicted_winner']}")
    print(f"Win Probability: {wa['win_probability']:.2%}")
    print('Key Advantages:')
    for adv in wa['key_advantages']:
        print(f"  - {adv['factor']}: {adv['advantage']} ({adv['contribution']:.1f}%)")
else:
    print(f"Error: {result.get('error', 'Unknown error')}")
