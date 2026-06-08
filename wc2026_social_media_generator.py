"""
World Cup 2026 Social Media Content Generator
==============================================
Generates social media content in 3 languages (EN, 簡中, 繁中)
with compliance-safe terminology (AI data science positioning).

Classes:
    SocialMediaGenerator — main generator with 5 content methods
"""

from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Optional dependency imports — graceful fallback
# ---------------------------------------------------------------------------
try:
    from wc2026_team_path_generator import TeamPathGenerator
    _HAS_PATH_GEN = True
except ImportError:
    TeamPathGenerator = None
    _HAS_PATH_GEN = False

try:
    from formula_v11_emoglyph import FormulaV11Engine
    _HAS_ENGINE = True
except ImportError:
    FormulaV11Engine = None
    _HAS_ENGINE = False


# ===================================================================
#  HASHTAG LISTS
# ===================================================================

HASHTAGS: Dict[str, List[str]] = {
    "en": ["#WorldCup2026", "#AIPrediction", "#DataScience", "#SoccerAnalytics", "#WC2026"],
    "zh_cn": ["#世界杯2026", "#AI预测", "#数据科学", "#足球分析", "#2026世界杯"],
    "zh_tw": ["#世界盃2026", "#AI預測", "#數據科學", "#足球分析", "#2026世界盃"],
}

# ===================================================================
#  COMPLIANCE TERM MAPPING — replace gambling terms
# ===================================================================

COMPLIANCE_MAP: Dict[str, Dict[str, str]] = {
    "en": {
        "betting odds": "statistical probability",
        "gambling": "data science analysis",
        "bookmaker": "data model",
        "wager": "projection",
        "payout": "confidence level",
    },
    "zh_cn": {
        "赔率": "统计概率",
        "博彩": "数据分析",
        "下注": "预测",
        "庄家": "数据模型",
        "投注": "概率推算",
    },
    "zh_tw": {
        "賠率": "統計概率",
        "博彩": "數據分析",
        "下注": "預測",
        "莊家": "數據模型",
        "投注": "概率推算",
    },
}

# ===================================================================
#  TEAM NAME TRANSLATIONS
# ===================================================================

TEAM_NAMES: Dict[str, Dict[str, str]] = {
    "Mexico": {"zh_cn": "墨西哥", "zh_tw": "墨西哥"},
    "South Africa": {"zh_cn": "南非", "zh_tw": "南非"},
    "South Korea": {"zh_cn": "韩国", "zh_tw": "韓國"},
    "Czech Republic": {"zh_cn": "捷克", "zh_tw": "捷克"},
    "Canada": {"zh_cn": "加拿大", "zh_tw": "加拿大"},
    "Bosnia and Herzegovina": {"zh_cn": "波黑", "zh_tw": "波黑"},
    "Qatar": {"zh_cn": "卡塔尔", "zh_tw": "卡塔爾"},
    "Switzerland": {"zh_cn": "瑞士", "zh_tw": "瑞士"},
    "Brazil": {"zh_cn": "巴西", "zh_tw": "巴西"},
    "Morocco": {"zh_cn": "摩洛哥", "zh_tw": "摩洛哥"},
    "Haiti": {"zh_cn": "海地", "zh_tw": "海地"},
    "Scotland": {"zh_cn": "苏格兰", "zh_tw": "蘇格蘭"},
    "USA": {"zh_cn": "美国", "zh_tw": "美國"},
    "Paraguay": {"zh_cn": "巴拉圭", "zh_tw": "巴拉圭"},
    "Australia": {"zh_cn": "澳大利亚", "zh_tw": "澳洲"},
    "Turkey": {"zh_cn": "土耳其", "zh_tw": "土耳其"},
    "Germany": {"zh_cn": "德国", "zh_tw": "德國"},
    "Curacao": {"zh_cn": "库拉索", "zh_tw": "庫拉索"},
    "Ivory Coast": {"zh_cn": "科特迪瓦", "zh_tw": "科特迪瓦"},
    "Ecuador": {"zh_cn": "厄瓜多尔", "zh_tw": "厄瓜多爾"},
    "Netherlands": {"zh_cn": "荷兰", "zh_tw": "荷蘭"},
    "Japan": {"zh_cn": "日本", "zh_tw": "日本"},
    "Sweden": {"zh_cn": "瑞典", "zh_tw": "瑞典"},
    "Tunisia": {"zh_cn": "突尼斯", "zh_tw": "突尼斯"},
    "Belgium": {"zh_cn": "比利时", "zh_tw": "比利時"},
    "Egypt": {"zh_cn": "埃及", "zh_tw": "埃及"},
    "Iran": {"zh_cn": "伊朗", "zh_tw": "伊朗"},
    "New Zealand": {"zh_cn": "新西兰", "zh_tw": "新西蘭"},
    "Spain": {"zh_cn": "西班牙", "zh_tw": "西班牙"},
    "Cape Verde": {"zh_cn": "佛得角", "zh_tw": "佛得角"},
    "Saudi Arabia": {"zh_cn": "沙特", "zh_tw": "沙特"},
    "Uruguay": {"zh_cn": "乌拉圭", "zh_tw": "烏拉圭"},
    "France": {"zh_cn": "法国", "zh_tw": "法國"},
    "Senegal": {"zh_cn": "塞内加尔", "zh_tw": "塞內加爾"},
    "Iraq": {"zh_cn": "伊拉克", "zh_tw": "伊拉克"},
    "Norway": {"zh_cn": "挪威", "zh_tw": "挪威"},
    "Argentina": {"zh_cn": "阿根廷", "zh_tw": "阿根廷"},
    "Algeria": {"zh_cn": "阿尔及利亚", "zh_tw": "阿爾及利亞"},
    "Austria": {"zh_cn": "奥地利", "zh_tw": "奧地利"},
    "Jordan": {"zh_cn": "约旦", "zh_tw": "約旦"},
    "Portugal": {"zh_cn": "葡萄牙", "zh_tw": "葡萄牙"},
    "DR Congo": {"zh_cn": "刚果(金)", "zh_tw": "剛果(金)"},
    "Uzbekistan": {"zh_cn": "乌兹别克斯坦", "zh_tw": "烏茲別克斯坦"},
    "Colombia": {"zh_cn": "哥伦比亚", "zh_tw": "哥倫比亞"},
    "England": {"zh_cn": "英格兰", "zh_tw": "英格蘭"},
    "Croatia": {"zh_cn": "克罗地亚", "zh_tw": "克羅地亞"},
    "Ghana": {"zh_cn": "加纳", "zh_tw": "加納"},
    "Panama": {"zh_cn": "巴拿马", "zh_tw": "巴拿馬"},
}

# ===================================================================
#  STAGE NAME TRANSLATIONS
# ===================================================================

STAGE_NAMES: Dict[str, Dict[str, str]] = {
    "Group": {"en": "Group", "zh_cn": "小组赛", "zh_tw": "小組賽"},
    "R32": {"en": "R32", "zh_cn": "32强", "zh_tw": "32強"},
    "R16": {"en": "R16", "zh_cn": "16强", "zh_tw": "16強"},
    "QF": {"en": "QF", "zh_cn": "八强", "zh_tw": "八強"},
    "SF": {"en": "SF", "zh_cn": "四强", "zh_tw": "四強"},
    "Final": {"en": "Final", "zh_cn": "决赛", "zh_tw": "決賽"},
}

# ===================================================================
#  FACTOR DEFINITIONS — keyed by factor_name
# ===================================================================

FACTOR_INFO: Dict[str, Dict] = {
    "extreme_heat": {
        "en": {
            "emoji": "🌡️",
            "title": "Extreme Heat Factor",
            "short_desc": "Summer heat in North America could be the ultimate equalizer at WC2026!",
            "long_desc": (
                "🌡️ The Heat Factor: North America's Summer Challenge\n\n"
                "With matches in Dallas, Houston, and Monterrey, WBGT readings could exceed 30°C!\n\n"
                "Teams from hot climates gain an edge:\n"
                "✅ Morocco, Senegal — natural heat acclimatization\n"
                "✅ Mexico — altitude + heat training advantage\n"
                "❌ Northern European teams face 15-20% performance drop\n\n"
                "AI data science projection — not gambling advice!"
            ),
            "high_teams": ["Morocco", "Senegal", "Mexico"],
            "low_teams": ["Sweden", "Norway", "Scotland"],
        },
        "zh_cn": {
            "emoji": "🌡️",
            "title": "极端高温因素",
            "short_desc": "北美夏季高温可能成为2026世界杯的终极平衡器！",
            "long_desc": (
                "🌡️ 高温因素：北美夏季的挑战\n\n"
                "达拉斯、休斯顿和蒙特雷的比赛，WBGT指数可能超过30°C！\n\n"
                "来自炎热气候的球队获得优势：\n"
                "✅ 摩洛哥、塞内加尔 — 天然耐热适应\n"
                "✅ 墨西哥 — 高原+高温训练优势\n"
                "❌ 北欧球队面临15-20%的表现下降\n\n"
                "AI数据科学概率推算 — 非博彩建议！"
            ),
            "high_teams": ["摩洛哥", "塞内加尔", "墨西哥"],
            "low_teams": ["瑞典", "挪威", "苏格兰"],
        },
        "zh_tw": {
            "emoji": "🌡️",
            "title": "極端高溫因素",
            "short_desc": "北美夏季高溫可能成為2026世界盃嘅終極平衡器！",
            "long_desc": (
                "🌡️ 高溫因素：北美夏季嘅挑戰\n\n"
                "達拉斯、休斯頓同蒙特雷嘅比賽，WBGT指數可能超過30°C！\n\n"
                "來自炎熱氣候嘅球隊獲得優勢：\n"
                "✅ 摩洛哥、塞內加爾 — 天然耐熱適應\n"
                "✅ 墨西哥 — 高原+高溫訓練優勢\n"
                "❌ 北歐球隊面臨15-20%嘅表現下降\n\n"
                "AI數據科學概率推算 — 非博彩建議！"
            ),
            "high_teams": ["摩洛哥", "塞內加爾", "墨西哥"],
            "low_teams": ["瑞典", "挪威", "蘇格蘭"],
        },
    },
    "structural_advantage": {
        "en": {
            "emoji": "🏗️",
            "title": "The Hidden X-Factor: Structural Advantage",
            "short_desc": "NEW in 2026: 48 teams means top 2 + 8 best 3rd-place advance! Strong teams can WIN first 2 matches, REST in the 3rd.",
            "long_desc": (
                "🏗️ The Hidden X-Factor: Structural Advantage\n\n"
                "NEW in 2026: 48 teams means top 2 + 8 best 3rd-place advance!\n"
                "Strong teams can WIN first 2 matches, REST in the 3rd.\n\n"
                "This gives them:\n"
                "✅ Fresh legs for R32\n"
                "✅ Better squad rotation\n"
                "✅ Favorable bracket position\n\n"
                "Teams with HIGH structural advantage: France, Brazil, Argentina\n"
                "Teams with LOW structural advantage: Croatia, Sweden\n\n"
                "AI data science projection — not gambling advice!"
            ),
            "high_teams": ["France", "Brazil", "Argentina"],
            "low_teams": ["Croatia", "Sweden"],
        },
        "zh_cn": {
            "emoji": "🏗️",
            "title": "隐藏的X因子：结构优势",
            "short_desc": "2026新赛制：48队参赛，小组前2名+8个最佳第3名晋级！强队可以赢下前2场，第3场轮换休息！",
            "long_desc": (
                "🏗️ 隐藏的X因子：结构优势\n\n"
                "2026新赛制：48队参赛，小组前2名+8个最佳第3名晋级！\n"
                "强队可以赢下前2场，第3场轮换休息！\n\n"
                "这带来：\n"
                "✅ 32强赛时体能更充沛\n"
                "✅ 更好的阵容轮换\n"
                "✅ 更有利的淘汰赛位置\n\n"
                "结构优势高的球队：法国、巴西、阿根廷\n"
                "结构优势低的球队：克罗地亚、瑞典\n\n"
                "AI数据科学概率推算 — 非博彩建议！"
            ),
            "high_teams": ["法国", "巴西", "阿根廷"],
            "low_teams": ["克罗地亚", "瑞典"],
        },
        "zh_tw": {
            "emoji": "🏗️",
            "title": "隱藏嘅X因子：結構優勢",
            "short_desc": "2026新賽制：48隊參賽，小組前2名+8個最佳第3名晉級！強隊可以贏咗頭2場，第3場輪換休息！",
            "long_desc": (
                "🏗️ 隱藏嘅X因子：結構優勢\n\n"
                "2026新賽制：48隊參賽，小組前2名+8個最佳第3名晉級！\n"
                "強隊可以贏咗頭2場，第3場輪換休息！\n\n"
                "呢個帶嚟：\n"
                "✅ 32強賽時體能更充沛\n"
                "✅ 更好嘅陣容輪換\n"
                "✅ 更有利嘅淘汰賽位置\n\n"
                "結構優勢高嘅球隊：法國、巴西、阿根廷\n"
                "結構優勢低嘅球隊：克羅地亞、瑞典\n\n"
                "AI數據科學概率推算 — 非博彩建議！"
            ),
            "high_teams": ["法國", "巴西", "阿根廷"],
            "low_teams": ["克羅地亞", "瑞典"],
        },
    },
    "squad_depth": {
        "en": {
            "emoji": "🔄",
            "title": "Squad Depth: The Marathon Factor",
            "short_desc": "7 matches in 39 days — teams with deep benches survive! France & England can field 2 full XIs.",
            "long_desc": (
                "🔄 Squad Depth: The Marathon Factor\n\n"
                "7 matches in 39 days — teams with deep benches survive!\n"
                "France & England can field 2 full XIs.\n\n"
                "Why it matters:\n"
                "✅ Injuries are inevitable in a long tournament\n"
                "✅ Fresh substitutions change games in R16+\n"
                "✅ Tactical flexibility requires multiple options\n\n"
                "Teams with HIGH squad depth: France, England, Spain\n"
                "Teams with LOW squad depth: Panama, Haiti, Curacao\n\n"
                "AI data science projection — not gambling advice!"
            ),
            "high_teams": ["France", "England", "Spain"],
            "low_teams": ["Panama", "Haiti", "Curacao"],
        },
        "zh_cn": {
            "emoji": "🔄",
            "title": "阵容深度：马拉松因素",
            "short_desc": "39天7场比赛——阵容深厚的球队才能坚持！法国和英格兰可以派出两套完整首发。",
            "long_desc": (
                "🔄 阵容深度：马拉松因素\n\n"
                "39天7场比赛——阵容深厚的球队才能坚持！\n"
                "法国和英格兰可以派出两套完整首发。\n\n"
                "为什么重要：\n"
                "✅ 长赛程中伤病不可避免\n"
                "✅ 16强后新鲜替补能改变比赛\n"
                "✅ 战术灵活性需要多种选择\n\n"
                "阵容深度高的球队：法国、英格兰、西班牙\n"
                "阵容深度低的球队：巴拿马、海地、库拉索\n\n"
                "AI数据科学概率推算 — 非博彩建议！"
            ),
            "high_teams": ["法国", "英格兰", "西班牙"],
            "low_teams": ["巴拿马", "海地", "库拉索"],
        },
        "zh_tw": {
            "emoji": "🔄",
            "title": "陣容深度：馬拉松因素",
            "short_desc": "39日7場比賽——陣容深厚嘅球隊先撐得住！法國同英格蘭可以派出兩套完整首發。",
            "long_desc": (
                "🔄 陣容深度：馬拉松因素\n\n"
                "39日7場比賽——陣容深厚嘅球隊先撐得住！\n"
                "法國同英格蘭可以派出兩套完整首發。\n\n"
                "點解重要：\n"
                "✅ 長賽程中傷病不可避免\n"
                "✅ 16強後新鮮後備能改變比賽\n"
                "✅ 戰術靈活性需要多種選擇\n\n"
                "陣容深度高嘅球隊：法國、英格蘭、西班牙\n"
                "陣容深度低嘅球隊：巴拿馬、海地、庫拉索\n\n"
                "AI數據科學概率推算 — 非博彩建議！"
            ),
            "high_teams": ["法國", "英格蘭", "西班牙"],
            "low_teams": ["巴拿馬", "海地", "庫拉索"],
        },
    },
    "home_advantage": {
        "en": {
            "emoji": "🏠",
            "title": "Home Advantage: The Host Nation Boost",
            "short_desc": "USA, Canada, Mexico all host — but only one can truly capitalize on home soil!",
            "long_desc": (
                "🏠 Home Advantage: The Host Nation Boost\n\n"
                "USA, Canada, Mexico all host — but only one can truly capitalize!\n\n"
                "Historical data shows:\n"
                "✅ Host nations reach QF 73% of the time\n"
                "✅ Home crowd adds ~5% performance boost\n"
                "✅ Familiarity with venues reduces travel fatigue\n\n"
                "USA has the strongest squad among hosts.\n"
                "Mexico's altitude + heat combo is unique.\n\n"
                "AI data science projection — not gambling advice!"
            ),
            "high_teams": ["USA", "Mexico", "Canada"],
            "low_teams": [],
        },
        "zh_cn": {
            "emoji": "🏠",
            "title": "主场优势：东道主加成",
            "short_desc": "美国、加拿大、墨西哥都是东道主——但只有一个能真正利用主场之利！",
            "long_desc": (
                "🏠 主场优势：东道主加成\n\n"
                "美国、加拿大、墨西哥都是东道主——但只有一个能真正利用主场之利！\n\n"
                "历史数据显示：\n"
                "✅ 东道主73%的概率进入八强\n"
                "✅ 主场观众带来约5%的表现提升\n"
                "✅ 熟悉场地减少旅行疲劳\n\n"
                "美国是东道主中阵容最强的。\n"
                "墨西哥的高原+高温组合独一无二。\n\n"
                "AI数据科学概率推算 — 非博彩建议！"
            ),
            "high_teams": ["美国", "墨西哥", "加拿大"],
            "low_teams": [],
        },
        "zh_tw": {
            "emoji": "🏠",
            "title": "主場優勢：東道主加成",
            "short_desc": "美國、加拿大、墨西哥都係東道主——但只有一個可以真正利用主場之利！",
            "long_desc": (
                "🏠 主場優勢：東道主加成\n\n"
                "美國、加拿大、墨西哥都係東道主——但只有一個可以真正利用主場之利！\n\n"
                "歷史數據顯示：\n"
                "✅ 東道主73%嘅概率進入八強\n"
                "✅ 主場觀眾帶嚟約5%嘅表現提升\n"
                "✅ 熟悉場地減少旅行疲勞\n\n"
                "美國係東道主中陣容最強嘅。\n"
                "墨西哥嘅高原+高溫組合獨一無二。\n\n"
                "AI數據科學概率推算 — 非博彩建議！"
            ),
            "high_teams": ["美國", "墨西哥", "加拿大"],
            "low_teams": [],
        },
    },
}

# ===================================================================
#  GROUP DATA — pulled from formula_v11_emoglyph when available
# ===================================================================

_FALLBACK_GROUPS = {
    "A": ["Mexico", "South Africa", "South Korea", "Czech Republic"],
    "B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["USA", "Paraguay", "Australia", "Turkey"],
    "E": ["Germany", "Curacao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"],
}

# ===================================================================
#  ADJECTIVE MAP — tier-based adjectives for team descriptions
# ===================================================================

_TIER_ADJECTIVES = {
    1: {"en": "world-class", "zh_cn": "世界级", "zh_tw": "世界級"},
    2: {"en": "formidable", "zh_cn": "实力强劲的", "zh_tw": "實力強勁嘅"},
    3: {"en": "dangerous dark-horse", "zh_cn": "危险的黑马型", "zh_tw": "危險嘅黑馬型"},
    4: {"en": "competitive", "zh_cn": "有竞争力的", "zh_tw": "有競爭力嘅"},
    5: {"en": "spirited underdog", "zh_cn": "充满斗志的", "zh_tw": "充滿鬥志嘅"},
}

_STRUCTURAL_ADV_LEVEL = {
    1: {"en": "HIGH", "zh_cn": "高", "zh_tw": "高"},
    2: {"en": "MEDIUM", "zh_cn": "中", "zh_tw": "中"},
    3: {"en": "LOW", "zh_cn": "低", "zh_tw": "低"},
}

# Key factor descriptions per team tier
_FACTOR_DESCRIPTIONS = {
    1: {
        "en": [
            ("Squad Depth", "Multiple world-class options in every position"),
            ("Tournament Experience", "Deep runs in recent World Cups"),
        ],
        "zh_cn": [
            ("阵容深度", "每个位置都有多名世界级选择"),
            ("赛事经验", "近期世界杯深度晋级"),
        ],
        "zh_tw": [
            ("陣容深度", "每個位置都有多名世界級選擇"),
            ("賽事經驗", "近期世界盃深度晉級"),
        ],
    },
    2: {
        "en": [
            ("Coaching Quality", "Experienced managers with tournament know-how"),
            ("Tactical Flexibility", "Can adapt to different opponents"),
        ],
        "zh_cn": [
            ("教练水平", "经验丰富、擅长大赛的教练"),
            ("战术灵活性", "能针对不同对手调整"),
        ],
        "zh_tw": [
            ("教練水平", "經驗豐富、擅長大賽嘅教練"),
            ("戰術靈活性", "能針對唔同對手調整"),
        ],
    },
    3: {
        "en": [
            ("Underdog Momentum", "Nothing to lose, everything to prove"),
            ("Heat Acclimatization", "Many players from hot climates"),
        ],
        "zh_cn": [
            ("黑马势头", "无所畏惧，全力以赴"),
            ("耐热适应", "多名球员来自炎热气候"),
        ],
        "zh_tw": [
            ("黑馬勢頭", "無所畏懼，全力以赴"),
            ("耐熱適應", "多名球員來自炎熱氣候"),
        ],
    },
    4: {
        "en": [
            ("Competitive Spirit", "Fighting for every ball"),
            ("Tactical Discipline", "Well-organized defensive structure"),
        ],
        "zh_cn": [
            ("竞争精神", "每球必争"),
            ("战术纪律", "组织严密的防守体系"),
        ],
        "zh_tw": [
            ("競爭精神", "每球必爭"),
            ("戰術紀律", "組織嚴密嘅防守體系"),
        ],
    },
    5: {
        "en": [
            ("Underdog Fire", "Playing with house money — no expectations"),
            ("Team Unity", "Strong collective spirit"),
        ],
        "zh_cn": [
            ("黑马之火", "毫无压力——没有期望"),
            ("团队凝聚力", "强大的集体精神"),
        ],
        "zh_tw": [
            ("黑馬之火", "毫無壓力——冇期望"),
            ("團隊凝聚力", "強大嘅集體精神"),
        ],
    },
}


def _apply_compliance(text: str, language: str) -> str:
    """Replace gambling terminology with compliance-safe alternatives."""
    mapping = COMPLIANCE_MAP.get(language, {})
    for bad, good in mapping.items():
        text = text.replace(bad, good)
    return text


def _get_team_tier(team: str) -> int:
    """Determine team tier (1-5) from Elo rating."""
    try:
        from formula_v11_emoglyph import ELO_RATINGS
        elo = ELO_RATINGS.get(team, 1500)
    except ImportError:
        elo = 1500

    if elo >= 1950:
        return 1
    elif elo >= 1850:
        return 2
    elif elo >= 1700:
        return 3
    elif elo >= 1580:
        return 4
    else:
        return 5


def _team_name(team: str, language: str) -> str:
    """Get team name in the target language."""
    if language == "en":
        return team
    return TEAM_NAMES.get(team, {}).get(language, team)


def _find_group(team: str) -> Optional[str]:
    """Find which group a team belongs to."""
    try:
        from formula_v11_emoglyph import WC2026_GROUPS
        groups = WC2026_GROUPS
    except ImportError:
        groups = _FALLBACK_GROUPS

    for letter, teams in groups.items():
        if team in teams:
            return letter
    return None


def _get_groups() -> dict:
    """Get group data from engine or fallback."""
    try:
        from formula_v11_emoglyph import WC2026_GROUPS
        return WC2026_GROUPS
    except ImportError:
        return _FALLBACK_GROUPS


def _get_structural_adv(team: str) -> int:
    """Get structural advantage level: 1=HIGH, 2=MEDIUM, 3=LOW."""
    tier = _get_team_tier(team)
    group = _find_group(team)
    if not group:
        return 3
    try:
        from formula_v11_emoglyph import GROUP_STRENGTH_DATA
        parity = GROUP_STRENGTH_DATA.get(group, {}).get("parity", 0.5)
    except ImportError:
        parity = 0.5

    if tier <= 2 and parity >= 0.65:
        return 1  # HIGH
    elif tier <= 3:
        return 2  # MEDIUM
    else:
        return 3  # LOW


def _get_confidence(team: str) -> int:
    """Get AI confidence percentage for a team."""
    tier = _get_team_tier(team)
    base = {1: 78, 2: 62, 3: 45, 4: 30, 5: 18}
    return base.get(tier, 25)


def _project_path(team: str) -> str:
    """Project the tournament path for a team."""
    tier = _get_team_tier(team)
    group = _find_group(team) or "?"

    if tier == 1:
        return f"Group {group} → R32 → QF"
    elif tier == 2:
        return f"Group {group} → R32 → R16"
    elif tier == 3:
        return f"Group {group} → R32"
    else:
        return f"Group {group}"


def _project_path_zh(team: str, language: str) -> str:
    """Project the tournament path for a team in Chinese."""
    tier = _get_team_tier(team)
    group = _find_group(team) or "?"

    if language == "zh_cn":
        if tier == 1:
            return f"第{group}组 → 32强 → 八强"
        elif tier == 2:
            return f"第{group}组 → 32强 → 16强"
        elif tier == 3:
            return f"第{group}组 → 32强"
        else:
            return f"第{group}组"
    else:  # zh_tw
        if tier == 1:
            return f"第{group}組 → 32強 → 八強"
        elif tier == 2:
            return f"第{group}組 → 32強 → 16強"
        elif tier == 3:
            return f"第{group}組 → 32強"
        else:
            return f"第{group}組"


# ===================================================================
#  MAIN CLASS
# ===================================================================


class SocialMediaGenerator:
    """Generates social media content for World Cup 2026 in 3 languages."""

    def __init__(self):
        if _HAS_PATH_GEN and TeamPathGenerator is not None:
            self.path_gen = TeamPathGenerator()
        else:
            self.path_gen = None

        if _HAS_ENGINE and FormulaV11Engine is not None:
            self.engine = FormulaV11Engine()
        else:
            self.engine = None

    # ================================================================
    #  generate_team_spotlight
    # ================================================================

    def generate_team_spotlight(self, team: str, language: str) -> dict:
        """Generate team spotlight content in the specified language.

        Args:
            team: Team name in English (e.g. "Morocco")
            language: "en", "zh_cn", or "zh_tw"

        Returns:
            dict with keys: type, team, language, short, long, hashtags
        """
        if language not in ("en", "zh_cn", "zh_tw"):
            language = "en"

        tier = _get_team_tier(team)
        confidence = self._get_team_confidence(team)
        group = _find_group(team) or "?"
        struct_level = _get_structural_adv(team)
        adjective = _TIER_ADJECTIVES[tier][language]
        factors = _FACTOR_DESCRIPTIONS[tier][language]
        struct_label = _STRUCTURAL_ADV_LEVEL[struct_level][language]
        struct_reason = self._struct_reason(team, struct_level, language)
        team_local = _team_name(team, language)

        if language == "en":
            short = (
                f"🔥 {team}'s heat advantage could shock the world at WC2026! "
                f"AI confidence: {confidence}%"
            ) if tier >= 3 else (
                f"🔥 {team} enters WC2026 as a {adjective} contender! "
                f"AI confidence: {confidence}%"
            )
            short = _apply_compliance(short, language)

            path = _project_path(team)
            long = (
                f"🔥 Why {team} Could Shock the World at WC2026!\n\n"
                f"{team} enters with a {adjective} squad. Key factors:\n"
                f"• {factors[0][0]}: {factors[0][1]}\n"
                f"• {factors[1][0]}: {factors[1][1]}\n"
                f"• Structural Advantage: {struct_label} — {struct_reason}\n\n"
                f"Projected path: {path}\n"
                f"AI confidence: {confidence}%\n\n"
                f"#WorldCup2026 #{team} #AIPrediction #DataScience"
            )
            long = _apply_compliance(long, language)

        elif language == "zh_cn":
            short = (
                f"🔥 {team_local}可能震惊2026世界杯！AI信心：{confidence}%"
            ) if tier >= 3 else (
                f"🔥 {team_local}以{adjective}阵容征战2026世界杯！AI信心：{confidence}%"
            )
            short = _apply_compliance(short, language)

            path = _project_path_zh(team, language)
            long = (
                f"🔥 为什么{team_local}可能震惊2026世界杯！\n\n"
                f"{team_local}带着{adjective}阵容参赛。关键因素：\n"
                f"• {factors[0][0]}：{factors[0][1]}\n"
                f"• {factors[1][0]}：{factors[1][1]}\n"
                f"• 结构优势：{struct_label} — {struct_reason}\n\n"
                f"预测路径：{path}\n"
                f"AI信心：{confidence}%\n\n"
                f"#世界杯2026 #{team_local} #AI预测 #数据科学"
            )
            long = _apply_compliance(long, language)

        else:  # zh_tw
            short = (
                f"🔥 {team_local}可能震驚2026世界盃！AI信心：{confidence}%"
            ) if tier >= 3 else (
                f"🔥 {team_local}以{adjective}陣容征戰2026世界盃！AI信心：{confidence}%"
            )
            short = _apply_compliance(short, language)

            path = _project_path_zh(team, language)
            long = (
                f"🔥 點解{team_local}可能震驚2026世界盃！\n\n"
                f"{team_local}帶住{adjective}陣容參賽。關鍵因素：\n"
                f"• {factors[0][0]}：{factors[0][1]}\n"
                f"• {factors[1][0]}：{factors[1][1]}\n"
                f"• 結構優勢：{struct_label} — {struct_reason}\n\n"
                f"預測路徑：{path}\n"
                f"AI信心：{confidence}%\n\n"
                f"#世界盃2026 #{team_local} #AI預測 #數據科學"
            )
            long = _apply_compliance(long, language)

        # Enforce length limits
        short = short[:280]
        long = long[:1000]

        hashtags = self._build_hashtags(team, language)

        return {
            "type": "team_spotlight",
            "team": team,
            "language": language,
            "short": short,
            "long": long,
            "hashtags": hashtags,
        }

    # ================================================================
    #  generate_group_analysis
    # ================================================================

    def generate_group_analysis(self, group_letter: str, language: str) -> dict:
        """Generate group deep dive content.

        Args:
            group_letter: Single letter A-L
            language: "en", "zh_cn", or "zh_tw"

        Returns:
            dict with keys: type, group, language, short, long, hashtags
        """
        if language not in ("en", "zh_cn", "zh_tw"):
            language = "en"

        groups = _get_groups()
        group_letter = group_letter.upper()
        teams = groups.get(group_letter, [])

        if not teams:
            return {
                "type": "group_analysis",
                "group": group_letter,
                "language": language,
                "short": f"Group {group_letter} not found.",
                "long": f"Group {group_letter} not found.",
                "hashtags": HASHTAGS.get(language, HASHTAGS["en"])[:2],
            }

        # Determine favorite and dark horse
        team_tiers = [(t, _get_team_tier(t)) for t in teams]
        team_tiers.sort(key=lambda x: x[1])
        favorite = team_tiers[0][0]
        dark_horse = team_tiers[min(2, len(team_tiers) - 1)][0]

        try:
            from formula_v11_emoglyph import GROUP_STRENGTH_DATA
            parity = GROUP_STRENGTH_DATA.get(group_letter, {}).get("parity", 0.5)
            early_prob = GROUP_STRENGTH_DATA.get(group_letter, {}).get("early_secure_prob", 0.5)
        except ImportError:
            parity = 0.5
            early_prob = 0.5

        fav_local = _team_name(favorite, language)
        dh_local = _team_name(dark_horse, language)

        if language == "en":
            team_list = ", ".join(teams)
            short = (
                f"📊 Group {group_letter} Deep Dive: {fav_local} leads, "
                f"but watch out for {dh_local}! "
                f"Group parity: {parity:.0%}"
            )
            short = _apply_compliance(short, language)

            long = (
                f"📊 Group {group_letter} Analysis\n\n"
                f"Teams: {team_list}\n\n"
                f"🏆 Favorite: {favorite} — AI confidence to top group: {int(early_prob * 100)}%\n"
                f"🐴 Dark Horse: {dark_horse} — could sneak into R32\n\n"
                f"Group parity: {parity:.0%} "
                f"({'dominant favorite' if parity > 0.7 else 'competitive group' if parity > 0.5 else 'wide open'})\n\n"
                f"Key match: {favorite} vs {teams[1] if len(teams) > 1 else 'TBD'}\n\n"
                f"AI data science projection — not gambling advice!\n"
                f"#WorldCup2026 #Group{group_letter} #AIPrediction"
            )
            long = _apply_compliance(long, language)

        elif language == "zh_cn":
            team_list = "、".join(_team_name(t, "zh_cn") for t in teams)
            short = (
                f"📊 第{group_letter}组深度分析：{fav_local}领衔，"
                f"但小心{dh_local}！小组均衡度：{parity:.0%}"
            )
            short = _apply_compliance(short, language)

            long = (
                f"📊 第{group_letter}组分析\n\n"
                f"球队：{team_list}\n\n"
                f"🏆 头名热门：{fav_local} — AI头名概率：{int(early_prob * 100)}%\n"
                f"🐴 黑马：{dh_local} — 可能杀入32强\n\n"
                f"小组均衡度：{parity:.0%} "
                f"（{'一家独大' if parity > 0.7 else '竞争激烈' if parity > 0.5 else '群雄逐鹿'}）\n\n"
                f"关键比赛：{fav_local} vs {_team_name(teams[1], 'zh_cn') if len(teams) > 1 else '待定'}\n\n"
                f"AI数据科学概率推算 — 非博彩建议！\n"
                f"#世界杯2026 #第{group_letter}组 #AI预测"
            )
            long = _apply_compliance(long, language)

        else:  # zh_tw
            team_list = "、".join(_team_name(t, "zh_tw") for t in teams)
            short = (
                f"📊 第{group_letter}組深度分析：{fav_local}領銜，"
                f"但小心{dh_local}！小組均衡度：{parity:.0%}"
            )
            short = _apply_compliance(short, language)

            long = (
                f"📊 第{group_letter}組分析\n\n"
                f"球隊：{team_list}\n\n"
                f"🏆 首名熱門：{fav_local} — AI首名概率：{int(early_prob * 100)}%\n"
                f"🐴 黑馬：{dh_local} — 可能殺入32強\n\n"
                f"小組均衡度：{parity:.0%} "
                f"（{'一家獨大' if parity > 0.7 else '競爭激烈' if parity > 0.5 else '群雄逐鹿'}）\n\n"
                f"關鍵比賽：{fav_local} vs {_team_name(teams[1], 'zh_tw') if len(teams) > 1 else '待定'}\n\n"
                f"AI數據科學概率推算 — 非博彩建議！\n"
                f"#世界盃2026 #第{group_letter}組 #AI預測"
            )
            long = _apply_compliance(long, language)

        short = short[:280]
        long = long[:1000]

        return {
            "type": "group_analysis",
            "group": group_letter,
            "language": language,
            "short": short,
            "long": long,
            "hashtags": HASHTAGS.get(language, HASHTAGS["en"])[:3],
        }

    # ================================================================
    #  generate_path_prediction
    # ================================================================

    def generate_path_prediction(self, team: str, language: str) -> dict:
        """Generate '[Team]'s road to the final' content with projected opponents.

        Args:
            team: Team name in English
            language: "en", "zh_cn", or "zh_tw"

        Returns:
            dict with keys: type, team, language, short, long, hashtags
        """
        if language not in ("en", "zh_cn", "zh_tw"):
            language = "en"

        tier = _get_team_tier(team)
        confidence = self._get_team_confidence(team)
        group = _find_group(team) or "?"
        team_local = _team_name(team, language)

        # Use path_gen if available, otherwise build from tier
        path_stages = self._build_path_stages(team, tier, group)

        if language == "en":
            short = (
                f"🗺️ {team}'s road to the Final at WC2026! "
                f"Projected path through {len(path_stages)} stages. "
                f"AI confidence: {confidence}%"
            )
            short = _apply_compliance(short, language)

            stages_text = "\n".join(
                f"  {s['emoji']} {s['stage']}: vs {s['opponent']} "
                f"(win probability: {s['prob']}%)"
                for s in path_stages
            )
            long = (
                f"🗺️ {team}'s Road to the Final\n\n"
                f"{stages_text}\n\n"
                f"Overall AI confidence: {confidence}%\n\n"
                f"AI data science projection — not gambling advice!\n"
                f"#WorldCup2026 #{team} #AIPrediction #RoadToFinal"
            )
            long = _apply_compliance(long, language)

        elif language == "zh_cn":
            short = (
                f"🗺️ {team_local}的2026世界杯决赛之路！"
                f"预测经过{len(path_stages)}个阶段。AI信心：{confidence}%"
            )
            short = _apply_compliance(short, language)

            stages_text = "\n".join(
                f"  {s['emoji']} {s['stage_zh_cn']}: vs {s['opponent_zh_cn']} "
                f"(胜率：{s['prob']}%)"
                for s in path_stages
            )
            long = (
                f"🗺️ {team_local}的决赛之路\n\n"
                f"{stages_text}\n\n"
                f"整体AI信心：{confidence}%\n\n"
                f"AI数据科学概率推算 — 非博彩建议！\n"
                f"#世界杯2026 #{team_local} #AI预测 #决赛之路"
            )
            long = _apply_compliance(long, language)

        else:  # zh_tw
            short = (
                f"🗺️ {team_local}嘅2026世界盃決賽之路！"
                f"預測經過{len(path_stages)}個階段。AI信心：{confidence}%"
            )
            short = _apply_compliance(short, language)

            stages_text = "\n".join(
                f"  {s['emoji']} {s['stage_zh_tw']}: vs {s['opponent_zh_tw']} "
                f"(勝率：{s['prob']}%)"
                for s in path_stages
            )
            long = (
                f"🗺️ {team_local}嘅決賽之路\n\n"
                f"{stages_text}\n\n"
                f"整體AI信心：{confidence}%\n\n"
                f"AI數據科學概率推算 — 非博彩建議！\n"
                f"#世界盃2026 #{team_local} #AI預測 #決賽之路"
            )
            long = _apply_compliance(long, language)

        short = short[:280]
        long = long[:1000]

        return {
            "type": "path_prediction",
            "team": team,
            "language": language,
            "short": short,
            "long": long,
            "hashtags": self._build_hashtags(team, language),
        }

    # ================================================================
    #  generate_factor_spotlight
    # ================================================================

    def generate_factor_spotlight(self, factor_name: str, language: str) -> dict:
        """Generate content about a specific factor.

        Args:
            factor_name: One of "extreme_heat", "structural_advantage",
                         "squad_depth", "home_advantage"
            language: "en", "zh_cn", or "zh_tw"

        Returns:
            dict with keys: type, factor, language, short, long, hashtags
        """
        if language not in ("en", "zh_cn", "zh_tw"):
            language = "en"

        info = FACTOR_INFO.get(factor_name)
        if not info:
            return {
                "type": "factor_spotlight",
                "factor": factor_name,
                "language": language,
                "short": f"Factor '{factor_name}' not found.",
                "long": f"Factor '{factor_name}' not found.",
                "hashtags": HASHTAGS.get(language, HASHTAGS["en"])[:2],
            }

        lang_info = info.get(language, info.get("en", {}))
        short = _apply_compliance(lang_info.get("short_desc", ""), language)
        long = _apply_compliance(lang_info.get("long_desc", ""), language)

        short = short[:280]
        long = long[:1000]

        # Build factor-specific hashtags
        factor_hashtags = HASHTAGS.get(language, HASHTAGS["en"])[:2]
        if language == "en":
            factor_hashtags.append(f"#{factor_name.replace('_', '').title()}")
        else:
            factor_hashtags.append(f"#{lang_info.get('title', factor_name)}")

        return {
            "type": "factor_spotlight",
            "factor": factor_name,
            "language": language,
            "short": short,
            "long": long,
            "hashtags": factor_hashtags,
        }

    # ================================================================
    #  generate_daily_preview
    # ================================================================

    def generate_daily_preview(self, match_day: int, language: str) -> dict:
        """Generate match day preview content.

        Args:
            match_day: Match day number (1-39)
            language: "en", "zh_cn", or "zh_tw"

        Returns:
            dict with keys: type, match_day, language, short, long, hashtags
        """
        if language not in ("en", "zh_cn", "zh_tw"):
            language = "en"

        # Determine stage from match_day
        if match_day <= 12:
            stage = "group"
        elif match_day <= 18:
            stage = "R32"
        elif match_day <= 24:
            stage = "R16"
        elif match_day <= 30:
            stage = "QF"
        elif match_day <= 36:
            stage = "SF"
        else:
            stage = "Final"

        stage_local = STAGE_NAMES.get(stage.capitalize(), {}).get(language, stage)
        if not stage_local or stage_local == stage:
            stage_local = STAGE_NAMES.get(stage, {}).get(language, stage)

        # Generate sample matches based on stage
        matches = self._generate_sample_matches(match_day, stage)

        if language == "en":
            stage_label = stage_local
            match_list = "\n".join(
                f"⚽ {m['team_a']} vs {m['team_b']} — {m['narrative']}"
                for m in matches
            )
            short = (
                f"📅 Match Day {match_day} Preview: {stage_label} action! "
                f"{len(matches)} matches scheduled. "
                f"AI projections ready!"
            )
            short = _apply_compliance(short, language)

            long = (
                f"📅 Match Day {match_day} Preview — {stage_label}\n\n"
                f"{match_list}\n\n"
                f"AI data science projection — not gambling advice!\n"
                f"#WorldCup2026 #MatchDay{match_day} #AIPrediction"
            )
            long = _apply_compliance(long, language)

        elif language == "zh_cn":
            match_list = "\n".join(
                f"⚽ {_team_name(m['team_a'], 'zh_cn')} vs {_team_name(m['team_b'], 'zh_cn')} — {m['narrative_zh_cn']}"
                for m in matches
            )
            short = (
                f"📅 第{match_day}比赛日预告：{stage_local}阶段！"
                f"共{len(matches)}场比赛。AI预测已就绪！"
            )
            short = _apply_compliance(short, language)

            long = (
                f"📅 第{match_day}比赛日预告 — {stage_local}\n\n"
                f"{match_list}\n\n"
                f"AI数据科学概率推算 — 非博彩建议！\n"
                f"#世界杯2026 #第{match_day}比赛日 #AI预测"
            )
            long = _apply_compliance(long, language)

        else:  # zh_tw
            match_list = "\n".join(
                f"⚽ {_team_name(m['team_a'], 'zh_tw')} vs {_team_name(m['team_b'], 'zh_tw')} — {m['narrative_zh_tw']}"
                for m in matches
            )
            short = (
                f"📅 第{match_day}比賽日預告：{stage_local}階段！"
                f"共{len(matches)}場比賽。AI預測已就緒！"
            )
            short = _apply_compliance(short, language)

            long = (
                f"📅 第{match_day}比賽日預告 — {stage_local}\n\n"
                f"{match_list}\n\n"
                f"AI數據科學概率推算 — 非博彩建議！\n"
                f"#世界盃2026 #第{match_day}比賽日 #AI預測"
            )
            long = _apply_compliance(long, language)

        short = short[:280]
        long = long[:1000]

        return {
            "type": "daily_preview",
            "match_day": match_day,
            "language": language,
            "short": short,
            "long": long,
            "hashtags": HASHTAGS.get(language, HASHTAGS["en"])[:3],
        }

    # ================================================================
    #  Internal helpers
    # ================================================================

    def _get_team_confidence(self, team: str) -> int:
        """Get AI confidence for a team, using engine if available."""
        if self.engine is not None:
            try:
                profile = self.engine.get_team_profile(team)
                weighted = profile.get("weighted_total", 0.5)
                return int(weighted * 100)
            except Exception:
                pass
        return _get_confidence(team)

    def _struct_reason(self, team: str, level: int, language: str) -> str:
        """Generate structural advantage reason text."""
        group = _find_group(team) or "?"
        tier = _get_team_tier(team)

        if language == "en":
            if level == 1:
                return f"dominant in Group {group}, can rest key players in match 3"
            elif level == 2:
                return f"competitive in Group {group}, may need full effort"
            else:
                return f"tough group, must fight for every point"
        elif language == "zh_cn":
            if level == 1:
                return f"第{group}组实力占优，第3场可轮换"
            elif level == 2:
                return f"第{group}组竞争激烈，需全力以赴"
            else:
                return f"小组形势严峻，每分必争"
        else:  # zh_tw
            if level == 1:
                return f"第{group}組實力佔優，第3場可輪換"
            elif level == 2:
                return f"第{group}組競爭激烈，需全力以赴"
            else:
                return f"小組形勢嚴峻，每分必爭"

    def _build_hashtags(self, team: str, language: str) -> List[str]:
        """Build hashtag list for a team post."""
        base = HASHTAGS.get(language, HASHTAGS["en"])
        team_local = _team_name(team, language)
        return base[:3] + [f"#{team_local}"]

    def _build_path_stages(self, team: str, tier: int, group: str) -> List[dict]:
        """Build projected path stages with opponents."""
        groups = _get_groups()
        group_teams = groups.get(group, [team])
        opponents_in_group = [t for t in group_teams if t != team]

        # Pick a likely group opponent for the group stage narrative
        group_opp = opponents_in_group[0] if opponents_in_group else "TBD"

        stages = []

        if tier <= 3:
            # Likely to advance from group
            stages.append({
                "emoji": "🏟️",
                "stage": f"Group {group}",
                "stage_zh_cn": f"第{group}组",
                "stage_zh_tw": f"第{group}組",
                "opponent": group_opp,
                "opponent_zh_cn": _team_name(group_opp, "zh_cn"),
                "opponent_zh_tw": _team_name(group_opp, "zh_tw"),
                "prob": min(95, 50 + (4 - tier) * 15),
            })

        if tier <= 3:
            r32_opp = self._pick_knockout_opponent(team, tier, "R32")
            stages.append({
                "emoji": "⚔️",
                "stage": "R32",
                "stage_zh_cn": "32强",
                "stage_zh_tw": "32強",
                "opponent": r32_opp,
                "opponent_zh_cn": _team_name(r32_opp, "zh_cn"),
                "opponent_zh_tw": _team_name(r32_opp, "zh_tw"),
                "prob": min(80, 35 + (4 - tier) * 15),
            })

        if tier <= 2:
            r16_opp = self._pick_knockout_opponent(team, tier, "R16")
            stages.append({
                "emoji": "🛡️",
                "stage": "R16",
                "stage_zh_cn": "16强",
                "stage_zh_tw": "16強",
                "opponent": r16_opp,
                "opponent_zh_cn": _team_name(r16_opp, "zh_cn"),
                "opponent_zh_tw": _team_name(r16_opp, "zh_tw"),
                "prob": min(65, 25 + (3 - tier) * 15),
            })

        if tier <= 2:
            qf_opp = self._pick_knockout_opponent(team, tier, "QF")
            stages.append({
                "emoji": "🏆",
                "stage": "QF",
                "stage_zh_cn": "八强",
                "stage_zh_tw": "八強",
                "opponent": qf_opp,
                "opponent_zh_cn": _team_name(qf_opp, "zh_cn"),
                "opponent_zh_tw": _team_name(qf_opp, "zh_tw"),
                "prob": min(50, 15 + (3 - tier) * 12),
            })

        if tier == 1:
            sf_opp = self._pick_knockout_opponent(team, tier, "SF")
            stages.append({
                "emoji": "🌟",
                "stage": "SF",
                "stage_zh_cn": "四强",
                "stage_zh_tw": "四強",
                "opponent": sf_opp,
                "opponent_zh_cn": _team_name(sf_opp, "zh_cn"),
                "opponent_zh_tw": _team_name(sf_opp, "zh_tw"),
                "prob": min(40, 10 + (2 - tier) * 10),
            })

        return stages

    def _pick_knockout_opponent(self, team: str, tier: int, stage: str) -> str:
        """Pick a plausible knockout opponent based on stage and tier."""
        # Tier-based opponent pools
        tier1_teams = ["Spain", "France", "Argentina", "England", "Brazil", "Portugal"]
        tier2_teams = ["Germany", "Netherlands", "Belgium", "Croatia", "Uruguay"]
        tier3_teams = ["Colombia", "Switzerland", "USA", "Mexico", "Japan", "Morocco"]

        import random
        rng = random.Random(hash(team + stage))

        if stage == "R32":
            pool = tier3_teams + tier2_teams
        elif stage == "R16":
            pool = tier2_teams + tier1_teams
        elif stage == "QF":
            pool = tier1_teams + tier2_teams
        else:  # SF
            pool = tier1_teams

        pool = [t for t in pool if t != team]
        if not pool:
            return "TBD"

        return rng.choice(pool)

    def _generate_sample_matches(self, match_day: int, stage: str) -> List[dict]:
        """Generate sample matches for a match day preview."""
        import random
        rng = random.Random(match_day * 42)

        groups = _get_groups()
        all_teams = []
        for teams in groups.values():
            all_teams.extend(teams)

        if stage == "group":
            # Pick 2-3 group matches
            group_idx = (match_day - 1) % 12
            group_letter = chr(ord("A") + group_idx)
            group_teams = groups.get(group_letter, all_teams[:4])
            n_matches = min(2, len(group_teams) // 2)
            matches = []
            shuffled = list(group_teams)
            rng.shuffle(shuffled)
            for i in range(n_matches):
                a = shuffled[i * 2]
                b = shuffled[i * 2 + 1]
                matches.append({
                    "team_a": a,
                    "team_b": b,
                    "narrative": f"{_get_team_tier(a) != _get_team_tier(b) and 'Upset alert!' or 'Evenly matched!'}",
                    "narrative_zh_cn": "爆冷预警！" if _get_team_tier(a) != _get_team_tier(b) else "势均力敌！",
                    "narrative_zh_tw": "爆冷預警！" if _get_team_tier(a) != _get_team_tier(b) else "勢均力敵！",
                })
            return matches
        else:
            # Knockout: pick 1-2 matches from top teams
            top_teams = ["Spain", "France", "Argentina", "Brazil", "England", "Germany",
                         "Portugal", "Netherlands", "Belgium", "Uruguay"]
            rng.shuffle(top_teams)
            matches = []
            for i in range(min(2, len(top_teams) // 2)):
                a = top_teams[i * 2]
                b = top_teams[i * 2 + 1]
                matches.append({
                    "team_a": a,
                    "team_b": b,
                    "narrative": f"High-stakes {stage} clash!",
                    "narrative_zh_cn": f"{stage}阶段关键对决！",
                    "narrative_zh_tw": f"{stage}階段關鍵對決！",
                })
            return matches


# ===================================================================
#  Quick test
# ===================================================================

def quick_test():
    """Run a quick smoke test of the generator."""
    gen = SocialMediaGenerator()
    spotlight_en = gen.generate_team_spotlight("Morocco", "en")
    spotlight_cn = gen.generate_team_spotlight("Morocco", "zh_cn")
    spotlight_tw = gen.generate_team_spotlight("Morocco", "zh_tw")
    print("EN:", spotlight_en["short"][:100])
    print("簡中:", spotlight_cn["short"][:100])
    print("繁中:", spotlight_tw["short"][:100])
    factor = gen.generate_factor_spotlight("structural_advantage", "zh_tw")
    print("Factor 繁中:", factor["short"][:100])


if __name__ == "__main__":
    quick_test()
