import json
import os
import random
from typing import Dict, List, Tuple, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from formula_v9_ultimate import FormulaV9

_DEFAULT_PLAYER_DATA = os.path.join(os.path.dirname(__file__), 'data', 'wc2026_player_database.json')

class TournamentModel:
    def __init__(self, player_data_path: str = _DEFAULT_PLAYER_DATA):
        self.engine = FormulaV9(player_data_path)
        self.wc2026_groups = {
            'A': ['Mexico', 'South Africa', 'South Korea', 'Czech Republic'],
            'B': ['Canada', 'Bosnia', 'Qatar', 'Switzerland'],
            'C': ['Brazil', 'Morocco', 'Haiti', 'Scotland'],
            'D': ['USA', 'Paraguay', 'Australia', 'Poland'],
            'E': ['Germany', 'Curacao', 'Denmark', 'Italy'],
            'F': ['Netherlands', 'Japan', 'Tunisia', 'Sweden'],
            'G': ['Belgium', 'Egypt', 'Iran', 'New Zealand'],
            'H': ['Spain', 'Cape Verde', 'Saudi Arabia', 'Uruguay'],
            'I': ['France', 'Senegal', 'Iraq', 'Norway'],
            'J': ['Argentina', 'Algeria', 'Austria', 'Jordan'],
            'K': ['Portugal', 'Congo DR', 'Uzbekistan', 'Colombia'],
            'L': ['England', 'Croatia', 'Ghana', 'Nigeria']
        }
        self.wc2026_teams = []
        for group_teams in self.wc2026_groups.values():
            self.wc2026_teams.extend(group_teams)
        
        self.group_stage_teams = []
        self.knockout_bracket = {}
    
    def generate_groups(self) -> Dict[str, List[str]]:
        return dict(self.wc2026_groups)
    
    def simulate_group_stage(self) -> Dict[str, Dict]:
        groups = self.generate_groups()
        group_results = {}
        
        for group_letter, group in groups.items():
            group_name = f"Group {group_letter}"
            standings = {team: {'points': 0, 'goals_for': 0, 'goals_against': 0, 'goal_diff': 0, 'played': 0, 'won': 0, 'drawn': 0, 'lost': 0} for team in group}
            
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    home_team = group[i]
                    away_team = group[j]
                    
                    result = self.engine.predict_match(home_team, away_team)
                    
                    if not result.get('success', False):
                        if home_team < away_team:
                            predicted = "HOME_WIN"
                        else:
                            predicted = "AWAY_WIN"
                    else:
                        predicted = result['predicted_result']
                    
                    standings[home_team]['played'] += 1
                    standings[away_team]['played'] += 1
                    
                    if predicted == "HOME_WIN":
                        standings[home_team]['points'] += 3
                        standings[home_team]['goals_for'] += 2
                        standings[home_team]['won'] += 1
                        standings[away_team]['goals_against'] += 2
                        standings[away_team]['lost'] += 1
                    elif predicted == "AWAY_WIN":
                        standings[away_team]['points'] += 3
                        standings[away_team]['goals_for'] += 2
                        standings[away_team]['won'] += 1
                        standings[home_team]['goals_against'] += 2
                        standings[home_team]['lost'] += 1
                    else:
                        standings[home_team]['points'] += 1
                        standings[away_team]['points'] += 1
                        standings[home_team]['goals_for'] += 1
                        standings[away_team]['goals_for'] += 1
                        standings[home_team]['goals_against'] += 1
                        standings[away_team]['goals_against'] += 1
                        standings[home_team]['drawn'] += 1
                        standings[away_team]['drawn'] += 1
            
            for team in standings:
                standings[team]['goal_diff'] = standings[team]['goals_for'] - standings[team]['goals_against']
            
            sorted_teams = sorted(group, key=lambda t: (-standings[t]['points'], -standings[t]['goal_diff'], -standings[t]['goals_for']))
            
            group_results[group_name] = {
                'group_letter': group_letter,
                'teams': group,
                'standings': standings,
                'qualifiers': sorted_teams[:2],
                'third_place': sorted_teams[2] if len(sorted_teams) > 2 else None,
                'fourth_place': sorted_teams[3] if len(sorted_teams) > 3 else None
            }
        
        self.group_stage_teams = group_results
        return group_results
    
    def display_group_tables(self, group_results: Dict[str, Dict] = None) -> str:
        if group_results is None:
            group_results = self.group_stage_teams
        
        if not group_results:
            return "No group stage results available. Run simulate_group_stage() first."
        
        output = []
        group_letters = list(self.wc2026_groups.keys())
        
        for letter in group_letters:
            group_name = f"Group {letter}"
            if group_name not in group_results:
                continue
            
            group_data = group_results[group_name]
            standings = group_data['standings']
            teams = group_data['teams']
            
            sorted_teams = sorted(teams, key=lambda t: (
                -standings[t]['points'],
                -standings[t]['goal_diff'],
                -standings[t]['goals_for']
            ))
            
            output.append(f"\n{'='*50}")
            output.append(f"  Group {letter}")
            output.append(f"{'='*50}")
            output.append(f"  {'Team':<20} {'P':>3} {'W':>3} {'D':>3} {'L':>3} {'GF':>4} {'GA':>4} {'GD':>4} {'Pts':>4}")
            output.append(f"  {'-'*46}")
            
            for pos, team in enumerate(sorted_teams, 1):
                s = standings[team]
                marker = ""
                if pos <= 2:
                    marker = " *"
                elif pos == 3:
                    marker = " ?"
                output.append(
                    f"  {team:<20} {s['played']:>3} {s['won']:>3} {s['drawn']:>3} "
                    f"{s['lost']:>3} {s['goals_for']:>4} {s['goals_against']:>4} "
                    f"{s['goal_diff']:>+4} {s['points']:>4}{marker}"
                )
            
            output.append(f"  * = Qualified  ? = Best 3rd place candidate")
        
        return "\n".join(output)
    
    def generate_knockout_bracket(self, group_results: Dict[str, Dict]) -> Dict:
        qualifiers = []
        group_letters = list(self.wc2026_groups.keys())
        
        for letter in group_letters:
            group_name = f"Group {letter}"
            if group_name in group_results:
                qualifiers.extend(group_results[group_name]['qualifiers'])
        
        third_places = []
        for letter in group_letters:
            group_name = f"Group {letter}"
            if group_name in group_results and group_results[group_name]['third_place']:
                team = group_results[group_name]['third_place']
                standings = group_results[group_name]['standings'][team]
                third_places.append({
                    'team': team,
                    'points': standings['points'],
                    'goal_diff': standings['goal_diff'],
                    'goals_for': standings['goals_for']
                })
        
        third_places.sort(key=lambda x: (-x['points'], -x['goal_diff'], -x['goals_for']))
        best_thirds = [t['team'] for t in third_places[:8]]
        
        all_knockout_teams = qualifiers + best_thirds
        
        bracket = {
            'round_of_32': [],
            'round_of_16': [],
            'quarterfinals': [],
            'semifinals': [],
            'final': [],
            'winner': None
        }
        
        for i in range(0, len(all_knockout_teams), 2):
            bracket['round_of_32'].append((all_knockout_teams[i], all_knockout_teams[i + 1]))
        
        self.knockout_bracket = bracket
        return bracket
    
    def simulate_knockout_match(self, team1: str, team2: str, round_name: str) -> Tuple[str, Dict]:
        result = self.engine.predict_match(team1, team2)
        
        if not result.get('success', False):
            if team1 < team2:
                winner = team1
            else:
                winner = team2
            loser = team2 if winner == team1 else team1
            return winner, {
                'match': f"{team1} vs {team2}",
                'round': round_name,
                'winner': winner,
                'loser': loser,
                'home_win_prob': 0.5,
                'away_win_prob': 0.5,
                'draw_prob': 0.0,
                'confidence': 50,
                'fallback': True
            }
        
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
        
        print("Simulating Round of 32...")
        round_of_32_results = []
        round_of_16_teams = []
        for match in bracket['round_of_32']:
            winner, result = self.simulate_knockout_match(match[0], match[1], "Round of 32")
            round_of_32_results.append(result)
            round_of_16_teams.append(winner)
        
        bracket['round_of_32_results'] = round_of_32_results
        
        bracket['round_of_16'] = []
        for i in range(0, len(round_of_16_teams), 2):
            bracket['round_of_16'].append((round_of_16_teams[i], round_of_16_teams[i + 1]))
        
        print("Simulating Round of 16...")
        round_of_16_results = []
        quarterfinalists = []
        for match in bracket['round_of_16']:
            winner, result = self.simulate_knockout_match(match[0], match[1], "Round of 16")
            round_of_16_results.append(result)
            quarterfinalists.append(winner)
        
        bracket['round_of_16_results'] = round_of_16_results
        
        print("Simulating Quarterfinals...")
        quarterfinal_matches = []
        for i in range(0, len(quarterfinalists), 2):
            quarterfinal_matches.append((quarterfinalists[i], quarterfinalists[i + 1]))
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
        
        knockout_rounds = ['round_of_32_results', 'round_of_16_results', 'quarterfinal_results', 'semifinal_results']
        round_names = ['Round of 32', 'Round of 16', 'Quarterfinals', 'Semifinals']
        
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
                            round_positions = {'Round of 32': 17, 'Round of 16': 9, 'Quarterfinals': 5, 'Semifinals': 3}
                            stats['final_position'] = round_positions[round_name]
                            break
        
        return stats

if __name__ == "__main__":
    tournament = TournamentModel('data/wc2026_player_database.json')
    
    print("=== World Cup 2026 Tournament Simulation (48 Teams, 12 Groups) ===")
    result = tournament.simulate_tournament()
    
    print(f"\n🏆 World Cup 2026 Champion: {result['champion']}")
    print(f"🥈 Runner-up: {result['runner_up']}")
    print(f"🥉 Third Place: {result['third_place']}")
    
    print("\n=== Group Stage Tables ===")
    print(tournament.display_group_tables(result['group_stage']))
    
    print("\n=== Knockout Results ===")
    bracket = result['knockout_bracket']
    
    if 'round_of_32_results' in bracket:
        print("\nRound of 32:")
        for match in bracket['round_of_32_results']:
            print(f"  {match['match']} → {match['winner']}")
    
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