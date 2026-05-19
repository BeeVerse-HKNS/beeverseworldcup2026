import json
import random
from typing import Dict, List, Tuple, Optional
from formula_v9_ultimate import FormulaV9

class TournamentModel:
    def __init__(self, player_data_path: str):
        self.engine = FormulaV9(player_data_path)
        self.wc2026_teams = [
            "Japan", "South Korea", "Saudi Arabia", "Australia", "Iran", "Qatar",
            "Nigeria", "Senegal", "Morocco", "Egypt", "Cameroon", "Algeria",
            "USA", "Mexico", "Canada", "Costa Rica", "Jamaica", "Panama",
            "Brazil", "Argentina", "Uruguay", "Colombia", "Chile", "Peru",
            "Germany", "France", "Spain", "England", "Italy", "Netherlands", 
            "Portugal", "Belgium", "Croatia", "Switzerland", "Austria", "Denmark"
        ]
        
        self.group_stage_teams = []
        self.knockout_bracket = {}
    
    def generate_groups(self) -> List[List[str]]:
        teams_copy = self.wc2026_teams.copy()
        random.shuffle(teams_copy)
        
        groups = []
        for i in range(8):
            group = teams_copy[i*4:(i+1)*4]
            groups.append(group)
        
        return groups
    
    def simulate_group_stage(self) -> Dict[str, List[str]]:
        groups = self.generate_groups()
        group_results = {}
        
        group_letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        
        for idx, group in enumerate(groups):
            group_name = f"Group {group_letters[idx]}"
            standings = {team: {'points': 0, 'goals_for': 0, 'goals_against': 0, 'goal_diff': 0} for team in group}
            
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    home_team = group[i]
                    away_team = group[j]
                    
                    result = self.engine.predict_match(home_team, away_team)
                    
                    if result['predicted_result'] == "HOME_WIN":
                        standings[home_team]['points'] += 3
                        standings[home_team]['goals_for'] += 2
                        standings[away_team]['goals_against'] += 2
                    elif result['predicted_result'] == "AWAY_WIN":
                        standings[away_team]['points'] += 3
                        standings[away_team]['goals_for'] += 2
                        standings[home_team]['goals_against'] += 2
                    else:
                        standings[home_team]['points'] += 1
                        standings[away_team]['points'] += 1
                        standings[home_team]['goals_for'] += 1
                        standings[away_team]['goals_for'] += 1
                        standings[home_team]['goals_against'] += 1
                        standings[away_team]['goals_against'] += 1
            
            for team in standings:
                standings[team]['goal_diff'] = standings[team]['goals_for'] - standings[team]['goals_against']
            
            sorted_teams = sorted(group, key=lambda t: (-standings[t]['points'], -standings[t]['goal_diff'], -standings[t]['goals_for']))
            
            group_results[group_name] = {
                'teams': group,
                'standings': standings,
                'qualifiers': sorted_teams[:2],
                'third_place': sorted_teams[2] if len(sorted_teams) > 2 else None
            }
        
        self.group_stage_teams = group_results
        return group_results
    
    def generate_knockout_bracket(self, group_results: Dict[str, List[str]]) -> Dict:
        group_letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        qualifiers = []
        
        for letter in group_letters:
            group_name = f"Group {letter}"
            if group_name in group_results:
                qualifiers.extend(group_results[group_name]['qualifiers'])
        
        third_places = []
        for letter in group_letters:
            group_name = f"Group {letter}"
            if group_name in group_results and group_results[group_name]['third_place']:
                third_places.append(group_results[group_name]['third_place'])
        
        random.shuffle(third_places)
        lucky_third = third_places[:2]
        
        all_knockout_teams = qualifiers + lucky_third
        random.shuffle(all_knockout_teams)
        
        bracket = {
            'round_of_16': [],
            'quarterfinals': [],
            'semifinals': [],
            'final': [],
            'winner': None
        }
        
        bracket['round_of_16'] = [
            (all_knockout_teams[0], all_knockout_teams[1]),
            (all_knockout_teams[2], all_knockout_teams[3]),
            (all_knockout_teams[4], all_knockout_teams[5]),
            (all_knockout_teams[6], all_knockout_teams[7]),
            (all_knockout_teams[8], all_knockout_teams[9]),
            (all_knockout_teams[10], all_knockout_teams[11]),
            (all_knockout_teams[12], all_knockout_teams[13]),
            (all_knockout_teams[14], all_knockout_teams[15])
        ]
        
        self.knockout_bracket = bracket
        return bracket
    
    def simulate_knockout_match(self, team1: str, team2: str, round_name: str) -> Tuple[str, Dict]:
        result = self.engine.predict_match(team1, team2)
        
        if result['predicted_result'] == "HOME_WIN":
            winner = team1
            loser = team2
        elif result['predicted_result'] == "AWAY_WIN":
            winner = team2
            loser = team1
        else:
            if result['home_win_probability'] > result['away_win_probability']:
                winner = team1
            else:
                winner = team2
            loser = team2 if winner == team1 else team1
        
        return winner, {
            'match': f"{team1} vs {team2}",
            'round': round_name,
            'winner': winner,
            'loser': loser,
            'home_win_prob': result['home_win_probability'],
            'away_win_prob': result['away_win_probability'],
            'draw_prob': result['draw_probability'],
            'confidence': result['confidence']
        }
    
    def simulate_tournament(self) -> Dict:
        print("Simulating Group Stage...")
        group_results = self.simulate_group_stage()
        
        print("Generating Knockout Bracket...")
        bracket = self.generate_knockout_bracket(group_results)
        
        print("Simulating Round of 16...")
        round_of_16_results = []
        quarterfinalists = []
        for match in bracket['round_of_16']:
            winner, result = self.simulate_knockout_match(match[0], match[1], "Round of 16")
            round_of_16_results.append(result)
            quarterfinalists.append(winner)
        
        bracket['round_of_16_results'] = round_of_16_results
        
        print("Simulating Quarterfinals...")
        quarterfinal_matches = [
            (quarterfinalists[0], quarterfinalists[1]),
            (quarterfinalists[2], quarterfinalists[3]),
            (quarterfinalists[4], quarterfinalists[5]),
            (quarterfinalists[6], quarterfinalists[7])
        ]
        quarterfinal_results = []
        semifinalists = []
        for match in quarterfinal_matches:
            winner, result = self.simulate_knockout_match(match[0], match[1], "Quarterfinals")
            quarterfinal_results.append(result)
            semifinalists.append(winner)
        
        bracket['quarterfinals'] = quarterfinal_matches
        bracket['quarterfinal_results'] = quarterfinal_results
        
        print("Simulating Semifinals...")
        semifinal_matches = [
            (semifinalists[0], semifinalists[1]),
            (semifinalists[2], semifinalists[3])
        ]
        semifinal_results = []
        finalists = []
        for match in semifinal_matches:
            winner, result = self.simulate_knockout_match(match[0], match[1], "Semifinals")
            semifinal_results.append(result)
            finalists.append(winner)
        
        bracket['semifinals'] = semifinal_matches
        bracket['semifinal_results'] = semifinal_results
        
        print("Simulating Final...")
        winner, final_result = self.simulate_knockout_match(finalists[0], finalists[1], "Final")
        
        bracket['final'] = (finalists[0], finalists[1])
        bracket['final_result'] = final_result
        bracket['winner'] = winner
        
        third_place_match = (semifinal_results[0]['loser'], semifinal_results[1]['loser'])
        third_place_winner, _ = self.simulate_knockout_match(third_place_match[0], third_place_match[1], "Third Place")
        bracket['third_place'] = third_place_winner
        
        return {
            'group_stage': group_results,
            'knockout_bracket': bracket,
            'champion': winner,
            'runner_up': final_result['loser'],
            'third_place': third_place_winner
        }
    
    def get_team_tournament_stats(self, team_name: str, tournament_result: Dict) -> Dict:
        stats = {
            'team': team_name,
            'group_stage_performance': None,
            'knockout_performance': [],
            'final_position': None,
            'matches_played': 0,
            'matches_won': 0
        }
        
        for group_name, group_data in tournament_result['group_stage'].items():
            if team_name in group_data['teams']:
                stats['group_stage_performance'] = {
                    'group': group_name,
                    'standing': group_data['standings'][team_name],
                    'qualified': team_name in group_data['qualifiers']
                }
                stats['matches_played'] += 3
                stats['matches_won'] += group_data['standings'][team_name]['points'] // 3
        
        bracket = tournament_result['knockout_bracket']
        
        knockout_rounds = ['round_of_16_results', 'quarterfinal_results', 'semifinal_results']
        round_names = ['Round of 16', 'Quarterfinals', 'Semifinals']
        
        for round_key, round_name in zip(knockout_rounds, round_names):
            if round_key in bracket:
                for result in bracket[round_key]:
                    if team_name in [result['match'].split(' vs ')[0], result['match'].split(' vs ')[1]]:
                        stats['knockout_performance'].append({
                            'round': round_name,
                            'opponent': result['winner'] if result['winner'] != team_name else result['loser'],
                            'result': 'W' if result['winner'] == team_name else 'L'
                        })
                        stats['matches_played'] += 1
                        if result['winner'] == team_name:
                            stats['matches_won'] += 1
        
        if team_name == tournament_result['champion']:
            stats['final_position'] = 1
        elif team_name == tournament_result['runner_up']:
            stats['final_position'] = 2
        elif team_name == tournament_result.get('third_place'):
            stats['final_position'] = 3
        else:
            for round_key, round_name in zip(knockout_rounds, round_names):
                if round_key in bracket:
                    for result in bracket[round_key]:
                        if team_name == result['loser']:
                            round_positions = {'Round of 16': 9, 'Quarterfinals': 5, 'Semifinals': 3}
                            stats['final_position'] = round_positions[round_name]
                            break
        
        return stats

if __name__ == "__main__":
    tournament = TournamentModel('data/wc2026_player_database.json')
    
    print("=== World Cup 2026 Tournament Simulation ===")
    result = tournament.simulate_tournament()
    
    print(f"\n🏆 World Cup 2026 Champion: {result['champion']}")
    print(f"🥈 Runner-up: {result['runner_up']}")
    print(f"🥉 Third Place: {result['third_place']}")
    
    print("\n=== Group Stage Results ===")
    for group_name, group_data in result['group_stage'].items():
        print(f"\n{group_name}:")
        for team in group_data['qualifiers']:
            print(f"  ✓ {team}")
    
    print("\n=== Knockout Results ===")
    bracket = result['knockout_bracket']
    
    print("\nRound of 16:")
    for match in bracket['round_of_16_results']:
        print(f"  {match['match']} → {match['winner']}")
    
    print("\nQuarterfinals:")
    for match in bracket['quarterfinal_results']:
        print(f"  {match['match']} → {match['winner']}")
    
    print("\nSemifinals:")
    for match in bracket['semifinal_results']:
        print(f"  {match['match']} → {match['winner']}")
    
    print(f"\nFinal: {bracket['final'][0]} vs {bracket['final'][1]}")
    print(f"  Winner: {bracket['winner']} (Confidence: {bracket['final_result']['confidence']}%)")