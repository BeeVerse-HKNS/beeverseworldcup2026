import json
import math
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Player:
    name: str
    team: str
    position: str
    age: int
    market_value: float
    fitness: int
    form: int
    penalty_skills: int
    dribbling_skill: int
    pace: int
    shooting: int
    passing: int
    defending: int
    is_xfactor: bool
    injury_status: str

@dataclass
class Team:
    name: str
    players: List[Player]
    overall_strength: float
    attack_power: float
    defense_strength: float
    squad_value: float
    xfactor_count: int

class FormulaV5Market:
    def __init__(self, data_path: str):
        self.players = self._load_player_data(data_path)
        self.teams = self._build_team_database()
        self.factor_weights = {
            'attack_power': 0.25,
            'market_odds': 0.20,
            'squad_value': 0.20,
            'form_fitness': 0.20,
            'xfactor': 0.15
        }
        self.max_squad_value = 1000.0
    
    def _load_player_data(self, path: str) -> List[Player]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            players = []
            if 'teams' in data:
                for team_name, team_data in data['teams'].items():
                    for p in team_data.get('players', []):
                        rating = p.get('rating', 75)
                        market_val = p.get('market_value', self._estimate_market_value(rating, p.get('age', 25)))
                        players.append(Player(
                            name=p['name'],
                            team=team_name,
                            position=p['position'],
                            age=p['age'],
                            market_value=market_val,
                            fitness=p.get('fitness', 80),
                            form=p.get('form', 70),
                            penalty_skills=p.get('penalty_skills', 70),
                            dribbling_skill=p.get('dribbling_skill', int(rating * 0.9)),
                            pace=p.get('pace', int(rating * 0.85)),
                            shooting=p.get('shooting', int(rating * 0.8)),
                            passing=p.get('passing', int(rating * 0.85)),
                            defending=p.get('defending', int(rating * 0.7)),
                            is_xfactor=market_val >= 50.0,
                            injury_status=p.get('injury_status', 'fit')
                        ))
            else:
                for p in data.get('players', []):
                    rating = p.get('rating', 75)
                    market_val = p.get('market_value', self._estimate_market_value(rating, p.get('age', 25)))
                    players.append(Player(
                        name=p['name'],
                        team=p['team'],
                        position=p['position'],
                        age=p['age'],
                        market_value=market_val,
                        fitness=p.get('fitness', 80),
                        form=p.get('form', 70),
                        penalty_skills=p.get('penalty_skills', 70),
                        dribbling_skill=p.get('dribbling_skill', int(rating * 0.9)),
                        pace=p.get('pace', int(rating * 0.85)),
                        shooting=p.get('shooting', int(rating * 0.8)),
                        passing=p.get('passing', int(rating * 0.85)),
                        defending=p.get('defending', int(rating * 0.7)),
                        is_xfactor=market_val >= 50.0,
                        injury_status=p.get('injury_status', 'fit')
                    ))
            return players
        except Exception as e:
            print(f"[ERROR] _load_player_data failed: {e}")
            return []
    
    def _estimate_market_value(self, rating: int, age: int) -> float:
        base_value = (rating / 100) ** 2 * 100
        age_factor = 1.0
        if age < 23:
            age_factor = 1.3
        elif age < 27:
            age_factor = 1.0
        elif age < 31:
            age_factor = 0.8
        else:
            age_factor = 0.5
        return base_value * age_factor
    
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
                    'squad_value': 0.0,
                    'xfactor_count': 0
                }
            teams[player.team]['players'].append(player)
            teams[player.team]['sum_dribbling'] += player.dribbling_skill
            teams[player.team]['sum_pace'] += player.pace
            teams[player.team]['sum_shooting'] += player.shooting
            teams[player.team]['sum_passing'] += player.passing
            teams[player.team]['sum_defending'] += player.defending
            teams[player.team]['squad_value'] += player.market_value
            if player.is_xfactor:
                teams[player.team]['xfactor_count'] += 1
        
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
                squad_value=data['squad_value'],
                xfactor_count=data['xfactor_count']
            )
        return team_objects
    
    def calculate_attack_power(self, team: Team, is_home: bool = False) -> float:
        xg = team.attack_power / 100
        team_strength = team.overall_strength / 100
        attack_power = xg * 0.4 + team_strength * 0.6
        if is_home:
            attack_power += 0.03
        return min(1.0, attack_power)
    
    def calculate_market_odds_factor(self, home_team: Team, away_team: Team, 
                                     home_odds: Optional[float] = None,
                                     draw_odds: Optional[float] = None,
                                     away_odds: Optional[float] = None) -> Dict[str, float]:
        if home_odds and draw_odds and away_odds:
            try:
                home_prob = 1.0 / home_odds if home_odds > 0 else 0.333
                draw_prob = 1.0 / draw_odds if draw_odds > 0 else 0.333
                away_prob = 1.0 / away_odds if away_odds > 0 else 0.333
                total = home_prob + draw_prob + away_prob
                if total > 0:
                    home_prob /= total
                    away_prob /= total
                return {'home': home_prob, 'away': away_prob}
            except:
                pass
        
        strength_diff = home_team.overall_strength - away_team.overall_strength
        home_base = 0.5 + (strength_diff / 200) + 0.03
        away_base = 1.0 - home_base
        return {'home': max(0.1, min(0.9, home_base)), 'away': max(0.1, min(0.9, away_base))}
    
    def calculate_squad_value_factor(self, team: Team) -> float:
        normalized = team.squad_value / self.max_squad_value
        return min(1.0, normalized)
    
    def calculate_form_fitness(self, team: Team) -> float:
        if len(team.players) == 0:
            return 0.5
        avg_form = sum(p.form for p in team.players) / len(team.players) / 100
        avg_fitness = sum(p.fitness for p in team.players) / len(team.players) / 100
        avg_penalty = sum(p.penalty_skills for p in team.players) / len(team.players) / 100
        avg_substitution = sum(p.fitness for p in team.players) / len(team.players) / 100
        form_fitness = (avg_form + avg_fitness) / 2 * 0.5 + (avg_penalty + avg_substitution) / 2 * 0.25
        return min(1.0, form_fitness + 0.25)
    
    def calculate_xfactor_factor(self, team: Team) -> int:
        return team.xfactor_count
    
    def predict_match(self, home_team: str, away_team: str,
                     home_odds: Optional[float] = None,
                     draw_odds: Optional[float] = None,
                     away_odds: Optional[float] = None) -> Dict:
        home = self.teams.get(home_team)
        away = self.teams.get(away_team)
        
        if not home or not away:
            return {
                'success': False,
                'error': f"Teams not found: {home_team} or {away_team}"
            }
        
        attack_home = self.calculate_attack_power(home, is_home=True)
        attack_away = self.calculate_attack_power(away, is_home=False)
        
        market_odds = self.calculate_market_odds_factor(home, away, home_odds, draw_odds, away_odds)
        
        squad_home = self.calculate_squad_value_factor(home)
        squad_away = self.calculate_squad_value_factor(away)
        
        form_home = self.calculate_form_fitness(home)
        form_away = self.calculate_form_fitness(away)
        
        xfactor_home = self.calculate_xfactor_factor(home)
        xfactor_away = self.calculate_xfactor_factor(away)
        max_xfactor = max(xfactor_home, xfactor_away, 1)
        xfactor_home_norm = xfactor_home / max_xfactor
        xfactor_away_norm = xfactor_away / max_xfactor
        
        home_score = (
            attack_home * self.factor_weights['attack_power'] +
            market_odds['home'] * self.factor_weights['market_odds'] +
            squad_home * self.factor_weights['squad_value'] +
            form_home * self.factor_weights['form_fitness'] +
            xfactor_home_norm * self.factor_weights['xfactor']
        )
        
        away_score = (
            attack_away * self.factor_weights['attack_power'] +
            market_odds['away'] * self.factor_weights['market_odds'] +
            squad_away * self.factor_weights['squad_value'] +
            form_away * self.factor_weights['form_fitness'] +
            xfactor_away_norm * self.factor_weights['xfactor']
        )
        
        total = home_score + away_score
        if total == 0:
            total = 1.0
        
        home_win_prob = home_score / total
        away_win_prob = away_score / total
        
        draw_base = 0.25
        strength_diff = abs(home.overall_strength - away.overall_strength)
        draw_modifier = max(0, 0.15 - strength_diff / 500)
        draw_prob = draw_base * (1 + draw_modifier)
        
        remaining = 1.0 - draw_prob
        home_win_prob = home_win_prob * remaining
        away_win_prob = away_win_prob * remaining
        
        if home_win_prob > away_win_prob:
            result = 'HOME_WIN'
        elif away_win_prob > home_win_prob:
            result = 'AWAY_WIN'
        else:
            result = 'DRAW'
        
        if draw_prob > home_win_prob and draw_prob > away_win_prob:
            result = 'DRAW'
        
        return {
            'success': True,
            'home_team': home_team,
            'away_team': away_team,
            'predicted_result': result,
            'home_win_prob': round(home_win_prob, 4),
            'draw_prob': round(draw_prob, 4),
            'away_win_prob': round(away_win_prob, 4),
            'factors': {
                'attack_power': {
                    'home': round(attack_home, 4),
                    'away': round(attack_away, 4)
                },
                'market_odds': {
                    'home': round(market_odds['home'], 4),
                    'away': round(market_odds['away'], 4)
                },
                'squad_value': {
                    'home': round(squad_home, 4),
                    'away': round(squad_away, 4)
                },
                'form_fitness': {
                    'home': round(form_home, 4),
                    'away': round(form_away, 4)
                },
                'xfactor': {
                    'home': xfactor_home,
                    'away': xfactor_away
                }
            },
            'model': '5-Factor Market Model'
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
            'market_value': p.market_value,
            'fitness': p.fitness,
            'form': p.form,
            'penalty_skills': p.penalty_skills,
            'is_xfactor': p.is_xfactor,
            'injury_status': p.injury_status
        } for p in team.players]

if __name__ == "__main__":
    engine = FormulaV5Market('data/wc2026_player_database.json')
    
    print("=== World Cup 2026 Formula V5 Market Prediction Engine ===")
    print(f"Loaded {len(engine.players)} players from {len(engine.teams)} teams")
    
    test_match = engine.predict_match("Argentina", "Brazil")
    print("\nTest Prediction - Argentina vs Brazil:")
    print(f"Home Win: {test_match['home_win_prob']:.2%}")
    print(f"Draw: {test_match['draw_prob']:.2%}")
    print(f"Away Win: {test_match['away_win_prob']:.2%}")
    print(f"Predicted: {test_match['predicted_result']}")
    print(f"Model: {test_match['model']}")
    
    print("\nFactors Breakdown:")
    for factor, values in test_match['factors'].items():
        print(f"  {factor}: Home={values['home']}, Away={values['away']}")
