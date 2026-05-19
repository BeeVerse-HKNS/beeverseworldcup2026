import json
import math
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Player:
    name: str
    team: str
    position: str
    age: int
    dribbling_skill: int
    pace: int
    shooting: int
    passing: int
    defending: int
    fitness_level: int
    world_cup_experience: int
    is_xfactor: bool
    xfactor_type: Optional[str]
    injury_status: str

@dataclass
class Team:
    name: str
    players: List[Player]
    overall_strength: float
    attack_power: float
    defense_strength: float
    pk_ability: float

class ThreeBoardModel:
    def __init__(self):
        self.factors = {
            'home_advantage': 1.15,
            'defense_weight': 1.8,
            'xfactor_multiplier': 1.4,
            'substitution_effect': 0.15,
            'pk_boost': 1.3
        }
    
    def calculate_composite_odds(self, home_odds: float, draw_odds: float, away_odds: float) -> Tuple[float, float, float]:
        try:
            home_prob = 1.0 / home_odds if home_odds > 0 else 0.333
            draw_prob = 1.0 / draw_odds if draw_odds > 0 else 0.333
            away_prob = 1.0 / away_odds if away_odds > 0 else 0.333
            
            total = home_prob + draw_prob + away_prob
            if total == 0:
                return 0.333, 0.333, 0.333
            
            home_prob /= total
            draw_prob /= total
            away_prob /= total
            
            return home_prob, draw_prob, away_prob
        except:
            return 0.333, 0.333, 0.333

class FormulaV9:
    def __init__(self, player_data_path: str):
        self.players = self._load_player_data(player_data_path)
        self.teams = self._build_team_database()
        self.three_board = ThreeBoardModel()
        self.factor_weights = {
            'xg_weight': 0.25,
            'v7_weight': 0.20,
            'odds_weight': 0.20,
            'player_weight': 0.15,
            'defensive_pk_weight': 0.10,
            'substitution_weight': 0.05,
            'xfactor_weight': 0.05
        }
    
    def _load_player_data(self, path: str) -> List[Player]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            players = []
            for p in data.get('players', []):
                players.append(Player(
                    name=p['name'],
                    team=p['team'],
                    position=p['position'],
                    age=p['age'],
                    dribbling_skill=p.get('dribbling_skill', 0),
                    pace=p.get('pace', 0),
                    shooting=p.get('shooting', 0),
                    passing=p.get('passing', 0),
                    defending=p.get('defending', 0),
                    fitness_level=p.get('fitness_level', 0),
                    world_cup_experience=p.get('world_cup_experience', 0),
                    is_xfactor=p.get('is_xfactor', False),
                    xfactor_type=p.get('xfactor_type'),
                    injury_status=p.get('injury_status', 'fit')
                ))
            return players
        except Exception as e:
            return []
    
    def _build_team_database(self) -> Dict[str, Team]:
        teams = {}
        for player in self.players:
            if player.team not in teams:
                teams[player.team] = {
                    'players': [],
                    'sum_dribbling': 0,
                    'sum_pace': 0,
                    'sum_shooting': 0,
                    'sum_passing': 0,
                    'sum_defending': 0,
                    'sum_fitness': 0,
                    'xfactor_count': 0,
                    'wc_experience': 0
                }
            teams[player.team]['players'].append(player)
            teams[player.team]['sum_dribbling'] += player.dribbling_skill
            teams[player.team]['sum_pace'] += player.pace
            teams[player.team]['sum_shooting'] += player.shooting
            teams[player.team]['sum_passing'] += player.passing
            teams[player.team]['sum_defending'] += player.defending
            teams[player.team]['sum_fitness'] += player.fitness_level
            if player.is_xfactor:
                teams[player.team]['xfactor_count'] += 1
            teams[player.team]['wc_experience'] += player.world_cup_experience
        
        team_objects = {}
        for team_name, data in teams.items():
            count = len(data['players']) if len(data['players']) > 0 else 1
            team_objects[team_name] = Team(
                name=team_name,
                players=data['players'],
                overall_strength=min(99, (data['sum_dribbling'] + data['sum_pace'] + data['sum_shooting'] + 
                                        data['sum_passing'] + data['sum_defending']) / (count * 5)),
                attack_power=min(99, (data['sum_dribbling'] + data['sum_pace'] + data['sum_shooting'] + data['sum_passing']) / (count * 4)),
                defense_strength=min(99, data['sum_defending'] / count),
                pk_ability=min(99, (data['sum_fitness'] / count) + (data['xfactor_count'] * 5))
            )
        return team_objects
    
    def calculate_xg(self, team: Team, opponent_defense: float) -> float:
        base_xg = team.attack_power / 100
        defense_modifier = (100 - opponent_defense) / 100
        return base_xg * defense_modifier * 1.5
    
    def calculate_v7_base(self, home_team: Team, away_team: Team) -> float:
        home_advantage = 0.05
        strength_diff = (home_team.overall_strength - away_team.overall_strength) / 100
        return 0.5 + strength_diff + home_advantage
    
    def calculate_player_factor(self, team: Team) -> float:
        xfactor_bonus = sum(1 for p in team.players if p.is_xfactor) * 0.05
        fitness_avg = sum(p.fitness_level for p in team.players) / len(team.players) / 100
        exp_bonus = sum(p.world_cup_experience for p in team.players) / len(team.players) / 10
        return 0.5 + xfactor_bonus + (fitness_avg - 0.5) + exp_bonus
    
    def calculate_defensive_pk(self, team: Team) -> float:
        avg_defense = team.defense_strength / 100
        gk_skill = max(p.defending for p in team.players if p.position == 'GK') / 100 if any(p.position == 'GK' for p in team.players) else 0.7
        return (avg_defense + gk_skill) / 2
    
    def calculate_substitution_effect(self, team: Team) -> float:
        bench_quality = sum(p.fitness_level for p in team.players) / len(team.players) / 100
        return bench_quality * 0.15
    
    def calculate_xfactor(self, team: Team) -> float:
        xfactor_players = [p for p in team.players if p.is_xfactor]
        if not xfactor_players:
            return 0
        
        max_dribble = max(p.dribbling_skill for p in xfactor_players) / 100
        max_pace = max(p.pace for p in xfactor_players) / 100
        max_shooting = max(p.shooting for p in xfactor_players) / 100
        
        return (max_dribble + max_pace + max_shooting) / 3 * self.three_board.factors['xfactor_multiplier']
    
    def predict_match(self, home_team_name: str, away_team_name: str, 
                     home_odds: float = 2.0, draw_odds: float = 3.2, away_odds: float = 3.5) -> Dict:
        home_team = self.teams.get(home_team_name)
        away_team = self.teams.get(away_team_name)
        
        if not home_team or not away_team:
            return {
                'success': False,
                'error': f"Teams not found: {home_team_name} or {away_team_name}"
            }
        
        xg_home = self.calculate_xg(home_team, away_team.defense_strength)
        xg_away = self.calculate_xg(away_team, home_team.defense_strength)
        
        v7_base = self.calculate_v7_base(home_team, away_team)
        
        home_prob, draw_prob, away_prob = self.three_board.calculate_composite_odds(home_odds, draw_odds, away_odds)
        
        player_home = self.calculate_player_factor(home_team)
        player_away = self.calculate_player_factor(away_team)
        
        defensive_pk_home = self.calculate_defensive_pk(home_team)
        defensive_pk_away = self.calculate_defensive_pk(away_team)
        
        substitution_home = self.calculate_substitution_effect(home_team)
        substitution_away = self.calculate_substitution_effect(away_team)
        
        xfactor_home = self.calculate_xfactor(home_team)
        xfactor_away = self.calculate_xfactor(away_team)
        
        weighted_xg = (xg_home - xg_away) * self.factor_weights['xg_weight']
        weighted_v7 = (v7_base - 0.5) * self.factor_weights['v7_weight'] * 2
        weighted_odds = (home_prob - 0.5) * self.factor_weights['odds_weight'] * 2
        weighted_player = (player_home - player_away) * self.factor_weights['player_weight'] * 2
        weighted_defensive_pk = (defensive_pk_home - defensive_pk_away) * self.factor_weights['defensive_pk_weight'] * 2
        weighted_substitution = (substitution_home - substitution_away) * self.factor_weights['substitution_weight'] * 2
        weighted_xfactor = (xfactor_home - xfactor_away) * self.factor_weights['xfactor_weight'] * 2
        
        total_score = (weighted_xg + weighted_v7 + weighted_odds + 
                      weighted_player + weighted_defensive_pk + 
                      weighted_substitution + weighted_xfactor)
        
        home_win_prob = 1 / (1 + math.exp(-total_score * 10))
        
        normalized_home = home_win_prob * 0.7 + 0.15
        normalized_away = (1 - home_win_prob) * 0.7 + 0.15
        normalized_draw = 1 - normalized_home - normalized_away
        
        if normalized_draw < 0:
            normalized_draw = 0.1
            adjust = (1 - 0.1) / (normalized_home + normalized_away)
            normalized_home *= adjust
            normalized_away *= adjust
        
        result = "HOME_WIN" if normalized_home > normalized_away else "AWAY_WIN"
        if normalized_draw > max(normalized_home, normalized_away):
            result = "DRAW"
        
        return {
            'success': True,
            'home_team': home_team_name,
            'away_team': away_team_name,
            'home_win_probability': round(normalized_home, 4),
            'draw_probability': round(normalized_draw, 4),
            'away_win_probability': round(normalized_away, 4),
            'predicted_result': result,
            'factors': {
                'xg': {'home': round(xg_home, 4), 'away': round(xg_away, 4)},
                'v7_base': round(v7_base, 4),
                'odds_composite': {'home': round(home_prob, 4), 'draw': round(draw_prob, 4), 'away': round(away_prob, 4)},
                'player_factor': {'home': round(player_home, 4), 'away': round(player_away, 4)},
                'defensive_pk': {'home': round(defensive_pk_home, 4), 'away': round(defensive_pk_away, 4)},
                'substitution': {'home': round(substitution_home, 4), 'away': round(substitution_away, 4)},
                'xfactor': {'home': round(xfactor_home, 4), 'away': round(xfactor_away, 4)}
            },
            'team_stats': {
                home_team_name: {
                    'overall_strength': round(home_team.overall_strength, 2),
                    'attack_power': round(home_team.attack_power, 2),
                    'defense_strength': round(home_team.defense_strength, 2),
                    'pk_ability': round(home_team.pk_ability, 2),
                    'xfactor_count': sum(1 for p in home_team.players if p.is_xfactor)
                },
                away_team_name: {
                    'overall_strength': round(away_team.overall_strength, 2),
                    'attack_power': round(away_team.attack_power, 2),
                    'defense_strength': round(away_team.defense_strength, 2),
                    'pk_ability': round(away_team.pk_ability, 2),
                    'xfactor_count': sum(1 for p in away_team.players if p.is_xfactor)
                }
            },
            'confidence': round(min(99, 70 + (abs(total_score) * 20)), 1)
        }
    
    def get_team_comparison(self, team1_name: str, team2_name: str) -> Dict:
        team1 = self.teams.get(team1_name)
        team2 = self.teams.get(team2_name)
        
        if not team1 or not team2:
            return {'success': False, 'error': "Teams not found"}
        
        return {
            'success': True,
            'team1': team1_name,
            'team2': team2_name,
            'comparison': {
                'overall_strength': {
                    team1_name: round(team1.overall_strength, 1),
                    team2_name: round(team2.overall_strength, 1),
                    'winner': team1_name if team1.overall_strength > team2.overall_strength else team2_name
                },
                'attack_power': {
                    team1_name: round(team1.attack_power, 1),
                    team2_name: round(team2.attack_power, 1),
                    'winner': team1_name if team1.attack_power > team2.attack_power else team2_name
                },
                'defense_strength': {
                    team1_name: round(team1.defense_strength, 1),
                    team2_name: round(team2.defense_strength, 1),
                    'winner': team1_name if team1.defense_strength > team2.defense_strength else team2_name
                },
                'pk_ability': {
                    team1_name: round(team1.pk_ability, 1),
                    team2_name: round(team2.pk_ability, 1),
                    'winner': team1_name if team1.pk_ability > team2.pk_ability else team2_name
                },
                'xfactor_players': {
                    team1_name: sum(1 for p in team1.players if p.is_xfactor),
                    team2_name: sum(1 for p in team2.players if p.is_xfactor),
                    'winner': team1_name if sum(1 for p in team1.players if p.is_xfactor) > sum(1 for p in team2.players if p.is_xfactor) else team2_name
                }
            },
            'team1_players': [{'name': p.name, 'position': p.position, 'is_xfactor': p.is_xfactor} for p in team1.players],
            'team2_players': [{'name': p.name, 'position': p.position, 'is_xfactor': p.is_xfactor} for p in team2.players]
        }
    
    def get_all_teams(self) -> List[str]:
        return sorted(list(self.teams.keys()))
    
    def get_team_players(self, team_name: str) -> List[Dict]:
        team = self.teams.get(team_name)
        if not team:
            return []
        return [{
            'name': p.name,
            'position': p.position,
            'age': p.age,
            'dribbling_skill': p.dribbling_skill,
            'pace': p.pace,
            'shooting': p.shooting,
            'passing': p.passing,
            'defending': p.defending,
            'fitness_level': p.fitness_level,
            'world_cup_experience': p.world_cup_experience,
            'is_xfactor': p.is_xfactor,
            'xfactor_type': p.xfactor_type,
            'injury_status': p.injury_status
        } for p in team.players]

if __name__ == "__main__":
    engine = FormulaV9('data/wc2026_player_database.json')
    
    print("=== World Cup 2026 Formula V9 Prediction Engine ===")
    print(f"Loaded {len(engine.players)} players from {len(engine.teams)} teams")
    
    test_match = engine.predict_match("Argentina", "Brazil")
    print("\nTest Prediction - Argentina vs Brazil:")
    print(f"Home Win: {test_match['home_win_probability']:.2%}")
    print(f"Draw: {test_match['draw_probability']:.2%}")
    print(f"Away Win: {test_match['away_win_probability']:.2%}")
    print(f"Predicted: {test_match['predicted_result']}")
    print(f"Confidence: {test_match['confidence']}%")
    
    comparison = engine.get_team_comparison("Argentina", "Brazil")
    print("\nTeam Comparison:")
    for stat, data in comparison['comparison'].items():
        print(f"{stat}: {data['Argentina']} vs {data['Brazil']}")