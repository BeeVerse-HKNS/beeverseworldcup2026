import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from pathlib import Path
from datetime import datetime
from formula_v9_ultimate import FormulaV9
from odds_data_layer import OddsIntegratedPredictor
from tournament_model import TournamentModel

try:
    from formula_v11_emoglyph import FormulaV11Engine
    _V11_AVAILABLE = True
except ImportError:
    _V11_AVAILABLE = False

try:
    from wc2026_team_path_generator import TeamPathGenerator
    _PATH_GEN_AVAILABLE = True
except ImportError:
    _PATH_GEN_AVAILABLE = False

try:
    from wc2026_social_media_generator import SocialMediaGenerator
    _SOCIAL_GEN_AVAILABLE = True
except ImportError:
    _SOCIAL_GEN_AVAILABLE = False
from languages import LANGUAGES, LANGUAGE_NAMES, get_text, get_language_name, get_available_languages, get_default_language
from player_translations import get_player_name, get_team_name
from user_registration_db import save_registration, get_registration_count

try:
    from compliance_language_map import compliant_text, check_compliance
    from jurisdiction_detector import JurisdictionDetector
    from disclaimer_engine import DisclaimerEngine
    from revenue_models import RevenueManager
    _COMPLIANCE_AVAILABLE = True
except ImportError:
    _COMPLIANCE_AVAILABLE = False

SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_PATH = SCRIPT_DIR / 'data' / 'wc2026_player_database.json'

def _get_app_version():
    try:
        from version_config import APP_VERSION as vc_version
        return vc_version
    except ImportError:
        pass
    try:
        if 'APP_VERSION' in st.secrets:
            return st.secrets['APP_VERSION']
    except Exception:
        pass
    return os.environ.get('APP_VERSION', 'international')

APP_VERSION = _get_app_version()

if _COMPLIANCE_AVAILABLE:
    jurisdiction_detector = JurisdictionDetector()
    disclaimer_engine = DisclaimerEngine()
    revenue_manager = RevenueManager()
else:
    jurisdiction_detector = None
    disclaimer_engine = None
    revenue_manager = None

COUNTRY_CODES = [
    ('+1', '🇺🇸 USA/Canada'),
    ('+44', '🇬🇧 UK'),
    ('+852', '🇭🇰 Hong Kong'),
    ('+86', '🇨🇳 中国'),
    ('+886', '🇹🇼 台灣'),
    ('+81', '🇯🇵 Japan'),
    ('+82', '🇰🇷 South Korea'),
    ('+65', '🇸🇬 Singapore'),
    ('+60', '🇲🇾 Malaysia'),
    ('+61', '🇦🇺 Australia'),
    ('+49', '🇩🇪 Germany'),
    ('+33', '🇫🇷 France'),
    ('+34', '🇪🇸 Spain'),
    ('+39', '🇮🇹 Italy'),
    ('+31', '🇳🇱 Netherlands'),
    ('+46', '🇸🇪 Sweden'),
    ('+47', '🇳🇴 Norway'),
    ('+351', '🇵🇹 Portugal'),
    ('+55', '🇧🇷 Brazil'),
    ('+52', '🇲🇽 Mexico'),
    ('+54', '🇦🇷 Argentina'),
    ('+56', '🇨🇱 Chile'),
    ('+57', '🇨🇴 Colombia'),
    ('+91', '🇮🇳 India'),
    ('+92', '🇵🇰 Pakistan'),
    ('+62', '🇮🇩 Indonesia'),
    ('+66', '🇹🇭 Thailand'),
    ('+84', '🇻🇳 Vietnam'),
    ('+63', '🇵🇭 Philippines'),
    ('+234', '🇳🇬 Nigeria'),
    ('+27', '🇿🇦 South Africa'),
    ('+971', '🇦🇪 UAE'),
    ('+966', '🇸🇦 Saudi Arabia'),
    ('+965', '🇰🇼 Kuwait'),
    ('+20', '🇪🇬 Egypt'),
]

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

def premium_badge():
    return st.markdown('<span style="background:linear-gradient(135deg,#FFD700,#FFA000);color:#000;padding:2px 8px;border-radius:4px;font-size:0.75em;font-weight:bold;">⭐ PREMIUM</span>', unsafe_allow_html=True)

def premium_gate(feature_name: str):
    is_cn = APP_VERSION == 'china'
    if revenue_manager:
        jurisdiction = st.session_state.get('user_jurisdiction', 'other')
        tiers = revenue_manager.get_pricing_tiers(jurisdiction)
        st.markdown(f"""
        <div style="border:2px dashed #FFB300;border-radius:8px;padding:1.5rem;text-align:center;background:rgba(255,179,0,0.05);">
            <p style="font-size:1.2rem;margin:0;">⭐ {feature_name}</p>
            <p style="color:#FFB300;margin:0.5rem 0 0 0;">{'升級至 Premium 解鎖' if is_cn else 'Upgrade to unlock'}</p>
        </div>
        """, unsafe_allow_html=True)
        tier_cols = st.columns(len(tiers))
        for col, tier in zip(tier_cols, tiers):
            with col:
                st.markdown(f"**{tier['name']}** — {tier['price']}")
                if tier.get('stripe_link'):
                    st.link_button(
                        '🛒 ' + ('訂閱' if is_cn else 'Subscribe'),
                        tier['stripe_link'],
                    )
    else:
        st.markdown(f"""
        <div style="border:2px dashed #FFB300;border-radius:8px;padding:1.5rem;text-align:center;background:rgba(255,179,0,0.05);">
            <p style="font-size:1.2rem;margin:0;">⭐ {feature_name}</p>
            <p style="color:#FFB300;margin:0.5rem 0 0 0;">{'升級至 Premium 解鎖' if is_cn else 'Upgrade to Premium to unlock'}</p>
        </div>
        """, unsafe_allow_html=True)

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

@st.cache_resource
def load_odds_predictor():
    return OddsIntegratedPredictor(alpha=0.6)

odds_predictor = load_odds_predictor()

@st.cache_resource
def load_v11_engine():
    if not _V11_AVAILABLE:
        return None
    try:
        return FormulaV11Engine()
    except Exception:
        return None

v11_engine = load_v11_engine()

def t(key: str) -> str:
    return get_text(key, st.session_state.language)

def show_disclaimers():
    if not disclaimer_engine:
        return
    jurisdiction = st.session_state.get('user_jurisdiction', 'other')
    disclaimers = disclaimer_engine.get_all_disclaimers(jurisdiction, APP_VERSION)
    for d in disclaimers:
        label_map = {
            'prediction': '⚠️ Prediction Disclaimer',
            'anti_gambling': '🚫 Anti-Gambling Notice',
            'data_privacy': '🔒 Data Privacy',
            'ai_transparency': '🤖 AI Transparency',
        }
        label = label_map.get(d['type'], d['type'].replace('_', ' ').title())
        with st.sidebar.expander(label):
            st.caption(d['text'])

def show_affiliate_section():
    tokens = get_design_tokens(st.session_state.language, init_theme())
    is_cn = APP_VERSION == 'china'

    if revenue_manager:
        jurisdiction = st.session_state.get('user_jurisdiction', 'other')
        products = revenue_manager.get_compliant_affiliate_products(jurisdiction)
    else:
        if is_cn:
            products = [
                {"name": "⚽ 世界盃正版球衣", "url": "https://s.click.taobao.com/wc2026_jersey", "description": "官方授權球衣，支持你嘅球隊"},
                {"name": "🎫 世界盃門票", "url": "https://s.click.taobao.com/wc2026_tickets", "description": "2026 美加墨世界盃現場門票"},
                {"name": "✈️ 世界盃旅行套餐", "url": "https://s.click.taobao.com/wc2026_travel", "description": "機票+酒店+門票一站式服務"},
            ]
        else:
            products = [
                {"name": "⚽ Official WC Jersey", "url": "https://www.fifa.com/fifaplus/en/tournaments/mens/worldcup/canadamexicousa2026/shop/jerseys", "description": "Official licensed jerseys"},
                {"name": "🎫 Match Tickets", "url": "https://www.fifa.com/fifaplus/en/tournaments/mens/worldcup/canadamexicousa2026/tickets", "description": "FIFA World Cup 2026 tickets"},
                {"name": "✈️ Travel Packages", "url": "https://www.booking.com/searchresults.html?ss=world+cup+2026", "description": "Flight + Hotel + Ticket bundles"},
            ]

    st.markdown(f"### 🛒 {'世界盃周邊推薦' if is_cn else 'World Cup Shop'}")
    cols = st.columns(len(products))
    for col, product in zip(cols, products):
        with col:
            name = product.get('name', '')
            url = product.get('url', '')
            desc = product.get('description', '')
            st.markdown(f"""
            <div style="background:{tokens['card_bg']};border-radius:8px;padding:1rem;text-align:center;border:1px solid {tokens.get('surface_variant', '#333')};">
                <h4>{name}</h4>
                <p style="font-size:0.85rem;color:{tokens['text_secondary']};">{desc}</p>
                <a href="{url}" target="_blank" style="background:{tokens['primary_color']};color:white;padding:8px 16px;border-radius:4px;text-decoration:none;display:inline-block;">{'查看詳情' if is_cn else 'Shop Now'}</a>
            </div>
            """, unsafe_allow_html=True)

def show_business_solutions():
    lang = init_language()
    theme = init_theme()
    apply_custom_css(lang, theme)
    tokens = get_design_tokens(lang, theme)
    jurisdiction = st.session_state.get('user_jurisdiction', 'other')

    is_cn = APP_VERSION == 'china'

    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <h1>💼 {'商業方案' if is_cn else 'Business Solutions'}</h1>
        <p style="color:{tokens['text_secondary']};">{'為你嘅業務提供專業解決方案' if is_cn else 'Professional solutions for your business'}</p>
    </div>
    """, unsafe_allow_html=True)

    if not revenue_manager:
        st.warning('⚠️ Revenue module not available' if not is_cn else '⚠️ 收入模組不可用')
        return

    tiers = revenue_manager.get_pricing_tiers(jurisdiction)

    st.subheader('💰 ' + ('定價方案' if is_cn else 'Pricing Plans'))
    tier_cols = st.columns(len(tiers))
    for col, tier in zip(tier_cols, tiers):
        with col:
            is_popular = tier['id'] == 'pro'
            border = f"2px solid {tokens['primary_color']}" if is_popular else f"1px solid {tokens.get('surface_variant', '#333')}"
            badge = '<span style="background:#FFB300;color:#000;padding:2px 8px;border-radius:4px;font-size:0.7em;font-weight:bold;">POPULAR</span>' if is_popular else ''
            st.markdown(f"""
            <div style="background:{tokens['card_bg']};border-radius:8px;padding:1.5rem;text-align:center;border:{border};">
                {badge}
                <h3>{tier['name']}</h3>
                <p style="font-size:1.5rem;font-weight:bold;color:{tokens['primary_color']};">{tier['price']}</p>
                <p style="font-size:0.8rem;color:{tokens['text_secondary']};">{tier['period']}</p>
            </div>
            """, unsafe_allow_html=True)
            for feature in tier['features']:
                st.markdown(f"- {feature}")
            if tier.get('stripe_link'):
                st.link_button(
                    '🛒 ' + ('訂閱' if is_cn else 'Subscribe'),
                    tier['stripe_link'],
                    use_container_width=True,
                )

    st.divider()

    st.subheader('📊 ' + ('功能比較' if is_cn else 'Feature Comparison'))
    comparison = revenue_manager.get_feature_comparison()
    comp_df = pd.DataFrame(comparison)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader('🛒 ' + ('推薦產品' if is_cn else 'Recommended Products'))
    products = revenue_manager.get_compliant_affiliate_products(jurisdiction)
    prod_cols = st.columns(len(products))
    for col, product in zip(prod_cols, products):
        with col:
            st.markdown(f"""
            <div style="background:{tokens['card_bg']};border-radius:8px;padding:1rem;text-align:center;border:1px solid {tokens.get('surface_variant', '#333')};">
                <h4>{product['name']}</h4>
                <p style="font-size:0.85rem;color:{tokens['text_secondary']};">{product['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.link_button(
                '🛍️ ' + ('查看' if is_cn else 'Shop Now'),
                product['url'],
                use_container_width=True,
            )

    st.divider()

    st.subheader('🏢 ' + ('企業合作' if is_cn else 'B2B Contact'))
    with st.form("b2b_contact"):
        company_name = st.text_input('🏢 ' + ('公司名稱' if is_cn else 'Company Name'))
        contact_email = st.text_input('📧 ' + ('聯絡電郵' if is_cn else 'Contact Email'))
        use_case = st.text_area('📝 ' + ('使用場景' if is_cn else 'Use Case'))
        if st.form_submit_button('📤 ' + ('提交' if is_cn else 'Submit'), use_container_width=True):
            if company_name and contact_email:
                st.success('✅ ' + ('已收到你嘅查詢，我哋會盡快聯絡你。' if is_cn else 'Thank you! We will contact you shortly.'))
            else:
                st.error('❌ ' + ('請填寫公司名稱和電郵' if is_cn else 'Please fill in company name and email'))

    st.divider()

    api_url = revenue_manager.get_api_docs_url()
    st.subheader('🔧 API ' + ('文檔' if is_cn else 'Documentation'))
    st.markdown(f"📖 [{'API 文檔' if is_cn else 'API Documentation'}]({api_url})")

def show_monetization_guide():
    lang = init_language()
    theme = init_theme()
    apply_custom_css(lang, theme)
    tokens = get_design_tokens(lang, theme)

    if APP_VERSION == 'china':
        sections = {
            "💰 Freemium 變現策略": [
                "**基本策略**：免費提供基本預測（勝/平/負概率），付費解鎖高級分析",
                "**定價建議**：月費 ¥29-49，年費 ¥199-299",
                "**Premium 內容**：詳細因素拆解、歷史對比、統計概率分析、實時推送",
                "**轉化關鍵**：讓免費用戶體驗到價值，再引導付費",
            ],
            "🛒 Affiliate Marketing 收入": [
                "**球衣/周邊**：淘寶聯盟、京東聯盟，佣金 3-10%",
                "**門票**：官方授權渠道，佣金 5-15%",
                "**旅行套餐**：攜程/飛豬聯盟，佣金 3-8%",
                "**關鍵**：選擇合規數據分析產品，避免法律風險",
            ],
            "📱 社交媒體引流": [
                "**抖音**：世界盃預測短視頻 → 引流到 App → 轉化為註冊用戶",
                "**B站**：5因素模型深度分析視頻 → 建立專業形象 → Premium 轉化",
                "**小紅書**：世界盃攻略筆記 → 種草周邊產品 → Affiliate 收入",
                "**微信公眾號**：每日預測文章 → 付費深度分析 → 知識付費",
            ],
            "📊 數據驅動優化": [
                "**追蹤指標**：註冊轉化率、Premium 轉化率、Affiliate 點擊率",
                "**A/B 測試**：測試不同定價、不同 Premium 內容、不同 Affiliate 產品",
                "**用戶分層**：免費用戶 → 活躍用戶 → 付費用戶 → 超級用戶",
                "**持續迭代**：基於數據優化產品，而非憑感覺",
            ],
        }
    else:
        sections = {
            "💰 Freemium Strategy": [
                "**Basic**: Free predictions (Win/Draw/Lose probability)",
                "**Pricing**: Monthly $4.99-9.99, Annual $39.99-59.99",
                "**Premium Content**: Detailed factor breakdown, historical comparison, statistical probability analysis, real-time alerts",
                "**Conversion Key**: Let free users experience value first, then guide to paid",
            ],
            "🛒 Affiliate Marketing Revenue": [
                "**Jerseys/Merch**: Amazon Associates, FIFA Shop, 3-8% commission",
                "**Tickets**: Official FIFA channels, 5-15% commission",
                "**Travel**: Booking.com, Expedia affiliates, 3-8% commission",
                "**Key**: Choose compliant data analysis products to avoid legal risks",
            ],
            "📱 Social Media Traffic": [
                "**TikTok/IG Reels**: WC prediction shorts → Drive to App → Convert to registered users",
                "**YouTube**: 5-Factor Model deep analysis → Build authority → Premium conversion",
                "**Twitter/X**: Real-time match predictions → Build following → Affiliate revenue",
                "**Blog/Newsletter**: Daily prediction articles → Premium analysis → Knowledge commerce",
            ],
            "📊 Data-Driven Optimization": [
                "**Track Metrics**: Registration rate, Premium conversion rate, Affiliate click-through rate",
                "**A/B Testing**: Test different pricing, Premium content, Affiliate products",
                "**User Segmentation**: Free → Active → Paid → Super users",
                "**Continuous Iteration**: Optimize based on data, not gut feeling",
            ],
        }

    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <h1>📚 {'變現教學指南' if APP_VERSION == 'china' else 'Monetization Guide'}</h1>
        <p style="color:{tokens['text_secondary']};">{'如何從世界盃預測 App 賺錢' if APP_VERSION == 'china' else 'How to earn money from your WC2026 Predictor'}</p>
    </div>
    """, unsafe_allow_html=True)

    for title, items in sections.items():
        st.markdown(f"### {title}")
        for item in items:
            st.markdown(f"- {item}")
        st.divider()

def show_engagement_gate():
    """Engagement gate: Like + Share + Subscribe to enter (replaces registration)"""
    lang = init_language()
    theme = init_theme()
    apply_custom_css(lang, theme)
    tokens = get_design_tokens(lang, theme)
    is_cn = APP_VERSION == 'china'

    # Initialize session state
    for key in ['engagement_like', 'engagement_share', 'engagement_subscribe']:
        if key not in st.session_state:
            st.session_state[key] = False

    # Title
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 1rem;">
        <h1>🏆 World Cup 2026 AI Predictor</h1>
        <p style="font-size: 1.3rem; color: {tokens['text_secondary']};">
            {'免费使用 — 只需支持我们！' if is_cn else 'Free access — just support us!'}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Share text
    share_url = "https://beeverse-wc2026-international.streamlit.app/"
    share_text_en = "🏆 Check out this AI World Cup 2026 Predictor! 17 factors, 5000+ simulations, every team's path analyzed. Free to use! 🔮⚽ #WorldCup2026 #AIPrediction"
    share_text_cn = "🏆 2026世界杯AI预测器！17个因素、5000+次模拟、每支球队路径分析。免费使用！🔮⚽ #世界杯2026 #AI预测"
    share_text_tw = "🏆 2026世界盃AI預測器！17個因素、5000+次模擬、每支球隊路徑分析。免費使用！🔮⚽ #世界盃2026 #AI預測"
    share_text = share_text_cn if is_cn else share_text_en
    from urllib.parse import quote
    encoded_share = quote(share_text)

    # Step 1: Like
    st.markdown("### 👍 " + ("第一步：点赞" if is_cn else "Step 1: Like us"))
    like_cols = st.columns(4 if not is_cn else 3)
    like_platforms = [
        ("Twitter/X", f"https://twitter.com/intent/like?tweet_id=placeholder"),
        ("Facebook", f"https://www.facebook.com/"),
        ("Weibo", f"https://weibo.com/"),
        ("Douyin", f"https://www.douyin.com/"),
    ] if not is_cn else [
        ("微博 Weibo", f"https://weibo.com/"),
        ("抖音 Douyin", f"https://www.douyin.com/"),
        ("微信 WeChat", f"https://weixin.qq.com/"),
    ]
    for i, (name, url) in enumerate(like_platforms):
        with like_cols[i]:
            if st.button(f"👍 {name}", key=f"like_{name}"):
                st.session_state.engagement_like = True
                st.rerun()

    if st.session_state.engagement_like:
        st.markdown(f'<p style="color: #4CAF50; font-weight: bold;">✅ {"已点赞！" if is_cn else "Liked!"}</p>', unsafe_allow_html=True)

    st.divider()

    # Step 2: Share
    st.markdown("### 📤 " + ("第二步：分享" if is_cn else "Step 2: Share with friends"))
    share_cols = st.columns(4 if not is_cn else 3)
    share_platforms = [
        ("Twitter/X", f"https://twitter.com/intent/tweet?text={encoded_share}&url={share_url}"),
        ("Facebook", f"https://www.facebook.com/sharer/sharer.php?u={share_url}"),
        ("WhatsApp", f"https://wa.me/?text={encoded_share}%20{share_url}"),
        ("WeChat", None),  # WeChat needs copy link
    ] if not is_cn else [
        ("微博 Weibo", f"https://service.weibo.com/share/share.php?title={encoded_share}&url={share_url}"),
        ("微信 WeChat", None),
        ("抖音 Douyin", None),
    ]
    for i, (name, url) in enumerate(share_platforms):
        with share_cols[i]:
            if url:
                st.markdown(f'<a href="{url}" target="_blank" rel="noopener noreferrer" style="text-decoration:none;"><button style="background:{tokens["primary_color"]};color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;font-size:14px;width:100%;">📤 {name}</button></a>', unsafe_allow_html=True)
            else:
                # Copy link for WeChat
                st.markdown(f'<button onclick="navigator.clipboard.writeText(\'{share_text} {share_url}\');this.textContent=\'✅ Copied!\'" style="background:{tokens["primary_color"]};color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;font-size:14px;width:100%;">📤 {name}</button>', unsafe_allow_html=True)
            if st.button(f"✓ {name}", key=f"share_{name}"):
                st.session_state.engagement_share = True
                st.rerun()

    if st.session_state.engagement_share:
        st.markdown(f'<p style="color: #4CAF50; font-weight: bold;">✅ {"已分享！" if is_cn else "Shared!"}</p>', unsafe_allow_html=True)

    st.divider()

    # Step 3: Subscribe
    st.markdown("### 🔔 " + ("第三步：关注" if is_cn else "Step 3: Subscribe/Follow"))
    sub_cols = st.columns(4 if not is_cn else 3)
    sub_platforms = [
        ("Twitter/X", "https://twitter.com/"),
        ("YouTube", "https://www.youtube.com/"),
        ("Facebook", "https://www.facebook.com/"),
        ("Instagram", "https://www.instagram.com/"),
    ] if not is_cn else [
        ("微博 Weibo", "https://weibo.com/"),
        ("抖音 Douyin", "https://www.douyin.com/"),
        ("微信 WeChat", "https://weixin.qq.com/"),
    ]
    for i, (name, url) in enumerate(sub_platforms):
        with sub_cols[i]:
            if st.button(f"🔔 {name}", key=f"sub_{name}"):
                st.session_state.engagement_subscribe = True
                st.rerun()

    if st.session_state.engagement_subscribe:
        st.markdown(f'<p style="color: #4CAF50; font-weight: bold;">✅ {"已关注！" if is_cn else "Subscribed!"}</p>', unsafe_allow_html=True)

    st.divider()

    # Enter button
    all_done = st.session_state.engagement_like and st.session_state.engagement_share and st.session_state.engagement_subscribe

    if all_done:
        if st.button("✅ " + ("进入应用" if is_cn else "Enter the App"), type="primary", use_container_width=True, key="enter_app"):
            st.session_state.registered = True
            st.rerun()
    else:
        remaining = []
        if not st.session_state.engagement_like:
            remaining.append("👍 " + ("点赞" if is_cn else "Like"))
        if not st.session_state.engagement_share:
            remaining.append("📤 " + ("分享" if is_cn else "Share"))
        if not st.session_state.engagement_subscribe:
            remaining.append("🔔 " + ("关注" if is_cn else "Subscribe"))
        st.info("📌 " + ("请完成以下步骤：" if is_cn else "Please complete: ") + " | ".join(remaining))
        st.button("✅ " + ("进入应用" if is_cn else "Enter the App"), disabled=True, use_container_width=True, key="enter_app_disabled")

    # Language selector in sidebar
    with st.sidebar:
        st.markdown(f"### {t('language') if 't' in dir() else 'Language'}")
        available_langs = get_available_languages(APP_VERSION)
        lang_options = list(available_langs.keys())
        lang_labels = [available_langs[l] for l in lang_options]
        current_idx = lang_options.index(lang) if lang in lang_options else 0
        selected_lang_label = st.selectbox(
            "Language",
            lang_labels,
            index=current_idx,
            label_visibility="collapsed"
        )
        selected_lang = lang_options[lang_labels.index(selected_lang_label)]
        if selected_lang != lang:
            set_language(selected_lang)

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
        phone_col1, phone_col2 = st.columns([1, 2])
        with phone_col1:
            default_code_idx = 3 if APP_VERSION == 'china' else 0
            country_code = st.selectbox(
                'Country Code',
                options=[c[0] for c in COUNTRY_CODES],
                format_func=lambda x: next(f'{c[0]} {c[1]}' for c in COUNTRY_CODES if c[0] == x),
                index=default_code_idx,
                label_visibility='collapsed'
            )
            if jurisdiction_detector:
                user_jurisdiction = jurisdiction_detector.detect_from_phone(country_code)
                st.session_state.user_jurisdiction = user_jurisdiction
        with phone_col2:
            if APP_VERSION == 'china':
                phone_number = st.text_input(t('register_phone'), placeholder=t('register_phone_placeholder'), help='（可选）')
            else:
                phone_number = st.text_input(t('register_phone'), placeholder=t('register_phone_placeholder'))

        st.caption(f"🔒 {t('register_privacy')}")

        if APP_VERSION == 'china':
            pipl_consent = st.checkbox('我已阅读并同意《个人信息处理政策》', value=False)
            if not pipl_consent:
                st.caption('📋 [隐私政策](https://beeverseworldcup2026.streamlit.app/privacy)')

        submitted = st.form_submit_button(t('register_submit'), use_container_width=True)

        if submitted:
            if phone_number and not phone_number.replace(' ', '').replace('-', '').isdigit():
                st.error("Phone number should contain only digits" if lang == 'en' else "電話號碼只能包含數字" if lang == 'zh_hant' else "电话号码只能包含数字")
                return
            phone = f'{country_code} {phone_number}' if phone_number else ''
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

def show_admin_page():
    lang = init_language()
    theme = init_theme()
    apply_custom_css(lang, theme)
    tokens = get_design_tokens(lang, theme)

    if 'admin_authed' not in st.session_state:
        st.session_state.admin_authed = False

    if not st.session_state.admin_authed:
        admin_pw = st.secrets.get('ADMIN_PASSWORD', 'beeverse2026') if hasattr(st, 'secrets') else 'beeverse2026'
        pw = st.text_input('🔒 Admin Password', type='password')
        if st.button('Login'):
            if pw == admin_pw:
                st.session_state.admin_authed = True
                st.rerun()
            else:
                st.error('Wrong password')
        return

    from user_registration_db import get_all_registrations, get_registration_stats
    import io

    stats = get_registration_stats()

    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <h1>🔐 Admin Panel</h1>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Registrations", stats['total'])
    with col2:
        st.metric("🇨🇳 China Version", stats['china'])
    with col3:
        st.metric("🌍 International Version", stats['international'])
    with col4:
        st.metric("📅 Today", stats['today'])

    st.divider()

    rows = get_all_registrations()
    if rows:
        df = pd.DataFrame(rows, columns=['ID', 'Name', 'Email', 'Phone', 'Language', 'Version', 'Registered At'])
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        st.download_button(
            label="📥 Export CSV",
            data=csv_data,
            file_name=f"registrations_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No registrations yet")

    if st.button("🚪 Logout"):
        st.session_state.admin_authed = False
        st.rerun()

def main():
    if st.session_state.get('show_admin', False):
        show_admin_page()
        return

    lang = init_language()
    theme = init_theme()

    if 'registered' not in st.session_state:
        st.session_state.registered = False

    if 'is_premium' not in st.session_state:
        st.session_state.is_premium = False

    if 'user_jurisdiction' not in st.session_state:
        st.session_state.user_jurisdiction = 'other'

    if not st.session_state.registered:
        show_engagement_gate()
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
            t('team_squads_page'),
            '🌡️ ' + ('極端環境分析' if APP_VERSION == 'china' else 'Extreme Environment'),
            '🗺️ ' + ('球隊路徑策略' if APP_VERSION == 'china' else 'Team Path Strategy'),
            '📚 ' + ('變現指南' if APP_VERSION == 'china' else 'Monetization Guide'),
            '💼 ' + ('商業方案' if APP_VERSION == 'china' else 'Business Solutions')
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

        st.markdown("---")
        show_affiliate_section()

        st.divider()
        show_disclaimers()

        if disclaimer_engine:
            jurisdiction = st.session_state.get('user_jurisdiction', 'other')
            anti_gambling = disclaimer_engine.get_anti_gambling_notice(jurisdiction)
            if anti_gambling:
                st.sidebar.markdown(f"""
                <div style="background:#3B1010;border:1px solid #EF5350;border-radius:8px;padding:0.75rem;margin-top:0.5rem;">
                    <p style="color:#FFCDD2;font-size:0.8rem;margin:0;">🚫 {anti_gambling}</p>
                </div>
                """, unsafe_allow_html=True)

        st.divider()
        if st.button("🔒", key="admin_lock"):
            st.session_state.show_admin = not st.session_state.get('show_admin', False)

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
        elif page == '🌡️ ' + ('極端環境分析' if APP_VERSION == 'china' else 'Extreme Environment'):
            show_extreme_environment()
        elif page == '🗺️ ' + ('球隊路徑策略' if APP_VERSION == 'china' else 'Team Path Strategy'):
            show_team_path_strategy()
        elif page == '📚 ' + ('變現指南' if APP_VERSION == 'china' else 'Monetization Guide'):
            show_monetization_guide()
        elif page == '💼 ' + ('商業方案' if APP_VERSION == 'china' else 'Business Solutions'):
            show_business_solutions()
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

    use_odds = st.toggle("Odds Integration", value=True, help="Blend model prediction with market odds: P_final = 0.6 × P_odds + 0.4 × P_model")
    if use_odds:
        alpha_val = st.slider("Odds Weight (α)", min_value=0.0, max_value=1.0, value=0.6, step=0.05, help="α=1.0 = pure odds, α=0.0 = pure model")
        odds_predictor.alpha = alpha_val

    if st.button(t('predict_match'), width='stretch'):
        result = engine.predict_match(home_team, away_team, home_odds, draw_odds, away_odds)

        if not result['success']:
            st.error(result.get('error', t('prediction_failed')))
            return

        model_probs = (
            result['home_win_probability'],
            result['draw_probability'],
            result['away_win_probability'],
        )

        if use_odds:
            blended = odds_predictor.predict(home_team, away_team, model_probs)
            display_home = blended.final_home
            display_draw = blended.final_draw
            display_away = blended.final_away
            display_result = blended.predicted_result
            st.success(f"**{t('predicted_result')}:** {display_result} (Odds-Enhanced)")
        else:
            display_home = model_probs[0]
            display_draw = model_probs[1]
            display_away = model_probs[2]
            display_result = result['predicted_result']
            st.success(f"**{t('predicted_result')}:** {display_result}")

        st.info(f"**{t('confidence_level')}:** {result['confidence']}%")

        if disclaimer_engine:
            jurisdiction = st.session_state.get('user_jurisdiction', 'other')
            pred_disclaimer = disclaimer_engine.get_prediction_disclaimer(jurisdiction)
            if pred_disclaimer:
                st.warning(f"⚠️ {pred_disclaimer}")

        st.metric(t('model_confidence'), "90.4%")
        st.caption(t('based_on_iterations').format(735))

        home_display = get_team_name(home_team, lang)
        away_display = get_team_name(away_team, lang)

        if use_odds:
            st.subheader("📊 Probability Comparison")
            comp_col1, comp_col2 = st.columns(2)
            with comp_col1:
                st.markdown("**Model Only**")
                m_col1, m_col2, m_col3 = st.columns(3)
                with m_col1:
                    st.metric(f"{home_display}", f"{model_probs[0]:.2%}")
                with m_col2:
                    st.metric("Draw", f"{model_probs[1]:.2%}")
                with m_col3:
                    st.metric(f"{away_display}", f"{model_probs[2]:.2%}")
            with comp_col2:
                st.markdown(f"**Blended (α={odds_predictor.alpha:.2f})**")
                b_col1, b_col2, b_col3 = st.columns(3)
                with b_col1:
                    st.metric(f"{home_display}", f"{display_home:.2%}")
                with b_col2:
                    st.metric("Draw", f"{display_draw:.2%}")
                with b_col3:
                    st.metric(f"{away_display}", f"{display_away:.2%}")

            fig = go.Figure(data=[go.Pie(
                labels=[f"{home_display} Win", "Draw", f"{away_display} Win"],
                values=[display_home, display_draw, display_away],
                hole=0.3,
                marker=dict(colors=['#4CAF50', '#FFB300', '#81C784'])
            )])
            fig.update_layout(title_text=f"Blended Probability (α={odds_predictor.alpha:.2f})")
            st.plotly_chart(fig, width='stretch')

            stats = odds_predictor.get_accuracy_stats()
            if stats['total_matches'] > 0:
                st.subheader("📈 Accuracy Comparison")
                acc_col1, acc_col2, acc_col3 = st.columns(3)
                with acc_col1:
                    st.metric("Model Only", f"{stats['model_accuracy']:.1%}")
                with acc_col2:
                    st.metric("Odds-Blended", f"{stats['blended_accuracy']:.1%}")
                with acc_col3:
                    delta = stats['blended_accuracy'] - stats['model_accuracy']
                    st.metric("Improvement", f"{delta:+.1%}")
        else:
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric(f"{home_display} Win", f"{display_home:.2%}")
            with col_b:
                st.metric("Draw", f"{display_draw:.2%}")
            with col_c:
                st.metric(f"{away_display} Win", f"{display_away:.2%}")

            fig = go.Figure(data=[go.Pie(
                labels=[f"{home_display} Win", "Draw", f"{away_display} Win"],
                values=[display_home, display_draw, display_away],
                hole=0.3,
                marker=dict(colors=['#4CAF50', '#FFB300', '#81C784'])
            )])
            fig.update_layout(title_text=t('probability_distribution'))
            st.plotly_chart(fig, width='stretch')

        st.subheader(f"📊 {t('factor_breakdown')}")
        premium_badge()
        if st.session_state.get('is_premium', False):
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
        else:
            premium_gate("Detailed Factor Analysis")

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
        premium_badge()
        if st.session_state.get('is_premium', False):
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
        else:
            premium_gate("X-Factor Player Details")

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
    premium_badge()
    if st.session_state.get('is_premium', False):
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
    else:
        premium_gate("Factor Weights & Model Parameters")

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

def show_extreme_environment():
    """V11.1 Extreme Environment + LightDarkBalance Analysis Page"""
    is_cn = APP_VERSION == 'china'
    
    if not v11_engine:
        st.error("V11 Engine not available" if not is_cn else "V11 引擎未載入")
        return
    
    st.title("🌡️ " + ("極端環境 × 正暗平衡分析" if is_cn else "Extreme Environment × LightDarkBalance"))
    st.caption("Formula V11.1 — 17 Dimensions × 3 EmoGlyphPlay Engines" if not is_cn else "Formula V11.1 — 17 維度 × 3 EmoGlyphPlay 引擎")
    
    from formula_v11_emoglyph import WC2026_GROUPS, ELO_RATINGS
    from wc2026_venue_data import VENUES, get_wbgt_risk, get_travel_fatigue
    from wc2026_recovery_data import get_team_recovery, get_fatigue_risk_level
    
    # Section 1: Venue Heat Map
    st.markdown("### 🌡️ " + ("場館高溫風險" if is_cn else "Venue Heat Risk"))
    
    venue_data = []
    for vid, v in VENUES.items():
        risk = get_wbgt_risk(vid, "afternoon")
        venue_data.append({
            "Venue": v["name"], "City": v["city"], "Country": v["country"],
            "WBGT (°C)": v["wbgt_threshold"], "Risk": risk["risk_level"],
            "Altitude (m)": v["altitude_meters"]
        })
    
    df_venues = pd.DataFrame(venue_data)
    risk_colors = {"low": "🟢", "medium": "🟡", "high": "🟠", "extreme": "🔴"}
    df_venues["Risk"] = df_venues["Risk"].map(lambda x: risk_colors.get(x, "⚪") + " " + x.title())
    st.dataframe(df_venues, use_container_width=True, hide_index=True)
    
    # Section 2: Team Recovery Status
    st.markdown("### 💤 " + ("球隊恢復狀態" if is_cn else "Team Recovery Status"))
    
    all_teams = []
    for teams in WC2026_GROUPS.values():
        all_teams.extend(teams)
    
    recovery_data = []
    for team in all_teams:
        rec = get_team_recovery(team)
        risk = get_fatigue_risk_level(team)
        risk_icon = {"low": "🟢", "medium": "🟡", "high": "🟠", "extreme": "🔴"}.get(risk, "⚪")
        recovery_data.append({
            "Team": team, "League": rec["primary_league"],
            "Days Rest": rec["days_rest_before_wc"],
            "CL Players": rec["cl_final_players"],
            "Recovery": f"{rec['recovery_coefficient']:.2f}",
            "Risk": f"{risk_icon} {risk.title()}"
        })
    
    df_recovery = pd.DataFrame(recovery_data)
    st.dataframe(df_recovery, use_container_width=True, hide_index=True)
    
    # Section 3: Match Prediction with LightDarkBalance
    st.markdown("### ⚖️ " + ("正暗平衡預測" if is_cn else "LightDarkBalance Prediction"))
    
    col1, col2 = st.columns(2)
    with col1:
        team_a = st.selectbox("Team A" if not is_cn else "球隊 A", all_teams, index=0, key="v11_team_a")
    with col2:
        team_b = st.selectbox("Team B" if not is_cn else "球隊 B", all_teams, index=5, key="v11_team_b")
    
    col_v, col_t = st.columns(2)
    with col_v:
        venue_id = st.selectbox("Venue" if not is_cn else "場館", list(VENUES.keys()), 
                                format_func=lambda x: VENUES[x]["name"], key="v11_venue")
    with col_t:
        match_time = st.selectbox("Time" if not is_cn else "時間", 
                                  ["morning", "afternoon", "evening"], index=1, key="v11_time")
    
    stage = st.selectbox("Stage" if not is_cn else "階段",
                         ["group", "r32", "r16", "qf", "sf", "final"], index=1, key="v11_stage")
    
    if st.button("🔮 " + ("預測" if is_cn else "Predict"), key="v11_predict_btn"):
        ctx = {"venue_id": venue_id, "match_time": match_time, "stage": stage, "match_number": 4}
        result = v11_engine.predict_match(team_a, team_b, ctx)
        
        # Win probabilities
        st.markdown("#### " + ("勝率預測" if is_cn else "Win Probability"))
        prob_col1, prob_col2, prob_col3 = st.columns(3)
        with prob_col1:
            st.metric(team_a, f"{result['prob_a_win']:.1%}")
        with prob_col2:
            st.metric("Draw" if not is_cn else "平局", f"{result['prob_draw']:.1%}")
        with prob_col3:
            st.metric(team_b, f"{result['prob_b_win']:.1%}")
        
        # LightDarkBalance
        st.markdown("#### ⚖️ LightDarkBalance")
        ldb_col1, ldb_col2 = st.columns(2)
        with ldb_col1:
            ldb_a = result["ldb_a"]
            confidence_icon = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(ldb_a["confidence"], "⚪")
            st.markdown(f"**{team_a}**")
            st.markdown(f"- LDB Score: {ldb_a['ldb']:.3f}")
            st.markdown(f"- Light: {ldb_a['light']:.3f} | Dark: {ldb_a['dark']:.3f}")
            st.markdown(f"- Confidence: {confidence_icon} {ldb_a['confidence']}")
        with ldb_col2:
            ldb_b = result["ldb_b"]
            confidence_icon = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(ldb_b["confidence"], "⚪")
            st.markdown(f"**{team_b}**")
            st.markdown(f"- LDB Score: {ldb_b['ldb']:.3f}")
            st.markdown(f"- Light: {ldb_b['light']:.3f} | Dark: {ldb_b['dark']:.3f}")
            st.markdown(f"- Confidence: {confidence_icon} {ldb_b['confidence']}")
        
        if result["upset_alert"]:
            st.warning("⚠️ " + ("冷門警報！此場比賽可能出現意外結果" if is_cn else "Upset Alert! This match may see an unexpected result"))
        
        # SunTzu Strategy
        st.markdown("#### 🏛️ SunTzu " + ("策略分析" if is_cn else "Strategy"))
        st_col1, st_col2 = st.columns(2)
        with st_col1:
            sz_a = result["suntzu_a"]
            st.markdown(f"**{team_a}**: {sz_a['suntzu']:.3f}")
            st.markdown(f"道(Purpose): {sz_a['dao']:.2f} | 天(Weather): {sz_a['tian']:.2f}")
            st.markdown(f"地(Terrain): {sz_a['di']:.2f} | 將(Commander): {sz_a['jiang']:.2f}")
            st.markdown(f"法(Method): {sz_a['fa']:.2f}")
        with st_col2:
            sz_b = result["suntzu_b"]
            st.markdown(f"**{team_b}**: {sz_b['suntzu']:.3f}")
            st.markdown(f"道(Purpose): {sz_b['dao']:.2f} | 天(Weather): {sz_b['tian']:.2f}")
            st.markdown(f"地(Terrain): {sz_b['di']:.2f} | 將(Commander): {sz_b['jiang']:.2f}")
            st.markdown(f"法(Method): {sz_b['fa']:.2f}")
        
        # Dimension Scores
        st.markdown("#### 📊 " + ("17維度評分" if is_cn else "17 Dimension Scores"))
        dim_data = []
        for dim in result["scores_a"]:
            dim_data.append({
                "Dimension": dim,
                team_a: result["scores_a"][dim],
                team_b: result["scores_b"].get(dim, 0),
                "Gap": result["scores_a"][dim] - result["scores_b"].get(dim, 0),
                "Weight": v11_engine.weights.get(dim, 0)
            })
        df_dims = pd.DataFrame(dim_data)
        st.dataframe(df_dims.style.format({team_a: "{:.3f}", team_b: "{:.3f}", "Gap": "{:+.3f}", "Weight": "{:.0%}"}),
                     use_container_width=True, hide_index=True)

def show_team_path_strategy():
    """Team Path Strategy page — per-team path analysis with social media export"""
    is_cn = APP_VERSION == 'china'

    if not _PATH_GEN_AVAILABLE:
        st.error("Team Path Generator not available" if not is_cn else "球隊路徑生成器未載入")
        return

    st.title("🗺️ " + ("球隊路徑策略分析" if is_cn else "Team Path Strategy"))
    st.caption("Formula V11.1 — 17 Dimensions × 3 EmoGlyphPlay Engines × 48-Team Structural Advantage" if not is_cn
               else "Formula V11.1 — 17 維度 × 3 EmoGlyphPlay 引擎 × 48 隊結構優勢")

    from formula_v11_emoglyph import WC2026_GROUPS
    from wc2026_team_path_generator import TeamPathGenerator

    @st.cache_resource
    def load_path_gen():
        return TeamPathGenerator()

    path_gen = load_path_gen()

    # Build team list from groups
    all_teams = []
    for teams in WC2026_GROUPS.values():
        all_teams.extend(teams)

    # Team selector
    selected_team = st.selectbox(
        "Select Team" if not is_cn else "選擇球隊",
        all_teams,
        index=all_teams.index("France") if "France" in all_teams else 0,
        key="path_team_select"
    )

    # Language for social media
    sm_lang = st.selectbox(
        "Social Media Language" if not is_cn else "社交媒體語言",
        ["en", "zh_cn", "zh_tw"],
        format_func=lambda x: {"en": "English", "zh_cn": "簡體中文", "zh_tw": "繁體中文"}[x],
        key="path_sm_lang"
    )

    if st.button("🔍 " + ("分析路徑" if is_cn else "Analyze Path"), key="path_analyze_btn"):
        with st.spinner("Generating path analysis..." if not is_cn else "正在生成路徑分析..."):
            path = path_gen.generate_team_path(selected_team)

        # Header
        st.markdown(f"## {'⚽' if not is_cn else '⚽'} {selected_team}")
        group_label = f"Group {path['group']}" if not is_cn else f"第 {path['group']} 組"
        st.markdown(f"**{group_label}** — {', '.join(path['group_teammates'])}")

        # Structural Advantage
        sa = path['structural_advantage']
        sa_score = path['structural_advantage_score']
        sa_icon = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}.get(sa, "⚪")
        sa_label = "結構優勢" if is_cn else "Structural Advantage"
        st.markdown(f"### {sa_icon} {sa_label}: {sa} ({sa_score:.0%})")
        st.caption(path['structural_advantage_reason'])

        # Group Stage Matches
        st.markdown("### 🏟️ " + ("小組賽分析" if is_cn else "Group Stage Matches"))
        for match in path['group_matches']:
            approach = match.get(f'recommended_approach_{sm_lang}',
                                match.get('recommended_approach_en', ''))
            col1, col2, col3 = st.columns([2, 2, 3])
            with col1:
                st.markdown(f"**Match {match['match']}** vs {match['opponent']}")
            with col2:
                st.markdown(f"W: {match['win_prob']:.0%} | D: {match['draw_prob']:.0%} | L: {match['loss_prob']:.0%}")
            with col3:
                st.caption(approach)

        # Projected Group Finish
        finish = path['projected_group_finish']
        confidence = path['projected_group_finish_confidence']
        finish_label = "預計小組排名" if is_cn else "Projected Group Finish"
        st.markdown(f"**{finish_label}**: {finish} ({confidence:.0%})")

        # Knockout Path
        st.markdown("### 🏆 " + ("淘汰賽路徑" if is_cn else "Knockout Path"))
        for kp in path['knockout_path']:
            stage_name = kp['stage'].upper()
            strategy = kp.get(f'strategy_{sm_lang}', kp.get('strategy_en', ''))
            key_factor = kp.get('key_factor', '')
            st.markdown(f"**{stage_name}** vs {kp['opponent_team']} — Win: {kp['win_prob']:.0%}")
            if key_factor:
                st.caption(f"Key: {key_factor} | {strategy}")

        # Overall Win Probability
        st.markdown("### 📊 " + ("奪冠概率" if is_cn else "Overall Win Probability"))
        st.metric(selected_team, f"{path['overall_win_probability']:.1%}")

        # LightDarkBalance
        ldb = path.get('light_dark_balance', {})
        if ldb:
            st.markdown("### ⚖️ LightDarkBalance")
            ldb_icon = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(ldb.get('confidence', ''), "⚪")
            col_l, col_d, col_ldb = st.columns(3)
            with col_l:
                st.metric("Light", f"{ldb.get('light', 0):.2f}")
            with col_d:
                st.metric("Dark", f"{ldb.get('dark', 0):.2f}")
            with col_ldb:
                st.metric(f"LDB {ldb_icon}", f"{ldb.get('ldb', 0):.3f}")

        # X-Factor Players
        xfactor = path.get('xfactor_players', [])
        if xfactor:
            st.markdown("### ⭐ " + ("X因子球員" if is_cn else "X-Factor Players"))
            st.markdown(", ".join(xfactor))

        # Critical Risk
        risk = path.get('critical_risk', '')
        if risk:
            st.warning(f"⚠️ {'關鍵風險' if is_cn else 'Critical Risk'}: {risk}")

        # Scenarios
        best = path.get('best_case_scenario', '')
        worst = path.get('worst_case_scenario', '')
        if best or worst:
            st.markdown("### 🔮 " + ("情景分析" if is_cn else "Scenarios"))
            col_best, col_worst = st.columns(2)
            with col_best:
                st.success(f"✅ {'最佳' if is_cn else 'Best'}: {best}")
            with col_worst:
                st.error(f"❌ {'最差' if is_cn else 'Worst'}: {worst}")

        # Social Media Export
        st.markdown("---")
        st.markdown("### 📱 " + ("社交媒體內容" if is_cn else "Social Media Content"))

        if _SOCIAL_GEN_AVAILABLE:
            from wc2026_social_media_generator import SocialMediaGenerator
            sm_gen = SocialMediaGenerator()

            spotlight = sm_gen.generate_team_spotlight(selected_team, sm_lang)
            path_pred = sm_gen.generate_path_prediction(selected_team, sm_lang)

            tab1, tab2 = st.tabs(["Spotlight", "Path Prediction" if not is_cn else "路徑預測"])
            with tab1:
                st.markdown(f"**Short (≤280 chars):**")
                st.code(spotlight['short'], language=None)
                st.markdown(f"**Long (≤1000 chars):**")
                st.code(spotlight['long'], language=None)
                st.markdown(f"**Hashtags:** {' '.join(spotlight['hashtags'])}")

            with tab2:
                st.markdown(f"**Short:**")
                st.code(path_pred['short'], language=None)
                st.markdown(f"**Long:**")
                st.code(path_pred['long'], language=None)
                st.markdown(f"**Hashtags:** {' '.join(path_pred['hashtags'])}")

        # Formula Explanation (collapsible)
        with st.expander("📖 " + ("公式原理" if is_cn else "How It Works")):
            st.markdown(path_gen.explain_formula_human_readable(sm_lang))

if __name__ == "__main__":
    main()
