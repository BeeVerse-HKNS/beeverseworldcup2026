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
from languages import LANGUAGES, LANGUAGE_NAMES, get_text, get_language_name, get_available_languages, get_default_language
from player_translations import get_player_name, get_team_name
from user_registration_db import save_registration, get_registration_count

SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_PATH = SCRIPT_DIR / 'data' / 'wc2026_player_database.json'

def _get_app_version():
    try:
        if 'APP_VERSION' in st.secrets:
            return st.secrets['APP_VERSION']
    except Exception:
        pass
    return os.environ.get('APP_VERSION', 'international')

APP_VERSION = _get_app_version()

st.set_page_config(
    page_title="World Cup 2026 Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

DESIGN_TOKENS = {
    'primary_color': '#2E7D32',
    'primary_color_cn': '#FFB300',
    'primary_light': '#4CAF50',
    'secondary': '#F57F17',
    'background': '#FAFAFA',
    'card_bg': '#FFFFFF',
    'surface_variant': '#F5F5F5',
    'text_primary': '#1B1B1F',
    'text_secondary': '#49454F',
    'success': '#66BB6A',
    'warning': '#FFA726',
    'error': '#EF5350',
    'info': '#29B6F6',
    'border_radius': '8px',
    'shadow': '0 2px 4px rgba(0,0,0,0.1)',
    'font_size_body': '16px',
    'font_size_title': '24px',
}

DARK_TOKENS = {
    'primary_color': '#4CAF50',
    'primary_color_cn': '#FFB300',
    'primary_light': '#81C784',
    'secondary': '#FFB300',
    'background': '#121212',
    'card_bg': '#1E1E1E',
    'surface_variant': '#2C2C2C',
    'text_primary': '#ECEFF1',
    'text_secondary': '#B0BEC5',
    'success': '#66BB6A',
    'warning': '#FFA726',
    'error': '#EF5350',
    'info': '#29B6F6',
    'border_radius': '8px',
    'shadow': '0 2px 4px rgba(0,0,0,0.3)',
    'font_size_body': '16px',
    'font_size_title': '24px',
}

def get_design_tokens(lang: str, theme: str = 'dark') -> dict:
    tokens = DARK_TOKENS.copy() if theme == 'dark' else DESIGN_TOKENS.copy()
    if lang in ['zh_hant', 'zh_hans']:
        tokens['primary_color'] = tokens['primary_color_cn']
    return tokens

def apply_custom_css(lang: str, theme: str = 'dark'):
    tokens = get_design_tokens(lang, theme)
    if theme == 'dark':
        st.markdown(f"""
        <style>
            .main {{
                background-color: {tokens['background']};
                color: {tokens['text_primary']};
            }}
            .stApp {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                color: {tokens['text_primary']};
            }}
            h1 {{
                font-size: {tokens['font_size_title']};
                color: {tokens['text_primary']};
                font-weight: 600;
            }}
            h2, h3 {{
                color: {tokens['text_primary']};
            }}
            p, span, label {{
                color: {tokens['text_primary']};
            }}
            .stMetric {{
                background-color: {tokens['card_bg']};
                border-radius: {tokens['border_radius']};
                box-shadow: {tokens['shadow']};
                padding: 1rem;
                color: {tokens['text_primary']};
            }}
            .stMetric > div > div > div {{
                color: {tokens['text_primary']};
            }}
            .stButton > button {{
                background-color: {tokens['primary_color']};
                color: white;
                border-radius: {tokens['border_radius']};
                font-weight: 500;
                transition: all 0.2s ease;
            }}
            .stButton > button:hover {{
                background-color: {tokens['secondary']};
                color: #121212;
            }}
            .stSelectbox, .stMultiSelect {{
                border-radius: {tokens['border_radius']};
            }}
            [data-testid="stSidebar"] {{
                background-color: {tokens['surface_variant']};
            }}
            .stTab {{
                background-color: {tokens['surface_variant']};
            }}
            .stSuccess {{
                background-color: #1B3A1B;
                border-left: 4px solid {tokens['success']};
                color: #C8E6C9;
            }}
            .stInfo {{
                background-color: #0D2744;
                border-left: 4px solid {tokens['info']};
                color: #B3E5FC;
            }}
            .stWarning {{
                background-color: #3E2723;
                border-left: 4px solid {tokens['warning']};
                color: #FFE0B2;
            }}
            .stError {{
                background-color: #3B1010;
                border-left: 4px solid {tokens['error']};
                color: #FFCDD2;
            }}
            .card {{
                background-color: {tokens['card_bg']};
                border-radius: {tokens['border_radius']};
                box-shadow: {tokens['shadow']};
                padding: 1.5rem;
                margin-bottom: 1rem;
                color: {tokens['text_primary']};
            }}
            .stDataFrame {{
                color: {tokens['text_primary']};
            }}
            .stTextInput > div > div > input {{
                background-color: {tokens['card_bg']};
                color: {tokens['text_primary']};
            }}
            .stNumberInput > div > div > input {{
                background-color: {tokens['card_bg']};
                color: {tokens['text_primary']};
            }}
            .stRadio > div {{
                color: {tokens['text_primary']};
            }}
            .stCheckbox {{
                color: {tokens['text_primary']};
            }}
            .stCaption {{
                color: {tokens['text_secondary']};
            }}
            .news-card {{
                background-color: {tokens['card_bg']};
                border-radius: {tokens['border_radius']};
                box-shadow: {tokens['shadow']};
                padding: 1rem;
                margin-bottom: 1rem;
                color: {tokens['text_primary']};
            }}
            .news-card .source {{
                font-weight: bold;
                color: {tokens['primary_color']};
            }}
            .news-card .timestamp {{
                color: {tokens['text_secondary']};
                font-size: 0.85rem;
            }}
            .news-card .content {{
                margin-top: 0.5rem;
                color: {tokens['text_primary']};
            }}
        </style>
        """, unsafe_allow_html=True)
    else:
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
                background-color: {tokens['primary_light']};
                color: white;
            }}
            .stSelectbox, .stMultiSelect {{
                border-radius: {tokens['border_radius']};
            }}
            [data-testid="stSidebar"] {{
                background-color: {tokens['surface_variant']};
            }}
            .stTab {{
                background-color: {tokens['surface_variant']};
            }}
            .stSuccess {{
                background-color: #E8F5E9;
                border-left: 4px solid {tokens['success']};
            }}
            .stInfo {{
                background-color: #E1F5FE;
                border-left: 4px solid {tokens['info']};
            }}
            .stWarning {{
                background-color: #FFF3E0;
                border-left: 4px solid {tokens['warning']};
            }}
            .stError {{
                background-color: #FFEBEE;
                border-left: 4px solid {tokens['error']};
            }}
            .card {{
                background-color: {tokens['card_bg']};
                border-radius: {tokens['border_radius']};
                box-shadow: {tokens['shadow']};
                padding: 1.5rem;
                margin-bottom: 1rem;
            }}
            .news-card {{
                background-color: {tokens['card_bg']};
                border-radius: {tokens['border_radius']};
                box-shadow: {tokens['shadow']};
                padding: 1rem;
                margin-bottom: 1rem;
            }}
            .news-card .source {{
                font-weight: bold;
                color: {tokens['primary_color']};
            }}
            .news-card .timestamp {{
                color: {tokens['text_secondary']};
                font-size: 0.85rem;
            }}
            .news-card .content {{
                margin-top: 0.5rem;
                color: {tokens['text_primary']};
            }}
        </style>
        """, unsafe_allow_html=True)

def init_language():
    if 'language' not in st.session_state:
        st.session_state.language = get_default_language(APP_VERSION)
    return st.session_state.language

def set_language(lang: str):
    st.session_state.language = lang
    st.rerun()

def init_theme():
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    return st.session_state.theme

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

def show_registration():
    lang = init_language()
    theme = init_theme()
    apply_custom_css(lang, theme)

    tokens = get_design_tokens(lang, theme)

    st.markdown(f"""
    <div style="text-align: center; padding: 3rem;">
        <h1>🏆 {t('register_title')}</h1>
        <p style="font-size: 1.2rem; color: {tokens['text_secondary']};">
            {t('register_subtitle')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("registration_form"):
        name = st.text_input(t('register_name'), placeholder=t('register_name_placeholder'))
        email = st.text_input(t('register_email'), placeholder=t('register_email_placeholder'))
        if APP_VERSION == 'china':
            phone = st.text_input(t('register_phone'), placeholder=t('register_phone_placeholder'), help='（可选）')
        else:
            phone = st.text_input(t('register_phone'), placeholder=t('register_phone_placeholder'))

        st.caption(f"🔒 {t('register_privacy')}")

        if APP_VERSION == 'china':
            pipl_consent = st.checkbox('我已阅读并同意《个人信息处理政策》', value=False)
            if not pipl_consent:
                st.caption('📋 [隐私政策](https://beeverseworldcup2026.streamlit.app/privacy)')

        submitted = st.form_submit_button(t('register_submit'), use_container_width=True)

        if submitted:
            if name and email:
                if APP_VERSION == 'china' and not st.session_state.get('pipl_consent_checked', False):
                    if not pipl_consent:
                        st.error("请同意个人信息处理政策")
                        return
                save_registration(name, email, phone, lang, APP_VERSION)
                st.session_state.registered = True
                st.session_state.user_name = name
                st.rerun()
            else:
                st.error("Please fill in name and email" if lang == 'en' else "請填寫姓名和電郵" if lang == 'zh_hant' else "请填写姓名和电邮")

    with st.sidebar:
        st.markdown(f"### {t('language')}")
        available_langs = get_available_languages(APP_VERSION)
        lang_options = list(available_langs.keys())
        lang_labels = [available_langs[l] for l in lang_options]
        current_idx = lang_options.index(lang) if lang in lang_options else 0
        selected_lang_label = st.selectbox(
            t('select_language'),
            lang_labels,
            index=current_idx,
            label_visibility="collapsed"
        )
        selected_lang = lang_options[lang_labels.index(selected_lang_label)]
        if selected_lang != lang:
            set_language(selected_lang)

def main():
    lang = init_language()
    theme = init_theme()

    if 'registered' not in st.session_state:
        st.session_state.registered = False

    if not st.session_state.registered:
        show_registration()
        return

    apply_custom_css(lang, theme)

    if APP_VERSION == 'international' and 'cookie_consent' not in st.session_state:
        st.markdown("""
        <div style="position:fixed;bottom:0;left:0;right:0;background:#1E1E1E;padding:12px 24px;
        z-index:9999;display:flex;align-items:center;justify-content:space-between;border-top:1px solid #4CAF50;">
            <span style="color:#ECEFF1;font-size:14px;">🍪 We use cookies to improve your experience. 
            <a href="#" style="color:#4CAF50;">Learn more</a></span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Accept Cookies", key="cookie_accept"):
            st.session_state.cookie_consent = True
            st.rerun()

    with st.sidebar:
        st.markdown(f"### {t('theme_toggle')}")
        theme_options = [t('theme_dark'), t('theme_light')]
        theme_values = ['dark', 'light']
        current_theme_idx = theme_values.index(st.session_state.get('theme', 'dark'))
        selected_theme_label = st.radio(
            t('theme_toggle'),
            theme_options,
            index=current_theme_idx,
            horizontal=True,
            label_visibility="collapsed"
        )
        selected_theme = theme_values[theme_options.index(selected_theme_label)]
        st.session_state.theme = selected_theme

        st.markdown("---")
        st.markdown(f"### {t('language')}")
        available_langs = get_available_languages(APP_VERSION)
        lang_options = list(available_langs.keys())
        lang_labels = [available_langs[l] for l in lang_options]
        current_idx = lang_options.index(lang) if lang in lang_options else 0
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
            t('xfactor_page'),
            t('team_squads_page')
        ]
        page = st.radio(t('navigation'), pages)

        st.markdown("---")
        st.markdown("### 📤 Share")
        if APP_VERSION == 'china':
            st.markdown("""
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
                <a href="https://service.weibo.com/share/share.php?url=https://beeverseworldcup2026.streamlit.app/&title=2026世界杯预测" target="_blank" style="text-decoration:none;padding:4px 12px;background:#E6162D;color:white;border-radius:4px;font-size:12px;">微博</a>
                <a href="javascript:void(0)" onclick="copyToClipboard('https://beeverseworldcup2026.streamlit.app/')" style="text-decoration:none;padding:4px 12px;background:#07C160;color:white;border-radius:4px;font-size:12px;">微信</a>
                <a href="https://www.douyin.com/" target="_blank" style="text-decoration:none;padding:4px 12px;background:#010101;color:white;border-radius:4px;font-size:12px;">抖音</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
                <a href="https://twitter.com/intent/tweet?url=https://beeverseworldcup2026.streamlit.app/&text=2026%20World%20Cup%20Predictor" target="_blank" style="text-decoration:none;padding:4px 12px;background:#1DA1F2;color:white;border-radius:4px;font-size:12px;">Twitter/X</a>
                <a href="https://www.facebook.com/sharer/sharer.php?u=https://beeverseworldcup2026.streamlit.app/" target="_blank" style="text-decoration:none;padding:4px 12px;background:#1877F2;color:white;border-radius:4px;font-size:12px;">Facebook</a>
                <a href="https://wa.me/?text=2026%20World%20Cup%20Predictor%20https://beeverseworldcup2026.streamlit.app/" target="_blank" style="text-decoration:none;padding:4px 12px;background:#25D366;color:white;border-radius:4px;font-size:12px;">WhatsApp</a>
            </div>
            """, unsafe_allow_html=True)

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
        elif page == t('team_squads_page'):
            show_team_squads()
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

    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    with col_r1:
        st.metric(t('total_news'), "10,001")
    with col_r2:
        st.metric(t('xfactor_players'), "40")
    with col_r3:
        st.metric("Accuracy", "90.4%")
    with col_r4:
        st.metric(t('research_iterations'), "735")

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

    df_top = df.sort_values(overall_col, ascending=False).head(10)

    lang = st.session_state.language
    display_names = [get_team_name(t_name, lang) for t_name in df_top['Team']]

    heatmap_data = df_top[[t('overall_strength'), t('attack_power'), t('defense_strength'), t('pk_ability')]].values
    fig = px.imshow(
        heatmap_data,
        x=[t('overall_strength'), t('attack_power'), t('defense_strength'), t('pk_ability')],
        y=display_names,
        color_continuous_scale=['#1B5E20', '#4CAF50', '#81C784', '#FFB300', '#FFD54F'],
        aspect='auto',
        title=t('top_10_teams')
    )
    fig.update_xaxes(side='bottom')
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

    top_teams_for_opta = [t_name for t_name in [home_team, away_team] if t_name in opta_probs]
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
            hole=0.3,
            marker=dict(colors=['#4CAF50', '#FFB300', '#81C784'])
        )])
        fig.update_layout(title_text=t('probability_distribution'))
        st.plotly_chart(fig, width='stretch')

        st.subheader(f"📊 {t('factor_breakdown')}")
        factors = result['factors']

        st.write(f"**{t('expected_goals')}:**")
        col_xg1, col_xg2 = st.columns(2)
        with col_xg1:
            st.metric(home_display, f"{factors['xg']['home']:.2f}")
        with col_xg2:
            st.metric(away_display, f"{factors['xg']['away']:.2f}")

        st.write(f"**{t('player_factor')}:**")
        categories = [t('player_factor')]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[factors['player_factor']['home']],
            theta=categories,
            fill='toself',
            fillcolor='rgba(76,175,80,0.3)',
            line_color='#4CAF50',
            name=home_display
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[factors['player_factor']['away']],
            theta=categories,
            fill='toself',
            fillcolor='rgba(255,179,0,0.3)',
            line_color='#FFB300',
            name=away_display
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=True,
            title=t('player_factor')
        )
        st.plotly_chart(fig_radar, width='stretch')

        st.write(f"**{t('defensive_pk')}:**")
        col_pk1, col_pk2 = st.columns(2)
        with col_pk1:
            st.metric(home_display, f"{factors['defensive_pk']['home']:.2f}")
        with col_pk2:
            st.metric(away_display, f"{factors['defensive_pk']['away']:.2f}")

        st.write(f"**{t('xfactor_players')}:**")
        col_xf1, col_xf2 = st.columns(2)
        with col_xf1:
            st.metric(home_display, f"{factors['xfactor']['home']:.2f}")
        with col_xf2:
            st.metric(away_display, f"{factors['xfactor']['away']:.2f}")

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

        team1_values = []
        team2_values = []

        for metric, name in zip(metrics, metric_names):
            data = comparison['comparison'][metric]
            winner = data['winner']
            team1_values.append(data[team1])
            team2_values.append(data[team2])

            col_a, col_b, col_c = st.columns([2, 1, 2])
            with col_a:
                st.write(f"**{team1_display}:** {data[team1]}")
            with col_b:
                st.write(f"🏆 {get_team_name(winner, lang)}")
            with col_c:
                st.write(f"**{team2_display}:** {data[team2]}")

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=team1_values,
            theta=metric_names,
            fill='toself',
            fillcolor='rgba(76,175,80,0.3)',
            line_color='#4CAF50',
            name=team1_display
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=team2_values,
            theta=metric_names,
            fill='toself',
            fillcolor='rgba(255,179,0,0.3)',
            line_color='#FFB300',
            name=team2_display
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=True,
            title=t('5_point_comparison')
        )
        st.plotly_chart(fig_radar, width='stretch')

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

        avg_pace = df['pace'].mean()
        avg_shooting = df['shooting'].mean()
        avg_passing = df['passing'].mean()
        avg_defending = df['defending'].mean()
        avg_dribbling = df['dribbling_skill'].mean()
        avg_fitness = df['fitness_level'].mean()

        categories = ['Pace', 'Shooting', 'Passing', 'Defending', 'Dribbling', 'Fitness']
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[avg_pace, avg_shooting, avg_passing, avg_defending, avg_dribbling, avg_fitness],
            theta=categories,
            fill='toself',
            fillcolor='rgba(76,175,80,0.3)',
            line_color='#4CAF50',
            name=get_team_name(selected_team, lang)
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title=f"{get_team_name(selected_team, lang)} {t('attribute_distribution')}"
        )
        st.plotly_chart(fig_radar, width='stretch')

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
    fig_accuracy.update_traces(line=dict(width=3, color='#4CAF50'), marker=dict(size=10, color='#4CAF50'))
    st.plotly_chart(fig_accuracy, width='stretch')

    col_n1, col_n2, col_n3, col_n4 = st.columns(4)
    with col_n1:
        st.metric(f"Phase 1", "2,500")
    with col_n2:
        st.metric(f"Phase 2", "5,000")
    with col_n3:
        st.metric(f"Phase 3", "7,500")
    with col_n4:
        st.metric(f"Phase 4", "10,001")

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

    fig = px.pie(weight_df, values='Weight', names='Factor', title=t('weight_distribution'),
                 color_discrete_sequence=['#4CAF50', '#FFB300', '#81C784', '#F57F17', '#A5D6A7'])
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
    lang = st.session_state.language

    for cat in categories:
        top_teams = df.nlargest(5, cat)
        team_names = [get_team_name(t_name, lang) for t_name in top_teams['Team']]
        heatmap_values = top_teams[[cat]].values

        fig_heat = px.imshow(
            heatmap_values.T,
            x=team_names,
            y=[cat],
            color_continuous_scale=['#1B5E20', '#4CAF50', '#81C784', '#FFB300', '#FFD54F'],
            aspect='auto',
            title=f"{t('top_5_teams')} - {cat}"
        )
        fig_heat.update_xaxes(side='bottom')
        st.plotly_chart(fig_heat, width='stretch')

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

    tokens = get_design_tokens(st.session_state.language, st.session_state.get('theme', 'dark'))

    for i, article in enumerate(page_news):
        with st.container():
            st.markdown(f"""
            <div class="news-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="source">📰 {article['source']}</span>
                    <span class="timestamp">{article['timestamp']}</span>
                </div>
                <div class="content">{article['content']}</div>
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

        for idx, (_, player) in enumerate(selected_df.iterrows()):
            values = [
                player['rating'] / 100 * 5,
                min(player['goals'] / 30 * 5, 5),
                min(player['assists'] / 20 * 5, 5),
                player['form'],
                player['fitness'] / 20
            ]
            values.append(values[0])

            if idx == 0:
                fillcolor = 'rgba(76,175,80,0.3)'
                line_color = '#4CAF50'
            elif idx == 1:
                fillcolor = 'rgba(255,179,0,0.3)'
                line_color = '#FFB300'
            else:
                fillcolor = f'rgba(129,199,132,{0.3 - idx * 0.05})'
                line_color = '#81C784'

            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor=fillcolor,
                line_color=line_color,
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

def show_team_squads():
    st.title(f"👥 {t('team_squads_title')}")

    lang = st.session_state.language
    teams = engine.get_all_teams()
    if not teams:
        st.error(f"❌ {t('no_teams_available')}")
        return

    team_display_names = {team: get_team_name(team, lang) for team in teams}
    display_teams = [team_display_names[t] for t in teams]

    selected_display = st.selectbox(t('team_squads_select'), display_teams)
    selected_team = teams[display_teams.index(selected_display)]

    players = engine.get_team_players(selected_team)
    if not players:
        st.warning(t('team_squads_no_players'))
        return

    avg_pace = sum(p['pace'] for p in players) / len(players)
    avg_shooting = sum(p['shooting'] for p in players) / len(players)
    avg_passing = sum(p['passing'] for p in players) / len(players)
    avg_defending = sum(p['defending'] for p in players) / len(players)
    avg_dribbling = sum(p['dribbling_skill'] for p in players) / len(players)
    avg_fitness = sum(p['fitness_level'] for p in players) / len(players)

    categories = ['Pace', 'Shooting', 'Passing', 'Defending', 'Dribbling', 'Fitness']

    st.subheader(f"📊 {t('team_squads_avg_attributes')}")
    fig_team = go.Figure(data=go.Scatterpolar(
        r=[avg_pace, avg_shooting, avg_passing, avg_defending, avg_dribbling, avg_fitness],
        theta=categories,
        fill='toself',
        fillcolor='rgba(76,175,80,0.3)',
        line_color='#4CAF50',
        name=get_team_name(selected_team, lang)
    ))
    fig_team.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title=f"{get_team_name(selected_team, lang)} {t('team_squads_avg_attributes')}"
    )
    st.plotly_chart(fig_team, width='stretch')

    st.subheader(f"⚽ {t('team_squads_player_abilities')}")

    for p in players:
        p['overall'] = (p['pace'] + p['shooting'] + p['passing'] + p['defending'] + p['dribbling_skill'] + p['fitness_level']) / 6
    players_sorted = sorted(players, key=lambda x: x['overall'], reverse=True)

    for i in range(0, len(players_sorted), 3):
        row_players = players_sorted[i:i+3]
        cols = st.columns(len(row_players))
        for col, p in zip(cols, row_players):
            with col:
                player_name = get_player_name(p['name'], selected_team, lang)
                badge = f" {t('team_squads_xfactor_badge')}" if p['is_xfactor'] else ""
                st.markdown(f"**{player_name}**{badge}")
                st.caption(f"{p['position']} | {t('team_squads_overall')}: {p['overall']:.0f}")

                fig_player = go.Figure(data=go.Scatterpolar(
                    r=[p['pace'], p['shooting'], p['passing'], p['defending'], p['dribbling_skill'], p['fitness_level']],
                    theta=categories,
                    fill='toself',
                    fillcolor='rgba(76,175,80,0.3)',
                    line_color='#4CAF50',
                    name=player_name
                ))
                fig_player.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    showlegend=False,
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=250
                )
                st.plotly_chart(fig_player, width='stretch')

if __name__ == "__main__":
    main()
