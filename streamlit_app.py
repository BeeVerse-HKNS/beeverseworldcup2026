import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from formula_v9_ultimate import FormulaV9
from tournament_model import TournamentModel
from languages import LANGUAGES, LANGUAGE_NAMES, get_text, get_language_name

st.set_page_config(
    page_title="World Cup 2026 Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

DESIGN_TOKENS = {
    'primary_color': '#1E88E5',
    'primary_color_cn': '#C62828',
    'background': '#FAFAFA',
    'card_bg': '#FFFFFF',
    'text_primary': '#212121',
    'text_secondary': '#757575',
    'border_radius': '8px',
    'shadow': '0 2px 4px rgba(0,0,0,0.1)',
    'font_size_body': '16px',
    'font_size_title': '24px',
}

def get_design_tokens(lang: str) -> dict:
    tokens = DESIGN_TOKENS.copy()
    if lang in ['zh_hant', 'zh_hans']:
        tokens['primary_color'] = tokens['primary_color_cn']
    return tokens

def apply_custom_css(lang: str):
    tokens = get_design_tokens(lang)
    st.markdown(f"""
    <style>
        .main {{
            background-color: {tokens['background']};
        }}
        .stApp {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        }}
        h1 {{
            font-size: {tokens['font_size_title']};
            color: {tokens['text_primary']};
            font-weight: 600;
        }}
        h2, h3 {{
            color: {tokens['text_primary']};
        }}
        .stMetric {{
            background-color: {tokens['card_bg']};
            border-radius: {tokens['border_radius']};
            box-shadow: {tokens['shadow']};
            padding: 1rem;
        }}
        .stButton > button {{
            background-color: {tokens['primary_color']};
            color: white;
            border-radius: {tokens['border_radius']};
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        .stButton > button:hover {{
            filter: brightness(1.1);
        }}
        .stSelectbox, .stMultiSelect {{
            border-radius: {tokens['border_radius']};
        }}
        [data-testid="stSidebar"] {{
            background-color: {tokens['card_bg']};
        }}
        .stSuccess {{
            background-color: #E8F5E9;
            border-left: 4px solid #4CAF50;
        }}
        .stInfo {{
            background-color: #E3F2FD;
            border-left: 4px solid {tokens['primary_color']};
        }}
        .stWarning {{
            background-color: #FFF3E0;
            border-left: 4px solid #FF9800;
        }}
        .stError {{
            background-color: #FFEBEE;
            border-left: 4px solid #F44336;
        }}
        .card {{
            background-color: {tokens['card_bg']};
            border-radius: {tokens['border_radius']};
            box-shadow: {tokens['shadow']};
            padding: 1.5rem;
            margin-bottom: 1rem;
        }}
    </style>
    """, unsafe_allow_html=True)

def init_language():
    if 'language' not in st.session_state:
        st.session_state.language = 'zh_hant'
    return st.session_state.language

def set_language(lang: str):
    st.session_state.language = lang
    st.rerun()

@st.cache_resource
def load_engine():
    try:
        engine = FormulaV9('data/wc2026_player_database.json')
        if len(engine.players) == 0:
            return None
        return engine
    except Exception as e:
        return None

@st.cache_resource
def load_tournament():
    try:
        return TournamentModel('data/wc2026_player_database.json')
    except Exception as e:
        return None

engine = load_engine()
tournament = load_tournament()

def t(key: str) -> str:
    return get_text(key, st.session_state.language)

def main():
    lang = init_language()
    apply_custom_css(lang)
    
    with st.sidebar:
        st.markdown(f"### {t('language')}")
        lang_options = list(LANGUAGE_NAMES.keys())
        lang_labels = [LANGUAGE_NAMES[l] for l in lang_options]
        current_idx = lang_options.index(lang)
        selected_lang_label = st.selectbox(
            "",
            lang_labels,
            index=current_idx,
            label_visibility="collapsed"
        )
        selected_lang = lang_options[lang_labels.index(selected_lang_label)]
        if selected_lang != lang:
            set_language(selected_lang)
        
        st.markdown("---")
        st.title(f"🏆 {t('sidebar_title')}")
        st.markdown("---")
        
        if engine is None:
            st.error(f"❌ {t('engine_load_error')}")
            st.info(t('data_file_missing'))
            return
        
        pages = [
            t('home'),
            t('match_prediction'),
            t('team_comparison'),
            t('player_database'),
            t('tournament_simulation'),
            t('model_analysis')
        ]
        page = st.radio(t('navigation'), pages)
    
    try:
        if page == t('home'):
            show_home()
        elif page == t('match_prediction'):
            show_match_prediction()
        elif page == t('team_comparison'):
            show_team_comparison()
        elif page == t('player_database'):
            show_player_database()
        elif page == t('tournament_simulation'):
            show_tournament_simulation()
        elif page == t('model_analysis'):
            show_model_analysis()
    except Exception as e:
        st.error(f"❌ {t('page_error')}: {str(e)}")
        st.info(t('try_refresh'))

def show_home():
    st.title(f"🏆 {t('app_title')}")
    
    st.markdown(f"""
    {t('welcome_title')}
    
    {t('ai_model_intro')}
    
    - ⚽ **{t('expected_goals')}** — {t('factor_xg').split('—')[1] if '—' in t('factor_xg') else t('factor_xg')}
    - 📊 **{t('factor_v7').split('—')[0] if '—' in t('factor_v7') else t('factor_v7')}** — {t('factor_v7').split('—')[1] if '—' in t('factor_v7') else ''}
    - 🎯 **{t('factor_odds').split('—')[0] if '—' in t('factor_odds') else t('factor_odds')}** — {t('factor_odds').split('—')[1] if '—' in t('factor_odds') else ''}
    - ⭐ **{t('player_factor')}** — {t('factor_player').split('—')[1] if '—' in t('factor_player') else t('factor_player')}
    - 🛡️ **{t('defensive_pk')}** — {t('factor_pk').split('—')[1] if '—' in t('factor_pk') else t('factor_pk')}
    - 🔄 **{t('factor_sub').split('—')[0] if '—' in t('factor_sub') else t('factor_sub')}** — {t('factor_sub').split('—')[1] if '—' in t('factor_sub') else ''}
    - ✨ **{t('xfactor_players')}** — {t('factor_xfactor').split('—')[1] if '—' in t('factor_xfactor') else t('factor_xfactor')}
    
    **{t('features_title')}**
    - {t('feature_predict')}
    - {t('feature_compare')}
    - {t('feature_explore')}
    - {t('feature_simulate')}
    - {t('feature_analyze')}
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(t('metric_teams'), len(engine.get_all_teams()))
    with col2:
        st.metric(t('metric_players'), len(engine.players))
    with col3:
        st.metric(t('metric_xfactor'), sum(1 for p in engine.players if p.is_xfactor))
    
    st.subheader(f"🏅 {t('top_teams_title')}")
    team_strengths = []
    for team_name, team in engine.teams.items():
        team_strengths.append({
            'Team': team_name,
            t('overall_strength'): team.overall_strength,
            t('attack_power'): team.attack_power,
            t('defense_strength'): team.defense_strength,
            t('pk_ability'): team.pk_ability
        })
    
    if not team_strengths:
        st.warning(f"⚠️ {t('no_team_data')}")
        return
    
    df = pd.DataFrame(team_strengths)
    overall_col = t('overall_strength')
    if overall_col not in df.columns:
        st.warning(f"⚠️ {t('data_structure_error')}")
        st.write(df)
        return
    
    df = df.sort_values(overall_col, ascending=False).head(10)
    fig = px.bar(df, x='Team', y=overall_col, color=overall_col, 
                 color_continuous_scale='Viridis', title=t('top_10_teams'))
    st.plotly_chart(fig, use_container_width=True)

def show_match_prediction():
    st.title(f"⚽ {t('match_prediction_title')}")
    
    teams = engine.get_all_teams()
    if not teams:
        st.error(f"❌ {t('no_teams_available')}")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        default_home = teams.index("Brazil") if "Brazil" in teams else 0
        home_team = st.selectbox(t('home_team'), teams, index=default_home)
    with col2:
        default_away = teams.index("Argentina") if "Argentina" in teams else (1 if len(teams) > 1 else 0)
        away_team = st.selectbox(t('away_team'), teams, index=default_away)
    
    st.subheader(f"📈 {t('betting_odds_title')}")
    col3, col4, col5 = st.columns(3)
    with col3:
        home_odds = st.number_input(t('home_win_odds'), min_value=1.01, max_value=50.0, value=2.0, step=0.01)
    with col4:
        draw_odds = st.number_input(t('draw_odds'), min_value=1.01, max_value=50.0, value=3.2, step=0.01)
    with col5:
        away_odds = st.number_input(t('away_win_odds'), min_value=1.01, max_value=50.0, value=3.5, step=0.01)
    
    if st.button(t('predict_match'), use_container_width=True):
        result = engine.predict_match(home_team, away_team, home_odds, draw_odds, away_odds)
        
        if not result['success']:
            st.error(result.get('error', t('prediction_failed')))
            return
        
        st.success(f"**{t('predicted_result')}:** {result['predicted_result']}")
        st.info(f"**{t('confidence_level')}:** {result['confidence']}%")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric(f"{home_team} Win", f"{result['home_win_probability']:.2%}")
        with col_b:
            st.metric("Draw", f"{result['draw_probability']:.2%}")
        with col_c:
            st.metric(f"{away_team} Win", f"{result['away_win_probability']:.2%}")
        
        fig = go.Figure(data=[go.Pie(
            labels=[f"{home_team} Win", "Draw", f"{away_team} Win"],
            values=[result['home_win_probability'], result['draw_probability'], result['away_win_probability']],
            hole=0.3
        )])
        fig.update_layout(title_text=t('probability_distribution'))
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader(f"📊 {t('factor_breakdown')}")
        factors = result['factors']
        
        st.write(f"**{t('expected_goals')}:**")
        xg_df = pd.DataFrame({
            'Team': [home_team, away_team],
            'xG': [factors['xg']['home'], factors['xg']['away']]
        })
        st.bar_chart(xg_df.set_index('Team'))
        
        st.write(f"**{t('player_factor')}:**")
        player_df = pd.DataFrame({
            'Team': [home_team, away_team],
            t('player_factor'): [factors['player_factor']['home'], factors['player_factor']['away']]
        })
        st.bar_chart(player_df.set_index('Team'))
        
        st.write(f"**{t('defensive_pk')}:**")
        pk_df = pd.DataFrame({
            'Team': [home_team, away_team],
            t('pk_ability'): [factors['defensive_pk']['home'], factors['defensive_pk']['away']]
        })
        st.bar_chart(pk_df.set_index('Team'))
        
        st.write(f"**{t('xfactor_players')}:**")
        xfactor_df = pd.DataFrame({
            'Team': [home_team, away_team],
            'X-Factor': [factors['xfactor']['home'], factors['xfactor']['away']]
        })
        st.bar_chart(xfactor_df.set_index('Team'))

def show_team_comparison():
    st.title(f"⚔️ {t('team_comparison_title')}")
    
    teams = engine.get_all_teams()
    if not teams:
        st.error(f"❌ {t('no_teams_available')}")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        default_t1 = teams.index("Argentina") if "Argentina" in teams else 0
        team1 = st.selectbox(t('team_1'), teams, index=default_t1)
    with col2:
        default_t2 = teams.index("Brazil") if "Brazil" in teams else (1 if len(teams) > 1 else 0)
        team2 = st.selectbox(t('team_2'), teams, index=default_t2)
    
    if st.button(t('compare_teams'), use_container_width=True):
        comparison = engine.get_team_comparison(team1, team2)
        
        if not comparison['success']:
            st.error(comparison.get('error', t('comparison_failed')))
            return
        
        st.subheader(f"🏆 {t('5_point_comparison')}")
        
        metrics = ['overall_strength', 'attack_power', 'defense_strength', 'pk_ability', 'xfactor_players']
        metric_names = [t('overall_strength'), t('attack_power'), t('defense_strength'), t('pk_ability'), t('xfactor_players_label')]
        
        for metric, name in zip(metrics, metric_names):
            data = comparison['comparison'][metric]
            winner = data['winner']
            
            col_a, col_b, col_c = st.columns([2, 1, 2])
            with col_a:
                st.write(f"**{team1}:** {data[team1]}")
            with col_b:
                st.write(f"🏆 {winner}")
            with col_c:
                st.write(f"**{team2}:** {data[team2]}")
            
            df = pd.DataFrame({
                'Team': [team1, team2],
                name: [data[team1], data[team2]]
            })
            fig = px.bar(df, x='Team', y=name, color='Team', 
                        color_discrete_map={team1: '#1f77b4', team2: '#ff7f0e'},
                        title=name)
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader(f"📋 {team1} {t('xfactor_list_title')}")
        team1_players = [p for p in comparison['team1_players'] if p['is_xfactor']]
        if team1_players:
            for player in team1_players:
                st.write(f"⭐ {player['name']} ({player['position']})")
        else:
            st.write(t('no_xfactor_players'))
        
        st.subheader(f"📋 {team2} {t('xfactor_list_title')}")
        team2_players = [p for p in comparison['team2_players'] if p['is_xfactor']]
        if team2_players:
            for player in team2_players:
                st.write(f"⭐ {player['name']} ({player['position']})")
        else:
            st.write(t('no_xfactor_players'))

def show_player_database():
    st.title(f"👥 {t('player_database_title')}")
    
    teams = engine.get_all_teams()
    if not teams:
        st.error(f"❌ {t('no_teams_available')}")
        return
    
    selected_team = st.selectbox(t('select_team'), teams)
    
    players = engine.get_team_players(selected_team)
    
    if players:
        df = pd.DataFrame(players)
        df = df[['name', 'position', 'age', 'dribbling_skill', 'pace', 'shooting', 
                 'passing', 'defending', 'fitness_level', 'world_cup_experience', 
                 'is_xfactor', 'injury_status']]
        
        st.dataframe(df, use_container_width=True)
        
        st.subheader(f"📊 {t('attribute_distribution')}")
        
        attributes = ['dribbling_skill', 'pace', 'shooting', 'passing', 'defending', 'fitness_level']
        
        for attr in attributes:
            attr_title = attr.replace("_", " ").title()
            fig = px.histogram(df, x=attr, title=f'{attr_title} {t("distribution_title")}', 
                              nbins=10)
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader(f"⭐ {t('xfactor_players_section')}")
        xfactor_players = df[df['is_xfactor']]
        if not xfactor_players.empty:
            st.dataframe(xfactor_players, use_container_width=True)
        else:
            st.info(t('no_xfactor_in_team'))
    else:
        st.warning(t('no_players_found'))

def show_tournament_simulation():
    st.title(f"🎯 {t('tournament_simulation_title')}")
    
    if tournament is None:
        st.error(f"❌ {t('tournament_model_error')}")
        return
    
    if 'tournament_result' not in st.session_state:
        st.session_state.tournament_result = None
    
    if st.button(f"🎲 {t('simulate_tournament')}", use_container_width=True):
        with st.spinner(t('simulating')):
            st.session_state.tournament_result = tournament.simulate_tournament()
    
    if st.session_state.tournament_result:
        result = st.session_state.tournament_result
        
        st.success(f"**🏆 {t('champion')}:** {result['champion']}")
        st.info(f"**🥈 {t('runner_up')}:** {result['runner_up']}")
        st.info(f"**🥉 {t('third_place')}:** {result['third_place']}")
        
        st.subheader(f"📊 {t('group_stage_results')}")
        for group_name, group_data in result['group_stage'].items():
            st.write(f"**{group_name}:**")
            standings = pd.DataFrame(group_data['standings']).T
            standings = standings.sort_values('points', ascending=False)
            st.dataframe(standings, use_container_width=True)
        
        st.subheader(f"⚔️ {t('knockout_stage')}")
        
        bracket = result['knockout_bracket']
        
        st.write(f"**{t('round_of_16')}:**")
        for match in bracket['round_of_16_results']:
            st.write(f"  {match['match']} → **{match['winner']}** ({t('confidence')}: {match['confidence']}%)")
        
        st.write(f"**{t('quarterfinals')}:**")
        for match in bracket['quarterfinal_results']:
            st.write(f"  {match['match']} → **{match['winner']}** ({t('confidence')}: {match['confidence']}%)")
        
        st.write(f"**{t('semifinals')}:**")
        for match in bracket['semifinal_results']:
            st.write(f"  {match['match']} → **{match['winner']}** ({t('confidence')}: {match['confidence']}%)")
        
        st.write(f"**🏆 {t('final')}:**")
        final = bracket['final_result']
        st.write(f"  {final['match']} → **{final['winner']}** ({t('confidence')}: {final['confidence']}%)")

def show_model_analysis():
    st.title(f"📈 {t('model_analysis_title')}")
    
    st.subheader(f"🔧 {t('factor_weights_title')}")
    
    weights = engine.factor_weights
    labels = ['xg_weight', 'v7_weight', 'odds_weight', 'player_weight', 
              'defensive_pk_weight', 'substitution_weight', 'xfactor_weight']
    display_labels = [t('expected_goals'), 'V7 Base', t('factor_odds').split('—')[0] if '—' in t('factor_odds') else t('factor_odds'), 
                      t('player_factor'), t('defensive_pk'), 'Substitution', 'X-Factor']
    
    weight_df = pd.DataFrame({
        'Factor': display_labels,
        'Weight': [weights[l] for l in labels]
    })
    
    fig = px.pie(weight_df, values='Weight', names='Factor', title=t('weight_distribution'))
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader(f"📊 {t('three_board_params')}")
    params = engine.three_board.factors
    params_df = pd.DataFrame({
        t('parameter'): list(params.keys()),
        t('value'): list(params.values())
    })
    st.dataframe(params_df, use_container_width=True)
    
    st.subheader(f"🏆 {t('team_strength_distribution')}")
    team_data = []
    for team_name, team in engine.teams.items():
        team_data.append({
            'Team': team_name,
            t('overall_strength'): team.overall_strength,
            t('attack_power'): team.attack_power,
            t('defense_strength'): team.defense_strength,
            t('pk_ability'): team.pk_ability
        })
    
    if not team_data:
        st.warning(f"⚠️ {t('no_team_data')}")
        return
    
    df = pd.DataFrame(team_data)
    overall_col = t('overall_strength')
    attack_col = t('attack_power')
    defense_col = t('defense_strength')
    pk_col = t('pk_ability')
    
    fig = px.scatter_matrix(df, dimensions=[overall_col, attack_col, defense_col, pk_col], 
                           title=t('correlation_matrix'),
                           color='Team')
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader(f"📈 {t('top_by_category')}")
    categories = [overall_col, attack_col, defense_col, pk_col]
    for cat in categories:
        top_teams = df.nlargest(5, cat)
        fig = px.bar(top_teams, x='Team', y=cat, title=f"{t('top_5_teams')} - {cat}",
                    color=cat, color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
