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
            if 'teams' in data:
                for team_name, team_data in data['teams'].items():
                    for p in team_data.get('players', []):
                        rating = p.get('rating', 75)
                        players.append(Player(
                            name=p['name'],
                            team=team_name,
                            position=p['position'],
                            age=p['age'],
                            dribbling_skill=p.get('dribbling_skill', int(rating * 0.9)),
                            pace=p.get('pace', int(rating * 0.85)),
                            shooting=p.get('shooting', int(rating * 0.8)),
                            passing=p.get('passing', int(rating * 0.85)),
                            defending=p.get('defending', int(rating * 0.7)),
                            fitness_level=p.get('fitness_level', p.get('fitness', 80)),
                            world_cup_experience=p.get('world_cup_experience', p.get('experience', 0)),
                            is_xfactor=p.get('is_xfactor', rating >= 90),
                            xfactor_type=p.get('xfactor_type'),
                            injury_status=p.get('injury_status', 'fit')
                        ))
            else:
                for p in data.get('players', []):
                    rating = p.get('rating', 75)
                    players.append(Player(
                        name=p['name'],
                        team=p['team'],
                        position=p['position'],
                        age=p['age'],
                        dribbling_skill=p.get('dribbling_skill', int(rating * 0.9)),
                        pace=p.get('pace', int(rating * 0.85)),
                        shooting=p.get('shooting', int(rating * 0.8)),
                        passing=p.get('passing', int(rating * 0.85)),
                        defending=p.get('defending', int(rating * 0.7)),
                        fitness_level=p.get('fitness_level', p.get('fitness', 80)),
                        world_cup_experience=p.get('world_cup_experience', p.get('experience', 0)),
                        is_xfactor=p.get('is_xfactor', rating >= 90),
                        xfactor_type=p.get('xfactor_type'),
                        injury_status=p.get('injury_status', 'fit')
                    ))
            return players
        except Exception as e:
            print(f"[ERROR] _load_player_data failed: {e}")
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
    
    def explain_prediction(self, home_team_name: str, away_team_name: str, 
                          home_odds: float = 2.0, draw_odds: float = 3.2, away_odds: float = 3.5) -> Dict:
        prediction = self.predict_match(home_team_name, away_team_name, home_odds, draw_odds, away_odds)
        
        if not prediction.get('success', False):
            return prediction
        
        home_team = self.teams.get(home_team_name)
        away_team = self.teams.get(away_team_name)
        
        factors_detail = {}
        
        xg_home = prediction['factors']['xg']['home']
        xg_away = prediction['factors']['xg']['away']
        xg_diff = xg_home - xg_away
        factors_detail['xg'] = {
            'name': 'Expected Goals (xG)',
            'home_value': xg_home,
            'away_value': xg_away,
            'diff': round(xg_diff, 4),
            'contribution': 0.0,
            'explanation': f"{home_team_name} 嘅進攻能力（{home_team.attack_power:.1f}）vs {away_team_name} 嘅防守（{away_team.defense_strength:.1f}），預期進球 {'較多' if xg_diff > 0 else '較少' if xg_diff < 0 else '相若'}",
            'calculation': f"attack_power({home_team.attack_power:.1f}) / 100 × (100 - defense({away_team.defense_strength:.1f})) / 100 × 1.5 = {xg_home:.4f}",
            'weight': self.factor_weights['xg_weight']
        }
        
        v7_base = prediction['factors']['v7_base']
        v7_diff = (v7_base - 0.5) * 2
        factors_detail['v7_base'] = {
            'name': 'V7 Base (主場優勢 + 實力差)',
            'home_value': round(v7_base, 4),
            'away_value': round(1 - v7_base + 0.5, 4),
            'diff': round(v7_diff, 4),
            'contribution': 0.0,
            'explanation': f"主場優勢（+0.05）+ 實力差（{home_team.overall_strength:.1f} - {away_team.overall_strength:.1f}）/ 100 = {v7_base:.4f}，{'主隊佔優' if v7_diff > 0 else '客隊佔優' if v7_diff < 0 else '勢均力敵'}",
            'calculation': f"0.5 + (strength_diff({home_team.overall_strength:.1f} - {away_team.overall_strength:.1f}) / 100) + 0.05 = {v7_base:.4f}",
            'weight': self.factor_weights['v7_weight']
        }
        
        odds_home = prediction['factors']['odds_composite']['home']
        odds_away = prediction['factors']['odds_composite']['away']
        odds_diff = (odds_home - 0.5) * 2
        factors_detail['odds'] = {
            'name': 'Odds Composite (市場預期)',
            'home_value': odds_home,
            'away_value': odds_away,
            'diff': round(odds_diff, 4),
            'contribution': 0.0,
            'explanation': f"賠率轉換：主勝 {home_odds:.2f} → {odds_home:.2%}，客勝 {away_odds:.2f} → {odds_away:.2%}，市場{'看好主隊' if odds_diff > 0 else '看好客隊' if odds_diff < 0 else '認為勢均力敵'}",
            'calculation': f"1 / {home_odds:.2f} = {odds_home:.4f}（歸一化後），diff = ({odds_home:.4f} - 0.5) × 2 = {odds_diff:.4f}",
            'weight': self.factor_weights['odds_weight']
        }
        
        player_home = prediction['factors']['player_factor']['home']
        player_away = prediction['factors']['player_factor']['away']
        player_diff = player_home - player_away
        home_xfactor_count = sum(1 for p in home_team.players if p.is_xfactor)
        away_xfactor_count = sum(1 for p in away_team.players if p.is_xfactor)
        factors_detail['player'] = {
            'name': 'Player Factor (球員綜合素質)',
            'home_value': player_home,
            'away_value': player_away,
            'diff': round(player_diff, 4),
            'contribution': 0.0,
            'explanation': f"X-Factor 球員數：{home_team_name} {home_xfactor_count} vs {away_team_name} {away_xfactor_count}，體能同經驗綜合評估",
            'calculation': f"0.5 + xfactor_bonus({home_xfactor_count}×0.05) + fitness_avg + exp_bonus",
            'weight': self.factor_weights['player_weight']
        }
        
        def_pk_home = prediction['factors']['defensive_pk']['home']
        def_pk_away = prediction['factors']['defensive_pk']['away']
        def_pk_diff = def_pk_home - def_pk_away
        factors_detail['defensive_pk'] = {
            'name': 'Defensive PK (防守 + 門將)',
            'home_value': def_pk_home,
            'away_value': def_pk_away,
            'diff': round(def_pk_diff, 4),
            'contribution': 0.0,
            'explanation': f"防守穩定性：{home_team_name} {home_team.defense_strength:.1f} vs {away_team_name} {away_team.defense_strength:.1f}，門將能力綜合評估",
            'calculation': f"(defense({home_team.defense_strength:.1f}) / 100 + gk_skill) / 2 = {def_pk_home:.4f}",
            'weight': self.factor_weights['defensive_pk_weight']
        }
        
        sub_home = prediction['factors']['substitution']['home']
        sub_away = prediction['factors']['substitution']['away']
        sub_diff = sub_home - sub_away
        factors_detail['substitution'] = {
            'name': 'Substitution Effect (後備質量)',
            'home_value': sub_home,
            'away_value': sub_away,
            'diff': round(sub_diff, 4),
            'contribution': 0.0,
            'explanation': f"後備球員體能水平影響換人策略，{home_team_name} 後備質量 {'較優' if sub_diff > 0 else '較差' if sub_diff < 0 else '相若'}",
            'calculation': f"bench_fitness_avg × 0.15 = {sub_home:.4f}",
            'weight': self.factor_weights['substitution_weight']
        }
        
        xfactor_home = prediction['factors']['xfactor']['home']
        xfactor_away = prediction['factors']['xfactor']['away']
        xfactor_diff = xfactor_home - xfactor_away
        factors_detail['xfactor'] = {
            'name': 'X-Factor (關鍵球員能力)',
            'home_value': xfactor_home,
            'away_value': xfactor_away,
            'diff': round(xfactor_diff, 4),
            'contribution': 0.0,
            'explanation': f"關鍵球員嘅盤扭、速度、射門能力綜合，{home_team_name} X-Factor {'較強' if xfactor_diff > 0 else '較弱' if xfactor_diff < 0 else '相若'}",
            'calculation': f"(max_dribble + max_pace + max_shooting) / 3 × 1.4 = {xfactor_home:.4f}",
            'weight': self.factor_weights['xfactor_weight']
        }
        
        weighted_values = {
            'xg': abs(xg_diff * self.factor_weights['xg_weight']),
            'v7_base': abs(v7_diff * self.factor_weights['v7_weight']),
            'odds': abs(odds_diff * self.factor_weights['odds_weight']),
            'player': abs(player_diff * self.factor_weights['player_weight']),
            'defensive_pk': abs(def_pk_diff * self.factor_weights['defensive_pk_weight']),
            'substitution': abs(sub_diff * self.factor_weights['substitution_weight']),
            'xfactor': abs(xfactor_diff * self.factor_weights['xfactor_weight'])
        }
        
        total_weighted = sum(weighted_values.values())
        
        for factor_key in factors_detail:
            if total_weighted > 0:
                factors_detail[factor_key]['contribution'] = round(weighted_values[factor_key] / total_weighted * 100, 2)
            else:
                factors_detail[factor_key]['contribution'] = round(100 / 7, 2)
        
        sorted_factors = sorted(factors_detail.items(), key=lambda x: x[1]['contribution'], reverse=True)
        key_factors = [factor_key for factor_key, _ in sorted_factors[:3]]
        
        summary_parts = []
        winner = home_team_name if prediction['home_win_probability'] > prediction['away_win_probability'] else away_team_name
        loser = away_team_name if winner == home_team_name else home_team_name
        
        if prediction['predicted_result'] == 'DRAW':
            summary_parts.append(f"{home_team_name} 同 {away_team_name} 實力接近，預測為和局")
        else:
            summary_parts.append(f"{winner} 勝率較高（{max(prediction['home_win_probability'], prediction['away_win_probability']):.2%}）")
        
        key_factor_names = [factors_detail[k]['name'].split(' (')[0] for k in key_factors]
        summary_parts.append(f"主要因為：{', '.join(key_factor_names)}")
        
        for i, (factor_key, factor_data) in enumerate(sorted_factors[:2]):
            if factor_data['diff'] != 0:
                better_team = home_team_name if factor_data['diff'] > 0 else away_team_name
                summary_parts.append(f"{factor_data['name'].split(' (')[0]}：{better_team} 佔優（貢獻度 {factor_data['contribution']:.1f}%）")
        
        summary = "。".join(summary_parts) + "。"
        
        confidence = prediction['confidence']
        confidence_explanation = f"基於 7 大因素綜合分析，信心度為 {confidence}%（"
        if confidence >= 85:
            confidence_explanation += "高信心）"
        elif confidence >= 75:
            confidence_explanation += "中高信心）"
        elif confidence >= 65:
            confidence_explanation += "中等信心）"
        else:
            confidence_explanation += "低信心，結果可能受其他因素影響）"
        
        return {
            'success': True,
            'prediction': prediction,
            'explanation': {
                'summary': summary,
                'key_factors': key_factors,
                'factors_detail': factors_detail,
                'total_contribution': 100.0,
                'confidence_explanation': confidence_explanation,
                'winner_analysis': {
                    'predicted_winner': winner if prediction['predicted_result'] != 'DRAW' else 'DRAW',
                    'win_probability': max(prediction['home_win_probability'], prediction['away_win_probability']),
                    'key_advantages': [
                        {
                            'factor': factors_detail[k]['name'],
                            'advantage': factors_detail[k]['explanation'],
                            'contribution': factors_detail[k]['contribution']
                        }
                        for k in key_factors
                    ]
                }
            }
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