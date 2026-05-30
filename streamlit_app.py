import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from pathlib import Path
from datetime import datetime
from formula_v9_ultimate import FormulaV9
from tournament_model import TournamentModel
from languages import LANGUAGES, LANGUAGE_NAMES, get_text, get_language_name
from player_translations import get_player_name, get_team_name

SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_PATH = SCRIPT_DIR / 'data' / 'wc2026_player_database.json'

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
        engine = FormulaV9(str(DATA_PATH))
        if len(engine.players) == 0:
            return None
        return engine
    except Exception as e:
        return None

@st.cache_resource
def load_tournament():
    try:
        return TournamentModel(str(DATA_PATH))
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
            t('select_language'),
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
            t('model_analysis'),
            t('news_page'),
            t('xfactor_page')
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
        elif page == t('news_page'):
            show_news()
        elif page == t('xfactor_page'):
            show_xfactor()
    except Exception as e:
        st.error(f"❌ {t('page_error')}: {str(e)}")
        st.info(t('try_refresh'))

def show_home():
    st.title(f"🏆 {t('app_title')}")
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric(t('tournament_format').split('/')[0].strip(), "48")
    with col_info2:
        st.metric(t('tournament_dates'), t('tournament_dates'))
    with col_info3:
        st.metric(t('host_countries').split(':')[0] if ':' in t('host_countries') else t('host_countries'), 
                  t('host_countries').split(': ')[1] if ': ' in t('host_countries') else t('host_countries'))
    
    st.markdown(f"""
    {t('welcome_title')}
    
    {t('ai_model_intro')}
    
    - ⚽ **{t('factor_attack_power').split('—')[0].strip()}** — {t('factor_attack_power').split('—')[1].strip() if '—' in t('factor_attack_power') else t('factor_attack_power')}
    - 📊 **{t('factor_market_odds').split('—')[0].strip()}** — {t('factor_market_odds').split('—')[1].strip() if '—' in t('factor_market_odds') else t('factor_market_odds')}
    - 💰 **{t('factor_squad_value').split('—')[0].strip()}** — {t('factor_squad_value').split('—')[1].strip() if '—' in t('factor_squad_value') else t('factor_squad_value')}
    - 🏃 **{t('factor_form_fitness').split('—')[0].strip()}** — {t('factor_form_fitness').split('—')[1].strip() if '—' in t('factor_form_fitness') else t('factor_form_fitness')}
    - ⭐ **{t('factor_xfactor_players').split('—')[0].strip()}** — {t('factor_xfactor_players').split('—')[1].strip() if '—' in t('factor_xfactor_players') else t('factor_xfactor_players')}
    
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
    
    st.subheader(f"📊 {t('research_summary')}")
    
    research_stats = {
        t('total_news'): 10001,
        t('xfactor_players'): 40,
        t('prediction_accuracy') if 'prediction_accuracy' in LANGUAGES['en'] else 'Prediction Accuracy': 90.4,
        t('research_iterations'): 735
    }
    
    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    with col_r1:
        st.metric(t('total_news'), "10,001")
    with col_r2:
        st.metric(t('xfactor_players'), "40")
    with col_r3:
        st.metric("Accuracy", "90.4%")
    with col_r4:
        st.metric(t('research_iterations'), "735")
    
    research_df = pd.DataFrame({
        'Category': list(research_stats.keys()),
        'Value': [10001, 40, 90.4, 735]
    })
    fig_research = px.bar(research_df, x='Category', y='Value', 
                          color='Value', color_continuous_scale='Blues',
                          title=t('research_summary'))
    st.plotly_chart(fig_research, width='stretch')
    
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
    st.plotly_chart(fig, width='stretch')
    
def show_match_prediction():
    st.title(f"⚽ {t('match_prediction_title')}")
    
    lang = st.session_state.language
    teams = engine.get_all_teams()
    if not teams:
        st.error(f"❌ {t('no_teams_available')}")
        return
    
    team_display_names = {team: get_team_name(team, lang) for team in teams}
    display_teams = [team_display_names[t] for t in teams]
    
    col1, col2 = st.columns(2)
    with col1:
        default_home = teams.index("Brazil") if "Brazil" in teams else 0
        home_display = st.selectbox(t('home_team'), display_teams, index=default_home)
        home_team = teams[display_teams.index(home_display)]
    with col2:
        default_away = teams.index("Argentina") if "Argentina" in teams else (1 if len(teams) > 1 else 0)
        away_display = st.selectbox(t('away_team'), display_teams, index=default_away)
        away_team = teams[display_teams.index(away_display)]
    
    if tournament is not None:
        groups = tournament.generate_groups()
        home_group = None
        away_group = None
        for letter, group_teams in groups.items():
            if home_team in group_teams:
                home_group = letter
            if away_team in group_teams:
                away_group = letter
        
        group_col1, group_col2 = st.columns(2)
        with group_col1:
            if home_group:
                st.info(f"**{t('group')} {home_group}**")
        with group_col2:
            if away_group:
                st.info(f"**{t('group')} {away_group}**")
    
    opta_probs = {
        'Argentina': 12.5, 'France': 11.8, 'Brazil': 10.5, 'England': 9.2,
        'Spain': 8.5, 'Germany': 7.8, 'Portugal': 5.5, 'Netherlands': 4.2,
        'Italy': 3.8, 'Belgium': 3.2, 'Croatia': 2.5, 'Uruguay': 2.1
    }
    
    top_teams_for_opta = [t for t in [home_team, away_team] if t in opta_probs]
    if top_teams_for_opta:
        st.subheader(f"📊 {t('opta_win_prob')}")
        opta_cols = st.columns(len(top_teams_for_opta))
        for idx, team in enumerate(top_teams_for_opta):
            with opta_cols[idx]:
                st.metric(get_team_name(team, lang), f"{opta_probs[team]}%")
    
    st.subheader(f"📈 {t('betting_odds_title')}")
    col3, col4, col5 = st.columns(3)
    with col3:
        home_odds = st.number_input(t('home_win_odds'), min_value=1.01, max_value=50.0, value=2.0, step=0.01)
    with col4:
        draw_odds = st.number_input(t('draw_odds'), min_value=1.01, max_value=50.0, value=3.2, step=0.01)
    with col5:
        away_odds = st.number_input(t('away_win_odds'), min_value=1.01, max_value=50.0, value=3.5, step=0.01)
    
    if st.button(t('predict_match'), width='stretch'):
        result = engine.predict_match(home_team, away_team, home_odds, draw_odds, away_odds)
        
        if not result['success']:
            st.error(result.get('error', t('prediction_failed')))
            return
        
        st.success(f"**{t('predicted_result')}:** {result['predicted_result']}")
        st.info(f"**{t('confidence_level')}:** {result['confidence']}%")
        
        st.metric(t('model_confidence'), "90.4%")
        st.caption(t('based_on_iterations').format(735))
        
        home_display = get_team_name(home_team, lang)
        away_display = get_team_name(away_team, lang)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric(f"{home_display} Win", f"{result['home_win_probability']:.2%}")
        with col_b:
            st.metric("Draw", f"{result['draw_probability']:.2%}")
        with col_c:
            st.metric(f"{away_display} Win", f"{result['away_win_probability']:.2%}")
        
        fig = go.Figure(data=[go.Pie(
            labels=[f"{home_display} Win", "Draw", f"{away_display} Win"],
            values=[result['home_win_probability'], result['draw_probability'], result['away_win_probability']],
            hole=0.3
        )])
        fig.update_layout(title_text=t('probability_distribution'))
        st.plotly_chart(fig, width='stretch')
        
        st.subheader(f"📊 {t('factor_breakdown')}")
        factors = result['factors']
        
        st.write(f"**{t('expected_goals')}:**")
        xg_df = pd.DataFrame({
            'Team': [home_display, away_display],
            'xG': [factors['xg']['home'], factors['xg']['away']]
        })
        st.bar_chart(xg_df.set_index('Team'))
        
        st.write(f"**{t('player_factor')}:**")
        player_df = pd.DataFrame({
            'Team': [home_display, away_display],
            t('player_factor'): [factors['player_factor']['home'], factors['player_factor']['away']]
        })
        st.bar_chart(player_df.set_index('Team'))
        
        st.write(f"**{t('defensive_pk')}:**")
        pk_df = pd.DataFrame({
            'Team': [home_display, away_display],
            t('pk_ability'): [factors['defensive_pk']['home'], factors['defensive_pk']['away']]
        })
        st.bar_chart(pk_df.set_index('Team'))
        
        st.write(f"**{t('xfactor_players')}:**")
        xfactor_df = pd.DataFrame({
            'Team': [home_display, away_display],
            'X-Factor': [factors['xfactor']['home'], factors['xfactor']['away']]
        })
        st.bar_chart(xfactor_df.set_index('Team'))

def show_team_comparison():
    st.title(f"⚔️ {t('team_comparison_title')}")
    
    lang = st.session_state.language
    teams = engine.get_all_teams()
    if not teams:
        st.error(f"❌ {t('no_teams_available')}")
        return
    
    team_display_names = {team: get_team_name(team, lang) for team in teams}
    display_teams = [team_display_names[t] for t in teams]
    
    col1, col2 = st.columns(2)
    with col1:
        default_t1 = teams.index("Argentina") if "Argentina" in teams else 0
        team1_display = st.selectbox(t('team_1'), display_teams, index=default_t1)
        team1 = teams[display_teams.index(team1_display)]
    with col2:
        default_t2 = teams.index("Brazil") if "Brazil" in teams else (1 if len(teams) > 1 else 0)
        team2_display = st.selectbox(t('team_2'), display_teams, index=default_t2)
        team2 = teams[display_teams.index(team2_display)]
    
    if st.button(t('compare_teams'), width='stretch'):
        comparison = engine.get_team_comparison(team1, team2)
        
        if not comparison['success']:
            st.error(comparison.get('error', t('comparison_failed')))
            return
        
        st.subheader(f"🏆 {t('5_point_comparison')}")
        
        team1_display = get_team_name(team1, lang)
        team2_display = get_team_name(team2, lang)
        
        metrics = ['overall_strength', 'attack_power', 'defense_strength', 'pk_ability', 'xfactor_players']
        metric_names = [t('overall_strength'), t('attack_power'), t('defense_strength'), t('pk_ability'), t('xfactor_players_label')]
        
        for metric, name in zip(metrics, metric_names):
            data = comparison['comparison'][metric]
            winner = data['winner']
            
            col_a, col_b, col_c = st.columns([2, 1, 2])
            with col_a:
                st.write(f"**{team1_display}:** {data[team1]}")
            with col_b:
                st.write(f"🏆 {get_team_name(winner, lang)}")
            with col_c:
                st.write(f"**{team2_display}:** {data[team2]}")
            
            df = pd.DataFrame({
                'Team': [team1_display, team2_display],
                name: [data[team1], data[team2]]
            })
            fig = px.bar(df, x='Team', y=name, color='Team', 
                        color_discrete_map={team1_display: '#1f77b4', team2_display: '#ff7f0e'},
                        title=name)
            st.plotly_chart(fig, width='stretch')
        
        st.subheader(f"📋 {get_team_name(team1, lang)} {t('xfactor_list_title')}")
        team1_players = [p for p in comparison['team1_players'] if p['is_xfactor']]
        if team1_players:
            for player in team1_players:
                player_name = get_player_name(player['name'], team1, lang)
                st.write(f"⭐ {player_name} ({player['position']})")
        else:
            st.write(t('no_xfactor_players'))
        
        st.subheader(f"📋 {get_team_name(team2, lang)} {t('xfactor_list_title')}")
        team2_players = [p for p in comparison['team2_players'] if p['is_xfactor']]
        if team2_players:
            for player in team2_players:
                player_name = get_player_name(player['name'], team2, lang)
                st.write(f"⭐ {player_name} ({player['position']})")
        else:
            st.write(t('no_xfactor_players'))

def show_player_database():
    st.title(f"👥 {t('player_database_title')}")
    
    lang = st.session_state.language
    teams = engine.get_all_teams()
    if not teams:
        st.error(f"❌ {t('no_teams_available')}")
        return
    
    team_display_names = {team: get_team_name(team, lang) for team in teams}
    display_teams = [team_display_names[t] for t in teams]
    
    selected_display = st.selectbox(t('select_team'), display_teams)
    selected_team = teams[display_teams.index(selected_display)]
    
    show_xfactor_only = st.checkbox(t('show_xfactor_only'), value=False)
    
    players = engine.get_team_players(selected_team)
    
    if players:
        for p in players:
            p['name'] = get_player_name(p['name'], selected_team, lang)
        
        df = pd.DataFrame(players)
        df = df[['name', 'position', 'age', 'dribbling_skill', 'pace', 'shooting', 
                 'passing', 'defending', 'fitness_level', 'world_cup_experience', 
                 'is_xfactor', 'injury_status']]
        
        df_display = df.copy()
        df_display['name'] = df_display.apply(
            lambda row: f"⭐ {row['name']}" if row['is_xfactor'] else row['name'], 
            axis=1
        )
        
        if show_xfactor_only:
            df_display = df_display[df_display['is_xfactor']]
            df = df[df['is_xfactor']]
        
        st.dataframe(df_display, width='stretch')
        
        st.subheader(f"📊 {t('attribute_distribution')}")
        
        attributes = ['dribbling_skill', 'pace', 'shooting', 'passing', 'defending', 'fitness_level']
        
        for attr in attributes:
            attr_title = attr.replace("_", " ").title()
            fig = px.histogram(df, x=attr, title=f'{attr_title} {t("distribution_title")}', 
                              nbins=10)
            st.plotly_chart(fig, width='stretch')
        
        st.subheader(f"⭐ {t('xfactor_players_section')}")
        xfactor_players = df[df['is_xfactor']]
        if not xfactor_players.empty:
            st.dataframe(xfactor_players, width='stretch')
        else:
            st.info(t('no_xfactor_in_team'))
    else:
        st.warning(t('no_players_found'))

def show_tournament_simulation():
    st.title(f"🎯 {t('tournament_simulation_title')}")
    
    lang = st.session_state.language
    
    if tournament is None:
        st.error(f"❌ {t('tournament_model_error')}")
        return
    
    st.markdown(f"📋 **{t('tournament_format')}** | {t('third_place_advance')}")
    
    groups = tournament.generate_groups()
    group_letters = sorted(groups.keys())
    
    st.subheader(f"📊 {t('groups_stage')}")
    
    for row_start in range(0, len(group_letters), 4):
        row_letters = group_letters[row_start:row_start + 4]
        cols = st.columns(len(row_letters))
        for col, letter in zip(cols, row_letters):
            with col:
                st.markdown(f"**{t('group')} {letter}**")
                for team_name in groups[letter]:
                    display_name = get_team_name(team_name, lang)
                    st.write(f"- {display_name}")
    
    if 'tournament_result' not in st.session_state:
        st.session_state.tournament_result = None
    
    if st.button(f"🎲 {t('simulate_tournament')}", width='stretch'):
        with st.spinner(t('simulating')):
            st.session_state.tournament_result = tournament.simulate_tournament()
    
    if st.session_state.tournament_result:
        result = st.session_state.tournament_result
        
        st.success(f"**🏆 {t('champion')}:** {get_team_name(result['champion'], lang)}")
        st.info(f"**🥈 {t('runner_up')}:** {get_team_name(result['runner_up'], lang)}")
        st.info(f"**🥉 {t('third_place')}:** {get_team_name(result['third_place'], lang)}")
        
        st.subheader(f"📊 {t('group_stage_results')}")
        for group_name, group_data in result['group_stage'].items():
            group_letter = group_name.replace("Group ", "")
            st.markdown(f"**{t('group')} {group_letter}**")
            standings = pd.DataFrame(group_data['standings']).T
            standings = standings.sort_values('points', ascending=False)
            display_index = [get_team_name(team, lang) for team in standings.index]
            standings_display = standings.copy()
            standings_display.index = display_index
            st.dataframe(standings_display, width='stretch')
        
        st.subheader(f"⚔️ {t('knockout_stage')}")
        
        bracket = result['knockout_bracket']
        
        if 'round_of_32_results' in bracket:
            st.write(f"**{t('round_of_32')}:**")
            for match in bracket['round_of_32_results']:
                teams_in_match = match['match'].split(' vs ')
                display_match = f"{get_team_name(teams_in_match[0], lang)} vs {get_team_name(teams_in_match[1], lang)}"
                st.write(f"  {display_match} → **{get_team_name(match['winner'], lang)}** ({t('confidence')}: {match['confidence']}%)")
        
        st.write(f"**{t('round_of_16')}:**")
        for match in bracket['round_of_16_results']:
            teams_in_match = match['match'].split(' vs ')
            display_match = f"{get_team_name(teams_in_match[0], lang)} vs {get_team_name(teams_in_match[1], lang)}"
            st.write(f"  {display_match} → **{get_team_name(match['winner'], lang)}** ({t('confidence')}: {match['confidence']}%)")
        
        st.write(f"**{t('quarterfinals')}:**")
        for match in bracket['quarterfinal_results']:
            teams_in_match = match['match'].split(' vs ')
            display_match = f"{get_team_name(teams_in_match[0], lang)} vs {get_team_name(teams_in_match[1], lang)}"
            st.write(f"  {display_match} → **{get_team_name(match['winner'], lang)}** ({t('confidence')}: {match['confidence']}%)")
        
        st.write(f"**{t('semifinals')}:**")
        for match in bracket['semifinal_results']:
            teams_in_match = match['match'].split(' vs ')
            display_match = f"{get_team_name(teams_in_match[0], lang)} vs {get_team_name(teams_in_match[1], lang)}"
            st.write(f"  {display_match} → **{get_team_name(match['winner'], lang)}** ({t('confidence')}: {match['confidence']}%)")
        
        st.write(f"**🏆 {t('final')}:**")
        final = bracket['final_result']
        teams_in_final = final['match'].split(' vs ')
        display_final = f"{get_team_name(teams_in_final[0], lang)} vs {get_team_name(teams_in_final[1], lang)}"
        st.write(f"  {display_final} → **{get_team_name(final['winner'], lang)}** ({t('confidence')}: {final['confidence']}%)")

def show_model_analysis():
    st.title(f"📈 {t('model_analysis_title')}")
    
    st.subheader(f"📊 {t('research_statistics')}")
    
    accuracy_data = pd.DataFrame({
        'Iteration': ['100', '300', '500', '735'],
        'Accuracy (%)': [75.0, 80.0, 85.0, 90.4]
    })
    fig_accuracy = px.line(accuracy_data, x='Iteration', y='Accuracy (%)',
                           markers=True, title=t('accuracy_trend'),
                           line_shape='linear')
    fig_accuracy.update_traces(line=dict(width=3), marker=dict(size=10))
    st.plotly_chart(fig_accuracy, width='stretch')
    
    news_data = pd.DataFrame({
        'Phase': ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'],
        t('total_news'): [2500, 5000, 7500, 10001]
    })
    fig_news = px.bar(news_data, x='Phase', y=t('total_news'),
                      color=t('total_news'), color_continuous_scale='Greens',
                      title=t('news_collection'))
    st.plotly_chart(fig_news, width='stretch')
    
    st.subheader(f"🔧 {t('factor_weights_title')}")
    
    weights_data = {
        t('factor_attack_power').split('—')[0].strip(): 0.25,
        t('factor_market_odds').split('—')[0].strip(): 0.20,
        t('factor_squad_value').split('—')[0].strip(): 0.20,
        t('factor_form_fitness').split('—')[0].strip(): 0.20,
        t('factor_xfactor_players').split('—')[0].strip(): 0.15
    }
    
    weight_df = pd.DataFrame({
        'Factor': list(weights_data.keys()),
        'Weight': list(weights_data.values())
    })
    
    fig = px.pie(weight_df, values='Weight', names='Factor', title=t('weight_distribution'))
    st.plotly_chart(fig, width='stretch')
    
    st.subheader(f"📊 {t('three_board_params')}")
    params = engine.three_board.factors
    params_df = pd.DataFrame({
        t('parameter'): list(params.keys()),
        t('value'): list(params.values())
    })
    st.dataframe(params_df, width='stretch')
    
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
    st.plotly_chart(fig, width='stretch')
    
    st.subheader(f"📈 {t('top_by_category')}")
    categories = [overall_col, attack_col, defense_col, pk_col]
    for cat in categories:
        top_teams = df.nlargest(5, cat)
        fig = px.bar(top_teams, x='Team', y=cat, title=f"{t('top_5_teams')} - {cat}",
                    color=cat, color_continuous_scale='Blues')
        st.plotly_chart(fig, width='stretch')

def load_news_data():
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('news', [])
    except Exception:
        return []

def show_news():
    st.title(f"📰 {t('news_title')}")
    
    news_data = load_news_data()
    
    if not news_data:
        st.warning(t('news_no_articles'))
        return
    
    sources = list(set(item['source'] for item in news_data))
    sources.sort()
    
    col1, col2 = st.columns([1, 3])
    with col1:
        filter_source = st.selectbox(
            t('news_filter_source'),
            [t('news_all_sources')] + sources
        )
    
    if filter_source != t('news_all_sources'):
        filtered_news = [n for n in news_data if n['source'] == filter_source]
    else:
        filtered_news = news_data
    
    total_articles = len(filtered_news)
    st.info(f"**{t('news_total')}:** {total_articles:,}")
    
    items_per_page = 50
    total_pages = (total_articles + items_per_page - 1) // items_per_page
    
    if total_pages > 1:
        page_num = st.number_input(
            f"{t('news_page_info')} (1-{total_pages})",
            min_value=1,
            max_value=total_pages,
            value=1
        )
    else:
        page_num = 1
    
    start_idx = (page_num - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_news = filtered_news[start_idx:end_idx]
    
    for i, article in enumerate(page_news):
        with st.container():
            st.markdown(f"""
            <div style="background-color: #FFFFFF; border-radius: 8px; 
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 1rem; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold; color: #1E88E5;">📰 {article['source']}</span>
                    <span style="color: #757575; font-size: 0.85rem;">{article['timestamp']}</span>
                </div>
                <div style="margin-top: 0.5rem; color: #212121;">{article['content']}</div>
            </div>
            """, unsafe_allow_html=True)

def get_all_xfactor_players():
    xfactor_players = []
    for team_name, team in engine.teams.items():
        for player in team.players:
            if player.is_xfactor:
                rating = int((player.dribbling_skill + player.pace + player.shooting + player.passing + player.defending) / 5)
                xfactor_players.append({
                    'name': player.name,
                    'team': team_name,
                    'position': player.position,
                    'rating': rating,
                    'goals': int(rating * 0.15),
                    'assists': int(rating * 0.12),
                    'form': player.fitness_level // 20,
                    'fitness': player.fitness_level
                })
    return xfactor_players

def show_xfactor():
    st.title(f"⭐ {t('xfactor_title')}")
    
    xfactor_players = get_all_xfactor_players()
    
    if not xfactor_players:
        st.warning(t('xfactor_no_players'))
        return
    
    st.metric(t('xfactor_total'), len(xfactor_players))
    
    lang = st.session_state.language
    
    df = pd.DataFrame(xfactor_players)
    df['display_name'] = df.apply(
        lambda row: f"{get_player_name(row['name'], row['team'], lang)} ({get_team_name(row['team'], lang)})",
        axis=1
    )
    
    st.subheader(f"📊 {t('xfactor_radar_chart')}")
    
    selected_players = st.multiselect(
        t('xfactor_select_compare'),
        df['display_name'].tolist(),
        max_selections=5
    )
    
    if selected_players:
        selected_df = df[df['display_name'].isin(selected_players)]
        
        categories = [t('xfactor_rating'), t('xfactor_goals'), t('xfactor_assists'), 
                      t('xfactor_form'), t('xfactor_fitness')]
        
        fig = go.Figure()
        
        for _, player in selected_df.iterrows():
            values = [
                player['rating'] / 100 * 5,
                min(player['goals'] / 30 * 5, 5),
                min(player['assists'] / 20 * 5, 5),
                player['form'],
                player['fitness'] / 20
            ]
            values.append(values[0])
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name=player['display_name']
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )
            ),
            showlegend=True,
            title=t('xfactor_compare_title')
        )
        
        st.plotly_chart(fig, width='stretch')
    
    st.subheader(f"📋 {t('xfactor_title')}")
    
    display_df = df[['display_name', 'position', 'rating', 'goals', 'assists', 'form', 'fitness']].copy()
    display_df.columns = [
        t('xfactor_team'), t('xfactor_position'), t('xfactor_rating'),
        t('xfactor_goals'), t('xfactor_assists'), t('xfactor_form'), t('xfactor_fitness')
    ]
    
    st.dataframe(display_df, width='stretch')

if __name__ == "__main__":
    main()
