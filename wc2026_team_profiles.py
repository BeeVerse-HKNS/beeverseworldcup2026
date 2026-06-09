"""
WC2026 Team Profiles — Structured profile data for all 48 World Cup 2026 teams.

Each team entry contains coach info, formation, main player, strategy,
strengths, weaknesses, style classification, FIFA ranking, and ELO rating.
All tri-lingual fields use EN / 簡中 / 繁中 keys.
"""

# ---------------------------------------------------------------------------
# Style classification (reference: formula_v11_emoglyph.py)
# ---------------------------------------------------------------------------
TEAM_STYLE_CLASSIFICATION = {
    "defensive_counter": [
        "Morocco", "Uruguay", "Switzerland", "Croatia", "Mexico", "Japan",
        "South Korea", "Saudi Arabia", "Colombia", "Senegal", "Egypt",
        "Paraguay", "Scotland", "Iran", "Tunisia", "Panama", "Uzbekistan",
        "Jordan", "Australia", "Haiti", "DR Congo", "Curacao", "South Africa",
    ],
    "attacking_possession": [
        "Brazil", "Spain", "Argentina", "Portugal", "Netherlands", "Germany",
        "Belgium", "Turkey", "Ghana", "Qatar",
    ],
    "balanced": [
        "France", "England", "USA", "Norway", "Austria", "Sweden",
        "Ivory Coast", "Algeria", "Czech Republic", "Iraq",
        "Bosnia and Herzegovina", "New Zealand", "Cape Verde", "Canada",
        "Ecuador",
    ],
}

# ---------------------------------------------------------------------------
# ELO ratings (reference: formula_v11_emoglyph.py)
# ---------------------------------------------------------------------------
ELO_RATINGS = {
    "Spain": 2050, "France": 2040, "Argentina": 2020, "England": 1990,
    "Brazil": 1975, "Portugal": 1960, "Germany": 1940, "Netherlands": 1930,
    "Belgium": 1910, "Croatia": 1900, "Uruguay": 1870, "Colombia": 1850,
    "Switzerland": 1830, "USA": 1810, "Mexico": 1800, "Japan": 1790,
    "Morocco": 1780, "Senegal": 1770, "Australia": 1760, "Turkey": 1750,
    "Austria": 1740, "Sweden": 1730, "Ecuador": 1710, "Ivory Coast": 1700,
    "Ghana": 1690, "South Korea": 1660, "Paraguay": 1650, "Egypt": 1640,
    "Algeria": 1630, "Scotland": 1620, "Norway": 1610, "Czech Republic": 1600,
    "Iran": 1590, "Tunisia": 1580, "Panama": 1570, "Iraq": 1560,
    "Bosnia and Herzegovina": 1550, "Qatar": 1540, "Saudi Arabia": 1530,
    "Uzbekistan": 1520, "Jordan": 1510, "New Zealand": 1500, "Haiti": 1490,
    "DR Congo": 1480, "Cape Verde": 1470, "Curacao": 1460, "South Africa": 1540,
    "Canada": 1620,
}

# ---------------------------------------------------------------------------
# FIFA rankings (reference: formula_v11_emoglyph.py)
# ---------------------------------------------------------------------------
FIFA_RANKINGS = {
    "Argentina": 1, "Spain": 2, "France": 3, "England": 4, "Brazil": 5,
    "Portugal": 6, "Netherlands": 7, "Germany": 8, "Belgium": 9,
    "Uruguay": 10, "Colombia": 11, "Croatia": 12, "Morocco": 13,
    "Switzerland": 14, "Mexico": 15, "USA": 16, "Senegal": 17,
    "Japan": 18, "Austria": 19, "Iran": 20, "Norway": 21,
    "Turkey": 22, "South Korea": 23, "Ecuador": 24, "Ghana": 25,
    "Canada": 26, "Australia": 27, "Egypt": 28, "Ivory Coast": 29,
    "Sweden": 30, "Algeria": 31, "Tunisia": 32, "Scotland": 33,
    "Paraguay": 34, "Saudi Arabia": 35, "Qatar": 36, "Czech Republic": 37,
    "Bosnia and Herzegovina": 38, "Iraq": 39, "DR Congo": 40,
    "Panama": 41, "Haiti": 42, "New Zealand": 43, "Jordan": 44,
    "Uzbekistan": 45, "Curacao": 46, "Cape Verde": 47,
    "South Africa": 48,
}

# ---------------------------------------------------------------------------
# WC2026 Groups
# ---------------------------------------------------------------------------
WC2026_GROUPS = {
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

# ---------------------------------------------------------------------------
# Team profiles — all 48 teams
# ---------------------------------------------------------------------------
TEAM_PROFILES = {
    # ======================================================================
    # Group A
    # ======================================================================
    "Mexico": {
        "coach": {
            "name": "Javier Aguirre",
            "nationality": "Mexican",
            "age": 67,
            "style": "Pragmatic",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Santiago Gimenez",
            "position": "ST",
            "nickname": {
                "en": "Chaco",
                "簡中": "查科",
                "繁中": "查科",
            },
        },
        "strategy": {
            "en": "Mexico rely on disciplined defensive shape and rapid transitions to catch opponents on the break. They use the flanks to stretch play before central penetration. Set-piece organization is a key pillar of their game plan.",
            "簡中": "墨西哥依靠严密的防守阵型和快速转换来打对手反击。他们利用边路拉开空间后再从中路渗透。定位球组织是他们战术计划的重要支柱。",
            "繁中": "墨西哥依靠嚴密的防守陣型和快速轉換來打對手反擊。他們利用邊路拉開空間後再從中路滲透。定位球組織是他們戰術計劃的重要支柱。",
        },
        "strengths": [
            {"en": "Counter-attacking speed", "簡中": "反击速度", "繁中": "反擊速度"},
            {"en": "Set-piece delivery", "簡中": "定位球传中", "繁中": "定位球傳中"},
            {"en": "Home crowd energy", "簡中": "主场球迷氛围", "繁中": "主場球迷氛圍"},
            {"en": "Goalkeeper experience", "簡中": "门将经验", "繁中": "門將經驗"},
        ],
        "weaknesses": [
            {"en": "Defensive lapses under pressure", "簡中": "高压下防守失误", "繁中": "高壓下防守失誤"},
            {"en": "Lack of elite centre-backs", "簡中": "缺乏顶级中后卫", "繁中": "缺乏頂級中後衛"},
            {"en": "Struggle against possession teams", "簡中": "面对控球型球队吃力", "繁中": "面對控球型球隊吃力"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 15,
        "elo_rating": 1800,
    },

    "South Africa": {
        "coach": {
            "name": "Hugo Broos",
            "nationality": "Belgian",
            "age": 72,
            "style": "Pragmatic",
        },
        "formation": "4-4-2",
        "main_player": {
            "name": "Teboho Mokoena",
            "position": "MF",
            "nickname": {
                "en": "Tebza",
                "簡中": "特布扎",
                "繁中": "特布扎",
            },
        },
        "strategy": {
            "en": "South Africa prioritize a low block and compact midfield to frustrate stronger opponents. They look to hit on the break using pace on the wings. Set-piece defending is a major focus of their preparation.",
            "簡中": "南非优先采用低位防守和紧凑的中场来限制更强的对手。他们利用边路速度打反击。定位球防守是他们备战的重点。",
            "繁中": "南非優先採用低位防守和緊湊的中場來限制更強的對手。他們利用邊路速度打反擊。定位球防守是他們備戰的重點。",
        },
        "strengths": [
            {"en": "Physical resilience", "簡中": "身体韧性", "繁中": "身體韌性"},
            {"en": "Set-piece defending", "簡中": "定位球防守", "繁中": "定位球防守"},
            {"en": "Team discipline", "簡中": "团队纪律", "繁中": "團隊紀律"},
        ],
        "weaknesses": [
            {"en": "Limited technical quality", "簡中": "技术能力有限", "繁中": "技術能力有限"},
            {"en": "Shallow squad depth", "簡中": "阵容深度不足", "繁中": "陣容深度不足"},
            {"en": "Poor finishing", "簡中": "射门效率差", "繁中": "射門效率差"},
            {"en": "Vulnerable to high press", "簡中": "怕高位逼抢", "繁中": "怕高位逼搶"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 48,
        "elo_rating": 1540,
    },

    "South Korea": {
        "coach": {
            "name": "Hong Myung-bo",
            "nationality": "South Korean",
            "age": 56,
            "style": "Pragmatic",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Son Heung-min",
            "position": "LW",
            "nickname": {
                "en": "Sonny",
                "簡中": "孙哥",
                "繁中": "孫哥",
            },
        },
        "strategy": {
            "en": "South Korea build their game around Son's explosive runs and clinical finishing on the break. The double pivot shields the back four while the attacking midfield trio supports quick transitions. They are dangerous from wide areas and set pieces.",
            "簡中": "韩国围绕孙兴慜的爆发力奔跑和反击中的精准射门构建战术。双后腰保护后防线，攻击型中场三人组支持快速转换。他们在边路和定位球上极具威胁。",
            "繁中": "韓國圍繞孫興慜的爆發力奔跑和反擊中的精準射門構建戰術。雙後腰保護後防線，攻擊型中場三人組支持快速轉換。他們在邊路和定位球上極具威脅。",
        },
        "strengths": [
            {"en": "Son's individual brilliance", "簡中": "孙兴慜个人能力", "繁中": "孫興慜個人能力"},
            {"en": "Pace on the counter", "簡中": "反击速度", "繁中": "反擊速度"},
            {"en": "Set-piece threat", "簡中": "定位球威胁", "繁中": "定位球威脅"},
            {"en": "Work rate across the pitch", "簡中": "全场跑动能力", "繁中": "全場跑動能力"},
        ],
        "weaknesses": [
            {"en": "Over-reliance on Son", "簡中": "过度依赖孙兴慜", "繁中": "過度依賴孫興慜"},
            {"en": "Centre-back vulnerability", "簡中": "中后卫薄弱", "繁中": "中後衛薄弱"},
            {"en": "Midfield creativity gaps", "簡中": "中场创造力不足", "繁中": "中場創造力不足"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 23,
        "elo_rating": 1660,
    },

    "Czech Republic": {
        "coach": {
            "name": "Ivan Hasek",
            "nationality": "Czech",
            "age": 60,
            "style": "Balanced",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Vladimir Coufal",
            "position": "RB",
            "nickname": {
                "en": "Vlada",
                "簡中": "弗拉达",
                "繁中": "弗拉達",
            },
        },
        "strategy": {
            "en": "The Czech Republic favour a structured 4-2-3-1 that balances defensive solidity with measured build-up play. They rely on set pieces and crossing situations to create chances. The double pivot provides a stable platform for the attacking midfielders.",
            "簡中": "捷克偏好结构化的4-2-3-1阵型，平衡防守稳固与有序的推进。他们依靠定位球和传中创造机会。双后腰为攻击型中场提供稳定平台。",
            "繁中": "捷克偏好結構化的4-2-3-1陣型，平衡防守穩固與有序的推進。他們依靠定位球和傳中創造機會。雙後腰為攻擊型中場提供穩定平台。",
        },
        "strengths": [
            {"en": "Set-piece efficiency", "簡中": "定位球效率", "繁中": "定位球效率"},
            {"en": "Organized defense", "簡中": "防守有序", "繁中": "防守有序"},
            {"en": "Aerial duels", "簡中": "争顶能力", "繁中": "爭頂能力"},
        ],
        "weaknesses": [
            {"en": "Lack of pace in wide areas", "簡中": "边路速度不足", "繁中": "邊路速度不足"},
            {"en": "Limited creative midfielders", "簡中": "缺乏创造性中场", "繁中": "缺乏創造性中場"},
            {"en": "Squad depth concerns", "簡中": "阵容深度堪忧", "繁中": "陣容深度堪憂"},
        ],
        "style": "balanced",
        "fifa_ranking": 37,
        "elo_rating": 1600,
    },

    # ======================================================================
    # Group B
    # ======================================================================
    "Canada": {
        "coach": {
            "name": "Jesse Marsch",
            "nationality": "American",
            "age": 51,
            "style": "Intense pressing",
        },
        "formation": "4-4-2",
        "main_player": {
            "name": "Alphonso Davies",
            "position": "LB",
            "nickname": {
                "en": "Phonzie",
                "簡中": "冯齐",
                "繁中": "馮齊",
            },
        },
        "strategy": {
            "en": "Canada employ a high-energy pressing system under Marsch, looking to win the ball in advanced areas and attack quickly. Davies provides explosive width from left-back while the forward pairing stretches opposition defences. Their intensity can overwhelm opponents in the first 30 minutes.",
            "簡中": "加拿大在马什带领下采用高能逼抢体系，力求在前场夺回球权后快速进攻。戴维斯从左后卫位置提供爆发性宽度，前锋搭档拉开对手防线。他们的强度在前30分钟可以压倒对手。",
            "繁中": "加拿大在馬什帶領下採用高能逼搶體系，力求在前場奪回球權後快速進攻。戴維斯從左後衛位置提供爆發性寬度，前鋒搭檔拉開對手防線。他們的強度在前30分鐘可以壓倒對手。",
        },
        "strengths": [
            {"en": "Athleticism and pace", "簡中": "运动能力和速度", "繁中": "運動能力和速度"},
            {"en": "High pressing intensity", "簡中": "高位逼抢强度", "繁中": "高位逼搶強度"},
            {"en": "Davies' attacking threat from deep", "簡中": "戴维斯后插上威胁", "繁中": "戴維斯後插上威脅"},
        ],
        "weaknesses": [
            {"en": "Technical limitations in midfield", "簡中": "中场技术有限", "繁中": "中場技術有限"},
            {"en": "Defensive transitions", "簡中": "防守转换慢", "繁中": "防守轉換慢"},
            {"en": "Inexperience at elite level", "簡中": "顶级赛事经验不足", "繁中": "頂級賽事經驗不足"},
            {"en": "Squad depth beyond first XI", "簡中": "首发之外阵容深度不足", "繁中": "首發之外陣容深度不足"},
        ],
        "style": "balanced",
        "fifa_ranking": 26,
        "elo_rating": 1620,
    },

    "Bosnia and Herzegovina": {
        "coach": {
            "name": "Sergej Barbarez",
            "nationality": "Bosnian",
            "age": 53,
            "style": "Pragmatic",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Edin Dzeko",
            "position": "ST",
            "nickname": {
                "en": "The Diamond",
                "簡中": "钻石",
                "繁中": "鑽石",
            },
        },
        "strategy": {
            "en": "Bosnia build around Dzeko's hold-up play and aerial presence in a pragmatic 4-3-3. They look to play direct into the striker and use second-ball recoveries to create chances. The midfield three focuses on ball retention and recycling possession.",
            "簡中": "波黑围绕哲科的支点作用和空中优势构建务实的4-3-3。他们寻求直接找前锋，利用二点球创造机会。三中场专注于控球和重新组织进攻。",
            "繁中": "波黑圍繞哲科的支點作用和空中優勢構建務實的4-3-3。他們尋求直接找前鋒，利用二點球創造機會。三中場專注於控球和重新組織進攻。",
        },
        "strengths": [
            {"en": "Dzeko's experience and aerial ability", "簡中": "哲科经验和空中能力", "繁中": "哲科經驗和空中能力"},
            {"en": "Set-piece threat", "簡中": "定位球威胁", "繁中": "定位球威脅"},
            {"en": "Physical midfield", "簡中": "中场身体对抗", "繁中": "中場身體對抗"},
        ],
        "weaknesses": [
            {"en": "Aging core players", "簡中": "核心球员老化", "繁中": "核心球員老化"},
            {"en": "Lack of pace in defence", "簡中": "后防速度不足", "繁中": "後防速度不足"},
            {"en": "Limited creative options", "簡中": "创造力选择有限", "繁中": "創造力選擇有限"},
            {"en": "Shallow talent pool", "簡中": "人才储备浅", "繁中": "人才儲備淺"},
        ],
        "style": "balanced",
        "fifa_ranking": 38,
        "elo_rating": 1550,
    },

    "Qatar": {
        "coach": {
            "name": "Tintin Marquez",
            "nationality": "Spanish",
            "age": 60,
            "style": "Possession-based",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Akram Afif",
            "position": "LW",
            "nickname": {
                "en": "The Wizard",
                "簡中": "魔术师",
                "繁中": "魔術師",
            },
        },
        "strategy": {
            "en": "Qatar adopt a possession-oriented approach influenced by Spanish coaching philosophy. Afif is the creative hub drifting inside from the left to unlock defences. They circulate the ball patiently but can struggle to penetrate against deep blocks.",
            "簡中": "卡塔尔采用受西班牙教练哲学影响的控球打法。阿菲夫从左路内切作为创造核心来解锁防线。他们耐心地传导球，但面对低位防守时渗透困难。",
            "繁中": "卡塔爾採用受西班牙教練哲學影響的控球打法。阿菲夫從左路內切作為創造核心來解鎖防線。他們耐心地傳導球，但面對低位防守時滲透困難。",
        },
        "strengths": [
            {"en": "Ball retention and composure", "簡中": "控球和冷静", "繁中": "控球和冷靜"},
            {"en": "Afif's dribbling and creativity", "簡中": "阿菲夫的盘带和创造力", "繁中": "阿菲夫的盤帶和創造力"},
            {"en": "Aspire Academy cohesion", "簡中": "阿斯拜尔学院默契", "繁中": "阿斯拜爾學院默契"},
        ],
        "weaknesses": [
            {"en": "Lack of physicality", "簡中": "身体对抗不足", "繁中": "身體對抗不足"},
            {"en": "Defensive fragility", "簡中": "防守脆弱", "繁中": "防守脆弱"},
            {"en": "Struggle against high press", "簡中": "怕高位逼抢", "繁中": "怕高位逼搶"},
            {"en": "Limited goal-scoring options", "簡中": "进球选择有限", "繁中": "進球選擇有限"},
        ],
        "style": "attacking_possession",
        "fifa_ranking": 36,
        "elo_rating": 1540,
    },

    "Switzerland": {
        "coach": {
            "name": "Murat Yakin",
            "nationality": "Swiss",
            "age": 50,
            "style": "Defensively disciplined",
        },
        "formation": "3-4-2-1",
        "main_player": {
            "name": "Granit Xhaka",
            "position": "CM",
            "nickname": {
                "en": "The General",
                "簡中": "将军",
                "繁中": "將軍",
            },
        },
        "strategy": {
            "en": "Switzerland operate with a disciplined back three and a compact midfield led by Xhaka. They absorb pressure intelligently and strike on the counter through quick wide players. Their tournament experience makes them dangerous knockout opponents.",
            "簡中": "瑞士以纪律严明的三后卫和扎卡领衔的紧凑中场运作。他们聪明地吸收压力，通过快速的边路球员反击。他们的赛事经验使他们成为危险的淘汰赛对手。",
            "繁中": "瑞士以紀律嚴明的三後衛和扎卡領銜的緊湊中場運作。他們聰明地吸收壓力，通過快速的邊路球員反擊。他們的賽事經驗使他們成為危險的淘汰賽對手。",
        },
        "strengths": [
            {"en": "Defensive organization", "簡中": "防守组织", "繁中": "防守組織"},
            {"en": "Xhaka's midfield control", "簡中": "扎卡的中场控制", "繁中": "扎卡的中場控制"},
            {"en": "Tournament pedigree", "簡中": "大赛底蕴", "繁中": "大賽底蘊"},
            {"en": "Set-piece threat", "簡中": "定位球威胁", "繁中": "定位球威脅"},
        ],
        "weaknesses": [
            {"en": "Lack of elite striker", "簡中": "缺乏顶级前锋", "繁中": "缺乏頂級前鋒"},
            {"en": "Occasional slow starts", "簡中": "偶尔慢热", "繁中": "偶爾慢熱"},
            {"en": "Limited bench impact", "簡中": "替补影响力有限", "繁中": "替補影響力有限"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 14,
        "elo_rating": 1830,
    },

    # ======================================================================
    # Group C
    # ======================================================================
    "Brazil": {
        "coach": {
            "name": "Dorival Junior",
            "nationality": "Brazilian",
            "age": 62,
            "style": "Attacking",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Vinicius Junior",
            "position": "LW",
            "nickname": {
                "en": "Vini",
                "簡中": "维尼",
                "繁中": "維尼",
            },
        },
        "strategy": {
            "en": "Brazil play with flair and attacking intent, using Vinicius' electrifying dribbling to destabilize defences. The midfield balances creativity with physicality, supporting relentless forward runs. Full-backs provide width and overlapping options in a trademark Brazilian style.",
            "簡中": "巴西以华丽和进攻意图踢球，利用维尼修斯令人惊叹的盘带瓦解防线。中场平衡创造力与身体对抗，支持持续的前插跑动。边后卫以典型的巴西风格提供宽度和套边选择。",
            "繁中": "巴西以華麗和進攻意圖踢球，利用維尼修斯令人驚嘆的盤帶瓦解防線。中場平衡創造力與身體對抗，支持持續的前插跑動。邊後衛以典型的巴西風格提供寬度和套邊選擇。",
        },
        "strengths": [
            {"en": "Individual attacking talent", "簡中": "个人进攻天赋", "繁中": "個人進攻天賦"},
            {"en": "Vinicius' dribbling and pace", "簡中": "维尼修斯的盘带和速度", "繁中": "維尼修斯的盤帶和速度"},
            {"en": "Full-back attacking quality", "簡中": "边后卫进攻质量", "繁中": "邊後衛進攻質量"},
            {"en": "Set-piece variety", "簡中": "定位球多样性", "繁中": "定位球多樣性"},
            {"en": "Squad depth", "簡中": "阵容深度", "繁中": "陣容深度"},
        ],
        "weaknesses": [
            {"en": "Defensive vulnerability in transitions", "簡中": "转换中防守脆弱", "繁中": "轉換中防守脆弱"},
            {"en": "Occasional lack of focus", "簡中": "偶尔注意力不集中", "繁中": "偶爾注意力不集中"},
            {"en": "Over-reliance on individual brilliance", "簡中": "过度依赖个人能力", "繁中": "過度依賴個人能力"},
        ],
        "style": "attacking_possession",
        "fifa_ranking": 5,
        "elo_rating": 1975,
    },

    "Morocco": {
        "coach": {
            "name": "Walid Regragui",
            "nationality": "Moroccan",
            "age": 49,
            "style": "Defensively solid",
        },
        "formation": "4-1-4-1",
        "main_player": {
            "name": "Achraf Hakimi",
            "position": "RB",
            "nickname": {
                "en": "Achraf",
                "簡中": "阿什拉夫",
                "繁中": "阿什拉夫",
            },
        },
        "strategy": {
            "en": "Morocco employ a compact defensive block with a dedicated holding midfielder shielding the back four. Hakimi provides an explosive outlet on the right flank during transitions. Their World Cup 2022 run proved their ability to frustrate elite teams and punish on the break.",
            "簡中": "摩洛哥采用紧凑的防守阵型，专职后腰保护后防线。哈基米在转换中从右路提供爆发性出口。他们2022年世界杯的表现证明了自己限制强队和反击得分的能力。",
            "繁中": "摩洛哥採用緊湊的防守陣型，專職後腰保護後防線。哈基米在轉換中從右路提供爆發性出口。他們2022年世界盃的表現證明了自己限制強隊和反擊得分的能力。",
        },
        "strengths": [
            {"en": "Defensive discipline", "簡中": "防守纪律", "繁中": "防守紀律"},
            {"en": "Hakimi's attacking runs from deep", "簡中": "哈基米后插上进攻", "繁中": "哈基米後插上進攻"},
            {"en": "Tournament experience", "簡中": "大赛经验", "繁中": "大賽經驗"},
            {"en": "Physical midfield", "簡中": "强壮的中场", "繁中": "強壯的中場"},
        ],
        "weaknesses": [
            {"en": "Limited attacking creativity", "簡中": "进攻创造力有限", "繁中": "進攻創造力有限"},
            {"en": "Struggle to break down low blocks", "簡中": "面对低位防守难以突破", "繁中": "面對低位防守難以突破"},
            {"en": "Over-reliance on transitions", "簡中": "过度依赖转换进攻", "繁中": "過度依賴轉換進攻"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 13,
        "elo_rating": 1780,
    },

    "Haiti": {
        "coach": {
            "name": "Sebastien Migne",
            "nationality": "French",
            "age": 52,
            "style": "Defensive",
        },
        "formation": "5-4-1",
        "main_player": {
            "name": "Duckens Nazon",
            "position": "ST",
            "nickname": {
                "en": "Duck",
                "簡中": "达克",
                "繁中": "達克",
            },
        },
        "strategy": {
            "en": "Haiti set up in a deep 5-4-1 block, looking to stay compact and frustrate opponents. Nazon provides a physical outlet on the counter with his hold-up play. They rely heavily on defensive resilience and set pieces to stay in matches.",
            "簡中": "海地采用深度5-4-1防守阵型，力求保持紧凑来限制对手。纳宗在反击中提供身体支点。他们严重依赖防守韧性和定位球来留在比赛中。",
            "繁中": "海地採用深度5-4-1防守陣型，力求保持緊湊來限制對手。納宗在反擊中提供身體支點。他們嚴重依賴防守韌性和定位球來留在比賽中。",
        },
        "strengths": [
            {"en": "Defensive commitment", "簡中": "防守投入", "繁中": "防守投入"},
            {"en": "Physicality", "簡中": "身体对抗", "繁中": "身體對抗"},
            {"en": "Counter-attacking potential", "簡中": "反击潜力", "繁中": "反擊潛力"},
        ],
        "weaknesses": [
            {"en": "Very limited technical quality", "簡中": "技术能力非常有限", "繁中": "技術能力非常有限"},
            {"en": "Poor ball retention", "簡中": "控球能力差", "繁中": "控球能力差"},
            {"en": "Lack of elite-level experience", "簡中": "缺乏顶级赛事经验", "繁中": "缺乏頂級賽事經驗"},
            {"en": "Shallow squad", "簡中": "阵容薄弱", "繁中": "陣容薄弱"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 42,
        "elo_rating": 1490,
    },

    "Scotland": {
        "coach": {
            "name": "Steve Clarke",
            "nationality": "Scottish",
            "age": 61,
            "style": "Organized",
        },
        "formation": "3-4-2-1",
        "main_player": {
            "name": "Andrew Robertson",
            "position": "LB",
            "nickname": {
                "en": "Robbo",
                "簡中": "罗伯逊",
                "繁中": "羅伯遜",
            },
        },
        "strategy": {
            "en": "Scotland use a back three with Robertson and a wing-back providing width on the left. They are well-organized defensively and look to capitalize on set pieces and crosses. Clarke's tactical discipline makes them hard to break down.",
            "簡中": "苏格兰使用三后卫，罗伯逊和左翼卫提供左侧宽度。他们防守组织严密，寻求利用定位球和传中得分。克拉克的战术纪律使他们难以被攻破。",
            "繁中": "蘇格蘭使用三後衛，羅伯遜和左翼衛提供左側寬度。他們防守組織嚴密，尋求利用定位球和傳中得分。克拉克的戰術紀律使他們難以被攻破。",
        },
        "strengths": [
            {"en": "Set-piece threat", "簡中": "定位球威胁", "繁中": "定位球威脅"},
            {"en": "Defensive organization", "簡中": "防守组织", "繁中": "防守組織"},
            {"en": "Robertson's leadership", "簡中": "罗伯逊的领导力", "繁中": "羅伯遜的領導力"},
        ],
        "weaknesses": [
            {"en": "Lack of elite attacking talent", "簡中": "缺乏顶级进攻人才", "繁中": "缺乏頂級進攻人才"},
            {"en": "Limited ball progression", "簡中": "推进能力有限", "繁中": "推進能力有限"},
            {"en": "Struggle against possession teams", "簡中": "面对控球型球队吃力", "繁中": "面對控球型球隊吃力"},
            {"en": "Goalkeeping inconsistency", "簡中": "门将不稳定", "繁中": "門將不穩定"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 33,
        "elo_rating": 1620,
    },

    # ======================================================================
    # Group D
    # ======================================================================
    "USA": {
        "coach": {
            "name": "Mauricio Pochettino",
            "nationality": "Argentine",
            "age": 53,
            "style": "High pressing",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Christian Pulisic",
            "position": "LW",
            "nickname": {
                "en": "Captain America",
                "簡中": "美国队长",
                "繁中": "美國隊長",
            },
        },
        "strategy": {
            "en": "The USA blend positional play with high-energy pressing, using Pulisic's creativity as the primary attacking weapon. The midfield trio balances ball retention with forward runs. Home advantage in 2026 adds an extra dimension to their performance.",
            "簡中": "美国将位置进攻与高能逼抢相结合，以普利西奇的创造力作为主要进攻武器。三中场平衡控球与前插跑动。2026年主场优势为他们的表现增添了额外维度。",
            "繁中": "美國將位置進攻與高能逼搶相結合，以普利西奇的創造力作為主要進攻武器。三中場平衡控球與前插跑動。2026年主場優勢為他們的表現增添了額外維度。",
        },
        "strengths": [
            {"en": "Pulisic's dribbling and vision", "簡中": "普利西奇的盘带和视野", "繁中": "普利西奇的盤帶和視野"},
            {"en": "Athleticism across the pitch", "簡中": "全场运动能力", "繁中": "全場運動能力"},
            {"en": "Home advantage", "簡中": "主场优势", "繁中": "主場優勢"},
            {"en": "Young talented core", "簡中": "年轻有才华的核心", "繁中": "年輕有才華的核心"},
        ],
        "weaknesses": [
            {"en": "Striker position weakness", "簡中": "前锋位置薄弱", "繁中": "前鋒位置薄弱"},
            {"en": "Defensive lapses", "簡中": "防守失误", "繁中": "防守失誤"},
            {"en": "Inconsistent against top teams", "簡中": "对阵强队不稳定", "繁中": "對陣強隊不穩定"},
        ],
        "style": "balanced",
        "fifa_ranking": 16,
        "elo_rating": 1810,
    },

    "Paraguay": {
        "coach": {
            "name": "Gustavo Alfaro",
            "nationality": "Argentine",
            "age": 62,
            "style": "Defensive",
        },
        "formation": "4-4-2",
        "main_player": {
            "name": "Miguel Almiron",
            "position": "RW",
            "nickname": {
                "en": "Miggy",
                "簡中": "米吉",
                "繁中": "米吉",
            },
        },
        "strategy": {
            "en": "Paraguay prioritize defensive solidity in a compact 4-4-2, with Almiron providing the main counter-attacking threat. They are tough to break down and dangerous from set pieces. Alfaro's pragmatic approach maximizes limited resources.",
            "簡中": "巴拉圭在紧凑的4-4-2中优先考虑防守稳固，阿尔米隆提供主要的反击威胁。他们难以被攻破，定位球很有威胁。阿尔法罗的务实方法最大化了有限资源。",
            "繁中": "巴拉圭在緊湊的4-4-2中優先考慮防守穩固，阿爾米隆提供主要的反擊威脅。他們難以被攻破，定位球很有威脅。阿爾法羅的務實方法最大化了有限資源。",
        },
        "strengths": [
            {"en": "Defensive discipline", "簡中": "防守纪律", "繁中": "防守紀律"},
            {"en": "Almiron's pace on the break", "簡中": "阿尔米隆的反击速度", "繁中": "阿爾米隆的反擊速度"},
            {"en": "Set-piece threat", "簡中": "定位球威胁", "繁中": "定位球威脅"},
        ],
        "weaknesses": [
            {"en": "Limited attacking depth", "簡中": "进攻深度有限", "繁中": "進攻深度有限"},
            {"en": "Lack of creative midfielders", "簡中": "缺乏创造性中场", "繁中": "缺乏創造性中場"},
            {"en": "Struggle to retain possession", "簡中": "控球困难", "繁中": "控球困難"},
            {"en": "Goal-scoring inconsistency", "簡中": "进球不稳定", "繁中": "進球不穩定"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 34,
        "elo_rating": 1650,
    },

    "Australia": {
        "coach": {
            "name": "Tony Popovic",
            "nationality": "Australian",
            "age": 52,
            "style": "Organized",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Mathew Leckie",
            "position": "RW",
            "nickname": {
                "en": "Lecks",
                "簡中": "莱基",
                "繁中": "萊基",
            },
        },
        "strategy": {
            "en": "Australia play a structured 4-2-3-1 with emphasis on defensive shape and organized pressing. They use the flanks for counter-attacks and rely on set pieces for goals. Their fighting spirit and physicality make them competitive against stronger sides.",
            "簡中": "澳大利亚踢结构化的4-2-3-1，强调防守阵型和有组织的逼抢。他们利用边路反击，依靠定位球进球。他们的战斗精神和身体对抗使他们在面对强队时具有竞争力。",
            "繁中": "澳大利亞踢結構化的4-2-3-1，強調防守陣型和有組織的逼搶。他們利用邊路反擊，依靠定位球進球。他們的戰鬥精神和身體對抗使他們在面對強隊時具有競爭力。",
        },
        "strengths": [
            {"en": "Physical resilience", "簡中": "身体韧性", "繁中": "身體韌性"},
            {"en": "Set-piece threat", "簡中": "定位球威胁", "繁中": "定位球威脅"},
            {"en": "Team spirit and work rate", "簡中": "团队精神和跑动", "繁中": "團隊精神和跑動"},
        ],
        "weaknesses": [
            {"en": "Limited technical quality", "簡中": "技术能力有限", "繁中": "技術能力有限"},
            {"en": "Lack of elite-level attackers", "簡中": "缺乏顶级攻击手", "繁中": "缺乏頂級攻擊手"},
            {"en": "Vulnerable against possession teams", "簡中": "面对控球型球队脆弱", "繁中": "面對控球型球隊脆弱"},
            {"en": "Squad depth issues", "簡中": "阵容深度问题", "繁中": "陣容深度問題"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 27,
        "elo_rating": 1760,
    },

    "Turkey": {
        "coach": {
            "name": "Vincenzo Montella",
            "nationality": "Italian",
            "age": 50,
            "style": "Attacking",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Hakan Calhanoglu",
            "position": "CM",
            "nickname": {
                "en": "Hakan",
                "簡中": "恰尔汗奥卢",
                "繁中": "恰爾汗奧盧",
            },
        },
        "strategy": {
            "en": "Turkey play with attacking intent, using Calhanoglu's passing range and dead-ball ability as the creative fulcrum. The wide players cut inside to create overloads while full-backs push high. They can be devastating going forward but sometimes leave gaps at the back.",
            "簡中": "土耳其以进攻意图踢球，利用恰尔汗奥卢的传球范围和定位球能力作为创造核心。边路球员内切创造人数优势，边后卫高位压上。他们进攻端极具威胁，但有时后防留有空隙。",
            "繁中": "土耳其以進攻意圖踢球，利用恰爾汗奧盧的傳球範圍和定位球能力作為創造核心。邊路球員內切創造人數優勢，邊後衛高位壓上。他們進攻端極具威脅，但有時後防留有空隙。",
        },
        "strengths": [
            {"en": "Calhanoglu's set-piece mastery", "簡中": "恰尔汗奥卢的定位球绝技", "繁中": "恰爾汗奧盧的定位球絕技"},
            {"en": "Attacking flair", "簡中": "进攻天赋", "繁中": "進攻天賦"},
            {"en": "Passionate playing style", "簡中": "充满激情的踢法", "繁中": "充滿激情的踢法"},
            {"en": "Technical midfield", "簡中": "技术型中场", "繁中": "技術型中場"},
        ],
        "weaknesses": [
            {"en": "Defensive inconsistency", "簡中": "防守不稳定", "繁中": "防守不穩定"},
            {"en": "Prone to emotional lapses", "簡中": "容易情绪化失误", "繁中": "容易情緒化失誤"},
            {"en": "Vulnerable on transitions", "簡中": "转换中脆弱", "繁中": "轉換中脆弱"},
        ],
        "style": "attacking_possession",
        "fifa_ranking": 22,
        "elo_rating": 1750,
    },

    # ======================================================================
    # Group E
    # ======================================================================
    "Germany": {
        "coach": {
            "name": "Julian Nagelsmann",
            "nationality": "German",
            "age": 37,
            "style": "Tactical innovator",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Jamal Musiala",
            "position": "AM",
            "nickname": {
                "en": "Bambi",
                "簡中": "斑比",
                "繁中": "斑比",
            },
        },
        "strategy": {
            "en": "Germany under Nagelsmann blend positional play with fluid attacking movements, using Musiala's dribbling as the primary creative outlet. The double pivot provides stability while full-backs invert to create overloads in midfield. Their tactical flexibility allows multiple in-game adjustments.",
            "簡中": "纳格尔斯曼麾下的德国将位置进攻与流畅的攻击跑动相结合，以穆西亚拉的盘带作为主要创造手段。双后腰提供稳定性，边后卫内收在中场创造人数优势。他们的战术灵活性允许多种赛中调整。",
            "繁中": "納格爾斯曼麾下的德國將位置進攻與流暢的攻擊跑動相結合，以穆西亞拉的盤帶作為主要創造手段。雙後腰提供穩定性，邊後衛內收在中場創造人數優勢。他們的戰術靈活性允許多種賽中調整。",
        },
        "strengths": [
            {"en": "Musiala's dribbling and creativity", "簡中": "穆西亚拉的盘带和创造力", "繁中": "穆西亞拉的盤帶和創造力"},
            {"en": "Tactical flexibility", "簡中": "战术灵活性", "繁中": "戰術靈活性"},
            {"en": "Set-piece threat", "簡中": "定位球威胁", "繁中": "定位球威脅"},
            {"en": "Squad depth and versatility", "簡中": "阵容深度和多面性", "繁中": "陣容深度和多面性"},
            {"en": "Midfield control", "簡中": "中场控制力", "繁中": "中場控制力"},
        ],
        "weaknesses": [
            {"en": "Striker conversion rate", "簡中": "前锋转化率", "繁中": "前鋒轉化率"},
            {"en": "Occasional defensive lapses", "簡中": "偶尔防守失误", "繁中": "偶爾防守失誤"},
            {"en": "Pressure in knockout games", "簡中": "淘汰赛压力", "繁中": "淘汰賽壓力"},
        ],
        "style": "attacking_possession",
        "fifa_ranking": 8,
        "elo_rating": 1940,
    },

    "Curacao": {
        "coach": {
            "name": "Dick Advocaat",
            "nationality": "Dutch",
            "age": 78,
            "style": "Pragmatic",
        },
        "formation": "5-3-2",
        "main_player": {
            "name": "Leandro Bacuna",
            "position": "MF",
            "nickname": {
                "en": "Bacu",
                "簡中": "巴库纳",
                "繁中": "巴庫納",
            },
        },
        "strategy": {
            "en": "Curacao operate in a deep 5-3-2, prioritizing defensive compactness above all else. Bacuna provides the main creative spark from midfield with his passing range. They look to frustrate opponents and snatch goals from set pieces or counter-attacks.",
            "簡中": "库拉索采用深度5-3-2阵型，将防守紧凑性置于首位。巴库纳凭借传球范围从中场提供主要创造火花。他们力求限制对手，从定位球或反击中偷取进球。",
            "繁中": "庫拉索採用深度5-3-2陣型，將防守緊湊性置於首位。巴庫納憑藉傳球範圍從中場提供主要創造火花。他們力求限制對手，從定位球或反擊中偷取進球。",
        },
        "strengths": [
            {"en": "Defensive commitment", "簡中": "防守投入", "繁中": "防守投入"},
            {"en": "Set-piece organization", "簡中": "定位球组织", "繁中": "定位球組織"},
            {"en": "Team spirit", "簡中": "团队精神", "繁中": "團隊精神"},
        ],
        "weaknesses": [
            {"en": "Very limited technical depth", "簡中": "技术深度非常有限", "繁中": "技術深度非常有限"},
            {"en": "Lack of elite-level players", "簡中": "缺乏顶级球员", "繁中": "缺乏頂級球員"},
            {"en": "Poor ball retention", "簡中": "控球能力差", "繁中": "控球能力差"},
            {"en": "Vulnerable against quality opposition", "簡中": "面对强队脆弱", "繁中": "面對強隊脆弱"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 46,
        "elo_rating": 1460,
    },

    "Ivory Coast": {
        "coach": {
            "name": "Emerse Fae",
            "nationality": "Ivorian",
            "age": 41,
            "style": "Balanced",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Seko Fofana",
            "position": "CM",
            "nickname": {
                "en": "Seko",
                "簡中": "塞科",
                "繁中": "塞科",
            },
        },
        "strategy": {
            "en": "Ivory Coast blend physical power with technical ability in a balanced 4-3-3. Fofana drives the team forward from midfield with his box-to-box energy. They are strong in transitions and dangerous from wide areas, though defensive organization can waver.",
            "簡中": "科特迪瓦在平衡的4-3-3中融合身体力量与技术能力。福法纳以全能中场的能量从中场驱动球队前进。他们在转换中很强，边路很有威胁，但防守组织可能波动。",
            "繁中": "科特迪瓦在平衡的4-3-3中融合身體力量與技術能力。福法納以全能中場的能量從中場驅動球隊前進。他們在轉換中很強，邊路很有威脅，但防守組織可能波動。",
        },
        "strengths": [
            {"en": "Physical athleticism", "簡中": "身体运动能力", "繁中": "身體運動能力"},
            {"en": "Fofana's midfield drive", "簡中": "福法纳的中场推进", "繁中": "福法納的中場推進"},
            {"en": "Wide attacking options", "簡中": "边路进攻选择", "繁中": "邊路進攻選擇"},
            {"en": "AFCON-winning confidence", "簡中": "非洲杯冠军信心", "繁中": "非洲盃冠軍信心"},
        ],
        "weaknesses": [
            {"en": "Defensive lapses in transition", "簡中": "转换中防守失误", "繁中": "轉換中防守失誤"},
            {"en": "Inconsistent goalkeeping", "簡中": "门将不稳定", "繁中": "門將不穩定"},
            {"en": "Occasional tactical indiscipline", "簡中": "偶尔战术纪律松散", "繁中": "偶爾戰術紀律鬆散"},
        ],
        "style": "balanced",
        "fifa_ranking": 29,
        "elo_rating": 1700,
    },

    "Ecuador": {
        "coach": {
            "name": "Sebastian Beccacece",
            "nationality": "Argentine",
            "age": 44,
            "style": "Intense pressing",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Moises Caicedo",
            "position": "CM",
            "nickname": {
                "en": "Moises",
                "簡中": "莫伊塞斯",
                "繁中": "莫伊塞斯",
            },
        },
        "strategy": {
            "en": "Ecuador play with high intensity and aggressive pressing, using Caicedo as the midfield anchor who initiates attacks. The wide players provide pace and directness while the double pivot ensures defensive coverage. Their high-altitude conditioning gives them a stamina edge.",
            "簡中": "厄瓜多尔以高强度和积极逼抢踢球，以凯塞多作为发起进攻的中场锚点。边路球员提供速度和直接性，双后腰确保防守覆盖。他们的高原训练赋予他们体能优势。",
            "繁中": "厄瓜多爾以高強度和積極逼搶踢球，以凱塞多作為發起進攻的中場錨點。邊路球員提供速度和直接性，雙後腰確保防守覆蓋。他們的高原訓練賦予他們體能優勢。",
        },
        "strengths": [
            {"en": "Caicedo's midfield dominance", "簡中": "凯塞多的中场统治", "繁中": "凱塞多的中場統治"},
            {"en": "Pressing intensity", "簡中": "逼抢强度", "繁中": "逼搶強度"},
            {"en": "Physical stamina", "簡中": "体能耐力", "繁中": "體能耐力"},
            {"en": "Pace on the flanks", "簡中": "边路速度", "繁中": "邊路速度"},
        ],
        "weaknesses": [
            {"en": "Lack of elite striker", "簡中": "缺乏顶级前锋", "繁中": "缺乏頂級前鋒"},
            {"en": "Defensive lapses under sustained pressure", "簡中": "持续压力下防守失误", "繁中": "持續壓力下防守失誤"},
            {"en": "Limited creative options", "簡中": "创造力选择有限", "繁中": "創造力選擇有限"},
        ],
        "style": "balanced",
        "fifa_ranking": 24,
        "elo_rating": 1710,
    },

    # ======================================================================
    # Group F
    # ======================================================================
    "Netherlands": {
        "coach": {
            "name": "Ronald Koeman",
            "nationality": "Dutch",
            "age": 61,
            "style": "Attacking",
        },
        "formation": "3-4-3",
        "main_player": {
            "name": "Virgil van Dijk",
            "position": "CB",
            "nickname": {
                "en": "VVD",
                "簡中": "范戴克",
                "繁中": "范戴克",
            },
        },
        "strategy": {
            "en": "The Netherlands employ their trademark 3-4-3 with Van Dijk marshalling the defence and initiating attacks from deep. The wing-backs provide width while the front three rotate fluidly. Koeman's side balances defensive solidity with attacking ambition in classic Dutch fashion.",
            "簡中": "荷兰采用标志性的3-4-3阵型，范戴克统领防线并从后场发起进攻。翼卫提供宽度，前场三人组灵活轮转。科曼的球队以经典荷兰方式平衡防守稳固与进攻雄心。",
            "繁中": "荷蘭採用標誌性的3-4-3陣型，范戴克統領防線並從後場發起進攻。翼衛提供寬度，前場三人組靈活輪轉。科曼的球隊以經典荷蘭方式平衡防守穩固與進攻雄心。",
        },
        "strengths": [
            {"en": "Van Dijk's defensive leadership", "簡中": "范戴克的防守领导力", "繁中": "范戴克的防守領導力"},
            {"en": "Attacking width from wing-backs", "簡中": "翼卫进攻宽度", "繁中": "翼衛進攻寬度"},
            {"en": "Set-piece threat", "簡中": "定位球威胁", "繁中": "定位球威脅"},
            {"en": "Tactical tradition and flexibility", "簡中": "战术传统和灵活性", "繁中": "戰術傳統和靈活性"},
            {"en": "Technical midfield", "簡中": "技术型中场", "繁中": "技術型中場"},
        ],
        "weaknesses": [
            {"en": "Goalkeeping inconsistency", "簡中": "门将不稳定", "繁中": "門將不穩定"},
            {"en": "Occasional defensive lapses in transition", "簡中": "转换中偶尔防守失误", "繁中": "轉換中偶爾防守失誤"},
            {"en": "Striker position uncertainty", "簡中": "前锋位置不确定", "繁中": "前鋒位置不確定"},
        ],
        "style": "attacking_possession",
        "fifa_ranking": 7,
        "elo_rating": 1930,
    },

    "Japan": {
        "coach": {
            "name": "Hajime Moriyasu",
            "nationality": "Japanese",
            "age": 56,
            "style": "Disciplined",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Takefusa Kubo",
            "position": "RW",
            "nickname": {
                "en": "Take",
                "簡中": "久保",
                "繁中": "久保",
            },
        },
        "strategy": {
            "en": "Japan combine tactical discipline with technical quality, using Kubo's dribbling as a key creative weapon. The double pivot provides structure while the attacking midfielders rotate to find space. They are dangerous on the counter and well-organized at set pieces.",
            "簡中": "日本将战术纪律与技术能力相结合，以久保建英的盘带作为关键创造武器。双后腰提供结构，攻击型中场轮转寻找空间。他们反击很有威胁，定位球组织严密。",
            "繁中": "日本將戰術紀律與技術能力相結合，以久保建英的盤帶作為關鍵創造武器。雙後腰提供結構，攻擊型中場輪轉尋找空間。他們反擊很有威脅，定位球組織嚴密。",
        },
        "strengths": [
            {"en": "Technical quality across the pitch", "簡中": "全场技术能力", "繁中": "全場技術能力"},
            {"en": "Kubo's creativity", "簡中": "久保建英的创造力", "繁中": "久保建英的創造力"},
            {"en": "Tactical discipline", "簡中": "战术纪律", "繁中": "戰術紀律"},
            {"en": "Counter-attacking precision", "簡中": "反击精准度", "繁中": "反擊精準度"},
        ],
        "weaknesses": [
            {"en": "Physical disadvantage against stronger teams", "簡中": "面对强壮球队身体劣势", "繁中": "面對強壯球隊身體劣勢"},
            {"en": "Lack of elite striker", "簡中": "缺乏顶级前锋", "繁中": "缺乏頂級前鋒"},
            {"en": "Set-piece defending", "簡中": "定位球防守", "繁中": "定位球防守"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 18,
        "elo_rating": 1790,
    },

    "Sweden": {
        "coach": {
            "name": "Jon Dahl Tomasson",
            "nationality": "Danish",
            "age": 48,
            "style": "Balanced",
        },
        "formation": "4-4-2",
        "main_player": {
            "name": "Dejan Kulusevski",
            "position": "RW",
            "nickname": {
                "en": "Deki",
                "簡中": "德基",
                "繁中": "德基",
            },
        },
        "strategy": {
            "en": "Sweden play a balanced 4-4-2 with Kulusevski providing the main creative spark from the right flank. They are organized defensively and dangerous from set pieces with their physical presence. The forward pairing combines physicality with intelligent movement.",
            "簡中": "瑞典踢平衡的4-4-2，库卢塞夫斯基从右路提供主要创造火花。他们防守有序，凭借身体优势在定位球上很有威胁。前锋搭档结合身体对抗和聪明跑位。",
            "繁中": "瑞典踢平衡的4-4-2，庫盧塞夫斯基從右路提供主要創造火花。他們防守有序，憑藉身體優勢在定位球上很有威脅。前鋒搭檔結合身體對抗和聰明跑位。",
        },
        "strengths": [
            {"en": "Kulusevski's creativity", "簡中": "库卢塞夫斯基的创造力", "繁中": "庫盧塞夫斯基的創造力"},
            {"en": "Set-piece threat", "簡中": "定位球威胁", "繁中": "定位球威脅"},
            {"en": "Physical presence", "簡中": "身体优势", "繁中": "身體優勢"},
            {"en": "Defensive organization", "簡中": "防守组织", "繁中": "防守組織"},
        ],
        "weaknesses": [
            {"en": "Lack of pace in defence", "簡中": "后防速度不足", "繁中": "後防速度不足"},
            {"en": "Limited midfield creativity beyond Kulusevski", "簡中": "库卢之外中场创造力有限", "繁中": "庫盧之外中場創造力有限"},
            {"en": "Struggle against high press", "簡中": "怕高位逼抢", "繁中": "怕高位逼搶"},
        ],
        "style": "balanced",
        "fifa_ranking": 30,
        "elo_rating": 1730,
    },

    "Tunisia": {
        "coach": {
            "name": "Faouzi Benzarti",
            "nationality": "Tunisian",
            "age": 74,
            "style": "Defensive",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Youssef Msakni",
            "position": "LW",
            "nickname": {
                "en": "Youssef",
                "簡中": "优素福",
                "繁中": "優素福",
            },
        },
        "strategy": {
            "en": "Tunisia set up in a compact 4-3-3 focused on defensive solidity and rapid transitions. Msakni is the primary creative outlet with his dribbling and experience. They are difficult to break down but struggle to create chances against organized defences.",
            "簡中": "突尼斯以紧凑的4-3-3阵型专注于防守稳固和快速转换。姆萨克尼凭借盘带和经验是主要的创造出口。他们难以被攻破，但面对有组织的防守时难以创造机会。",
            "繁中": "突尼斯以緊湊的4-3-3陣型專注於防守穩固和快速轉換。姆薩克尼憑藉盤帶和經驗是主要的創造出口。他們難以被攻破，但面對有組織的防守時難以創造機會。",
        },
        "strengths": [
            {"en": "Defensive organization", "簡中": "防守组织", "繁中": "防守組織"},
            {"en": "Msakni's dribbling", "簡中": "姆萨克尼的盘带", "繁中": "姆薩克尼的盤帶"},
            {"en": "Counter-attacking speed", "簡中": "反击速度", "繁中": "反擊速度"},
        ],
        "weaknesses": [
            {"en": "Limited attacking depth", "簡中": "进攻深度有限", "繁中": "進攻深度有限"},
            {"en": "Struggle to break down low blocks", "簡中": "面对低位防守难以突破", "繁中": "面對低位防守難以突破"},
            {"en": "Lack of elite-level players", "簡中": "缺乏顶级球员", "繁中": "缺乏頂級球員"},
            {"en": "Goal-scoring inconsistency", "簡中": "进球不稳定", "繁中": "進球不穩定"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 32,
        "elo_rating": 1580,
    },

    # ======================================================================
    # Group G
    # ======================================================================
    "Belgium": {
        "coach": {
            "name": "Domenico Tedesco",
            "nationality": "Italian-German",
            "age": 39,
            "style": "Attacking",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Kevin De Bruyne",
            "position": "AM",
            "nickname": {
                "en": "KDB",
                "簡中": "德布劳内",
                "繁中": "德布勞內",
            },
        },
        "strategy": {
            "en": "Belgium revolve around De Bruyne's world-class passing and vision in a fluid 4-2-3-1. The wide attackers cut inside to create overloads while full-backs provide width. Tedesco has added more pressing intensity to complement their natural attacking quality.",
            "簡中": "比利时围绕德布劳内世界级的传球和视野在流畅的4-2-3-1中运作。边路攻击手内切创造人数优势，边后卫提供宽度。特德斯科增加了更多逼抢强度来补充他们天然的进攻质量。",
            "繁中": "比利時圍繞德布勞內世界級的傳球和視野在流暢的4-2-3-1中運作。邊路攻擊手內切創造人數優勢，邊後衛提供寬度。特德斯科增加了更多逼搶強度來補充他們天然的進攻質量。",
        },
        "strengths": [
            {"en": "De Bruyne's passing and creativity", "簡中": "德布劳内的传球和创造力", "繁中": "德布勞內的傳球和創造力"},
            {"en": "Attacking depth", "簡中": "进攻深度", "繁中": "進攻深度"},
            {"en": "Technical quality across the pitch", "簡中": "全场技术质量", "繁中": "全場技術質量"},
            {"en": "Set-piece delivery", "簡中": "定位球传中", "繁中": "定位球傳中"},
        ],
        "weaknesses": [
            {"en": "Aging defensive core", "簡中": "防守核心老化", "繁中": "防守核心老化"},
            {"en": "Transition vulnerability", "簡中": "转换中脆弱", "繁中": "轉換中脆弱"},
            {"en": "Over-reliance on De Bruyne", "簡中": "过度依赖德布劳内", "繁中": "過度依賴德布勞內"},
        ],
        "style": "attacking_possession",
        "fifa_ranking": 9,
        "elo_rating": 1910,
    },

    "Egypt": {
        "coach": {
            "name": "Hossam Hassan",
            "nationality": "Egyptian",
            "age": 59,
            "style": "Pragmatic",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Mohamed Salah",
            "position": "RW",
            "nickname": {
                "en": "Mo",
                "簡中": "莫萨拉赫",
                "繁中": "莫薩拉赫",
            },
        },
        "strategy": {
            "en": "Egypt build their entire attacking strategy around Salah's world-class ability to cut inside and score or assist. The double pivot protects the back four while the team stays compact and looks to release Salah on the break. They are dangerous from set pieces with Salah's delivery.",
            "簡中": "埃及围绕萨拉赫世界级的内切射门和助攻能力构建整个进攻策略。双后腰保护后防线，球队保持紧凑并寻求在反击中释放萨拉赫。萨拉赫的定位球传中使他们在定位球上很有威胁。",
            "繁中": "埃及圍繞薩拉赫世界級的內切射門和助攻能力構建整個進攻策略。雙後腰保護後防線，球隊保持緊湊並尋求在反擊中釋放薩拉赫。薩拉赫的定位球傳中使他們在定位球上很有威脅。",
        },
        "strengths": [
            {"en": "Salah's individual brilliance", "簡中": "萨拉赫的个人能力", "繁中": "薩拉赫的個人能力"},
            {"en": "Counter-attacking threat", "簡中": "反击威胁", "繁中": "反擊威脅"},
            {"en": "Set-piece delivery", "簡中": "定位球传中", "繁中": "定位球傳中"},
            {"en": "Defensive discipline", "簡中": "防守纪律", "繁中": "防守紀律"},
        ],
        "weaknesses": [
            {"en": "Over-reliance on Salah", "簡中": "过度依赖萨拉赫", "繁中": "過度依賴薩拉赫"},
            {"en": "Limited attacking alternatives", "簡中": "进攻选择有限", "繁中": "進攻選擇有限"},
            {"en": "Midfield creativity gaps", "簡中": "中场创造力不足", "繁中": "中場創造力不足"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 28,
        "elo_rating": 1640,
    },

    "Iran": {
        "coach": {
            "name": "Amir Ghalenoei",
            "nationality": "Iranian",
            "age": 62,
            "style": "Defensive",
        },
        "formation": "4-1-4-1",
        "main_player": {
            "name": "Sardar Azmoun",
            "position": "ST",
            "nickname": {
                "en": "Iranian Messi",
                "簡中": "伊朗梅西",
                "繁中": "伊朗梅西",
            },
        },
        "strategy": {
            "en": "Iran play with a deep defensive block and a dedicated holding midfielder, looking to absorb pressure and counter through Azmoun's movement. They are physical and organized, making them difficult opponents for teams that struggle to break down low blocks.",
            "簡中": "伊朗采用深度防守阵型和专职后腰，力求吸收压力后通过阿兹蒙的跑位反击。他们身体强壮、组织有序，使那些难以攻破低位防守的球队感到棘手。",
            "繁中": "伊朗採用深度防守陣型和專職後腰，力求吸收壓力後通過阿茲蒙的跑位反擊。他們身體強壯、組織有序，使那些難以攻破低位防守的球隊感到棘手。",
        },
        "strengths": [
            {"en": "Defensive discipline", "簡中": "防守纪律", "繁中": "防守紀律"},
            {"en": "Azmoun's finishing", "簡中": "阿兹蒙的射门", "繁中": "阿茲蒙的射門"},
            {"en": "Physical presence", "簡中": "身体优势", "繁中": "身體優勢"},
        ],
        "weaknesses": [
            {"en": "Limited technical quality in midfield", "簡中": "中场技术能力有限", "繁中": "中場技術能力有限"},
            {"en": "Struggle to retain possession", "簡中": "控球困难", "繁中": "控球困難"},
            {"en": "Lack of creative players", "簡中": "缺乏创造型球员", "繁中": "缺乏創造型球員"},
            {"en": "Vulnerable to pace in wide areas", "簡中": "边路怕速度", "繁中": "邊路怕速度"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 20,
        "elo_rating": 1590,
    },

    "New Zealand": {
        "coach": {
            "name": "Darren Bazeley",
            "nationality": "English",
            "age": 53,
            "style": "Organized",
        },
        "formation": "4-4-2",
        "main_player": {
            "name": "Chris Wood",
            "position": "ST",
            "nickname": {
                "en": "Woody",
                "簡中": "伍迪",
                "繁中": "伍迪",
            },
        },
        "strategy": {
            "en": "New Zealand play a direct 4-4-2 built around Wood's aerial ability and hold-up play. They are physical and organized, looking to compete on set pieces and crosses. Their pragmatic approach maximizes limited technical resources.",
            "簡中": "新西兰踢直接的4-4-2，围绕伍德的空中能力和支点作用。他们身体强壮、组织有序，寻求在定位球和传中上竞争。他们的务实方法最大化了有限的技术资源。",
            "繁中": "新西蘭踢直接的4-4-2，圍繞伍德的空中能力和支點作用。他們身體強壯、組織有序，尋求在定位球和傳中上競爭。他們的務實方法最大化了有限的技術資源。",
        },
        "strengths": [
            {"en": "Wood's aerial threat", "簡中": "伍德的空中威胁", "繁中": "伍德的空中威脅"},
            {"en": "Physical presence", "簡中": "身体优势", "繁中": "身體優勢"},
            {"en": "Set-piece organization", "簡中": "定位球组织", "繁中": "定位球組織"},
        ],
        "weaknesses": [
            {"en": "Very limited technical quality", "簡中": "技术能力非常有限", "繁中": "技術能力非常有限"},
            {"en": "Lack of pace in defence", "簡中": "后防速度不足", "繁中": "後防速度不足"},
            {"en": "Poor ball retention", "簡中": "控球能力差", "繁中": "控球能力差"},
            {"en": "Shallow talent pool", "簡中": "人才储备浅", "繁中": "人才儲備淺"},
        ],
        "style": "balanced",
        "fifa_ranking": 43,
        "elo_rating": 1500,
    },

    # ======================================================================
    # Group H
    # ======================================================================
    "Spain": {
        "coach": {
            "name": "Luis de la Fuente",
            "nationality": "Spanish",
            "age": 63,
            "style": "Possession-based",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Rodri",
            "position": "CM",
            "nickname": {
                "en": "The Engine",
                "簡中": "引擎",
                "繁中": "引擎",
            },
        },
        "strategy": {
            "en": "Spain dominate possession through their technically gifted midfield, with Rodri as the metronome controlling tempo. The wingers provide width and cutting-edge while the full-backs invert to create midfield overloads. De la Fuente has added more directness to the traditional tiki-taka approach.",
            "簡中": "西班牙通过技术精湛的中场控制球权，罗德里作为节拍器控制节奏。边锋提供宽度和杀伤力，边后卫内收创造中场人数优势。德拉富恩特在传统蒂基塔卡基础上增加了更多直接性。",
            "繁中": "西班牙通過技術精湛的中場控制球權，羅德里作為節拍器控制節奏。邊鋒提供寬度和殺傷力，邊後衛內收創造中場人數優勢。德拉富恩特在傳統蒂基塔卡基礎上增加了更多直接性。",
        },
        "strengths": [
            {"en": "Midfield dominance and possession", "簡中": "中场统治和控球", "繁中": "中場統治和控球"},
            {"en": "Rodri's control and passing", "簡中": "罗德里的控制和传球", "繁中": "羅德里的控制和傳球"},
            {"en": "Technical quality across the pitch", "簡中": "全场技术质量", "繁中": "全場技術質量"},
            {"en": "Set-piece delivery", "簡中": "定位球传中", "繁中": "定位球傳中"},
            {"en": "Squad depth", "簡中": "阵容深度", "繁中": "陣容深度"},
        ],
        "weaknesses": [
            {"en": "Occasionally too passive in attack", "簡中": "进攻中偶尔过于被动", "繁中": "進攻中偶爾過於被動"},
            {"en": "Vulnerable to rapid transitions", "簡中": "面对快速转换脆弱", "繁中": "面對快速轉換脆弱"},
            {"en": "Striker position less prolific", "簡中": "前锋位置进球率偏低", "繁中": "前鋒位置進球率偏低"},
        ],
        "style": "attacking_possession",
        "fifa_ranking": 2,
        "elo_rating": 2050,
    },

    "Cape Verde": {
        "coach": {
            "name": "Bubista",
            "nationality": "Cape Verdean",
            "age": 53,
            "style": "Organized",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Ryan Mendes",
            "position": "LW",
            "nickname": {
                "en": "Ryan",
                "簡中": "瑞恩",
                "繁中": "瑞恩",
            },
        },
        "strategy": {
            "en": "Cape Verde play an organized 4-3-3 with Mendes providing the main attacking threat from the left. They combine Portuguese-influenced technical ability with African physicality. Their compact shape makes them difficult to break down.",
            "簡中": "佛得角踢有组织的4-3-3，门德斯从左路提供主要进攻威胁。他们结合了受葡萄牙影响的技术能力和非洲身体对抗。他们紧凑的阵型使其难以被攻破。",
            "繁中": "佛得角踢有組織的4-3-3，門德斯從左路提供主要進攻威脅。他們結合了受葡萄牙影響的技術能力和非洲身體對抗。他們緊湊的陣型使其難以被攻破。",
        },
        "strengths": [
            {"en": "Technical ability", "簡中": "技术能力", "繁中": "技術能力"},
            {"en": "Mendes' dribbling", "簡中": "门德斯的盘带", "繁中": "門德斯的盤帶"},
            {"en": "Organized defensive shape", "簡中": "有序的防守阵型", "繁中": "有序的防守陣型"},
        ],
        "weaknesses": [
            {"en": "Limited squad depth", "簡中": "阵容深度有限", "繁中": "陣容深度有限"},
            {"en": "Lack of elite-level experience", "簡中": "缺乏顶级赛事经验", "繁中": "缺乏頂級賽事經驗"},
            {"en": "Goalkeeping concerns", "簡中": "门将问题", "繁中": "門將問題"},
            {"en": "Struggle against physical teams", "簡中": "面对身体型球队吃力", "繁中": "面對身體型球隊吃力"},
        ],
        "style": "balanced",
        "fifa_ranking": 47,
        "elo_rating": 1470,
    },

    "Saudi Arabia": {
        "coach": {
            "name": "Roberto Mancini",
            "nationality": "Italian",
            "age": 60,
            "style": "Defensive",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Salem Al-Dawsari",
            "position": "LW",
            "nickname": {
                "en": "Salem",
                "簡中": "萨利姆",
                "繁中": "薩利姆",
            },
        },
        "strategy": {
            "en": "Saudi Arabia under Mancini favour a structured defensive approach with quick transitions. Al-Dawsari is the primary creative force, capable of moments of individual brilliance. They are compact and disciplined, making them awkward opponents in tournament football.",
            "簡中": "曼奇尼麾下的沙特偏好结构化的防守方式和快速转换。多萨里是主要的创造力量，能够创造个人闪光时刻。他们紧凑而有纪律，在赛事足球中是棘手的对手。",
            "繁中": "曼奇尼麾下的沙特偏好結構化的防守方式和快速轉換。多薩里是主要的創造力量，能夠創造個人閃光時刻。他們緊湊而有紀律，在賽事足球中是棘手的對手。",
        },
        "strengths": [
            {"en": "Mancini's tactical organization", "簡中": "曼奇尼的战术组织", "繁中": "曼奇尼的戰術組織"},
            {"en": "Al-Dawsari's creativity", "簡中": "多萨里的创造力", "繁中": "多薩里的創造力"},
            {"en": "Defensive discipline", "簡中": "防守纪律", "繁中": "防守紀律"},
            {"en": "Tournament experience", "簡中": "大赛经验", "繁中": "大賽經驗"},
        ],
        "weaknesses": [
            {"en": "Limited attacking depth", "簡中": "进攻深度有限", "繁中": "進攻深度有限"},
            {"en": "Physical disadvantage", "簡中": "身体对抗劣势", "繁中": "身體對抗劣勢"},
            {"en": "Struggle against high press", "簡中": "怕高位逼抢", "繁中": "怕高位逼搶"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 35,
        "elo_rating": 1530,
    },

    "Uruguay": {
        "coach": {
            "name": "Marcelo Bielsa",
            "nationality": "Argentine",
            "age": 69,
            "style": "Intense pressing",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Federico Valverde",
            "position": "CM",
            "nickname": {
                "en": "Fede",
                "簡中": "费德",
                "繁中": "費德",
            },
        },
        "strategy": {
            "en": "Uruguay under Bielsa play with trademark intensity, pressing high and attacking with verticality. Valverde is the engine driving the team forward with his box-to-box energy. The defence is well-organized and they are lethal on the counter when pressing triggers fail.",
            "簡中": "贝尔萨麾下的乌拉圭以标志性的强度踢球，高位逼抢并纵向进攻。巴尔韦德以全能中场的能量驱动球队前进。防守组织严密，当逼抢触发失败时反击致命。",
            "繁中": "貝爾薩麾下的烏拉圭以標誌性的強度踢球，高位逼搶並縱向進攻。巴爾韋德以全能中場的能量驅動球隊前進。防守組織嚴密，當逼搶觸發失敗時反擊致命。",
        },
        "strengths": [
            {"en": "Bielsa's pressing intensity", "簡中": "贝尔萨的逼抢强度", "繁中": "貝爾薩的逼搶強度"},
            {"en": "Valverde's all-round midfield ability", "簡中": "巴尔韦德的全能中场能力", "繁中": "巴爾韋德的全能中場能力"},
            {"en": "Defensive solidity", "簡中": "防守稳固", "繁中": "防守穩固"},
            {"en": "Counter-attacking quality", "簡中": "反击质量", "繁中": "反擊質量"},
        ],
        "weaknesses": [
            {"en": "Can be exposed by sustained possession", "簡中": "持续控球可暴露弱点", "繁中": "持續控球可暴露弱點"},
            {"en": "Occasional tactical rigidity", "簡中": "偶尔战术僵化", "繁中": "偶爾戰術僵化"},
            {"en": "Striker position inconsistency", "簡中": "前锋位置不稳定", "繁中": "前鋒位置不穩定"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 10,
        "elo_rating": 1870,
    },

    # ======================================================================
    # Group I
    # ======================================================================
    "France": {
        "coach": {
            "name": "Didier Deschamps",
            "nationality": "French",
            "age": 57,
            "style": "Pragmatic",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Kylian Mbappe",
            "position": "LW",
            "nickname": {
                "en": "Kylian",
                "簡中": "姆总",
                "繁中": "姆總",
            },
        },
        "strategy": {
            "en": "France balance defensive pragmatism with devastating attacking talent, using Mbappe's explosive pace as the ultimate weapon. The double pivot provides stability while the attacking midfielders create and finish chances. Deschamps' tournament know-how makes them perennial contenders.",
            "簡中": "法国平衡防守务实与毁灭性的进攻天赋，以姆巴佩的爆发速度作为终极武器。双后腰提供稳定性，攻击型中场创造和完成机会。德尚的大赛经验使他们始终是争冠热门。",
            "繁中": "法國平衡防守務實與毀滅性的進攻天賦，以姆巴佩的爆發速度作為終極武器。雙後腰提供穩定性，攻擊型中場創造和完成機會。德尚的大賽經驗使他們始終是爭冠熱門。",
        },
        "strengths": [
            {"en": "Mbappe's pace and finishing", "簡中": "姆巴佩的速度和射门", "繁中": "姆巴佩的速度和射門"},
            {"en": "Squad depth and talent", "簡中": "阵容深度和天赋", "繁中": "陣容深度和天賦"},
            {"en": "Tournament pedigree", "簡中": "大赛底蕴", "繁中": "大賽底蘊"},
            {"en": "Defensive solidity", "簡中": "防守稳固", "繁中": "防守穩固"},
            {"en": "Versatile attacking options", "簡中": "多样化的进攻选择", "繁中": "多樣化的進攻選擇"},
        ],
        "weaknesses": [
            {"en": "Occasional complacency against weaker sides", "簡中": "面对弱队偶尔松懈", "繁中": "面對弱隊偶爾鬆懈"},
            {"en": "Internal chemistry issues", "簡中": "内部化学反应问题", "繁中": "內部化學反應問題"},
            {"en": "Over-reliance on Mbappe moments", "簡中": "过度依赖姆巴佩的个人时刻", "繁中": "過度依賴姆巴佩的個人時刻"},
        ],
        "style": "balanced",
        "fifa_ranking": 3,
        "elo_rating": 2040,
    },

    "Senegal": {
        "coach": {
            "name": "Aliou Cisse",
            "nationality": "Senegalese",
            "age": 48,
            "style": "Defensive",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Sadio Mane",
            "position": "LW",
            "nickname": {
                "en": "Mane",
                "簡中": "马内",
                "繁中": "馬內",
            },
        },
        "strategy": {
            "en": "Senegal combine defensive discipline with Mane's explosive attacking quality on the counter. The double pivot shields the back four while the wide players provide pace on transitions. Cisse's leadership has built a resilient team culture that thrives in tournament football.",
            "簡中": "塞内加尔将防守纪律与马内在反击中的爆发性进攻质量相结合。双后腰保护后防线，边路球员在转换中提供速度。西塞的领导力建立了一种在赛事足球中蓬勃发展的韧性团队文化。",
            "繁中": "塞內加爾將防守紀律與馬內在反擊中的爆發性進攻質量相結合。雙後腰保護後防線，邊路球員在轉換中提供速度。西塞的領導力建立了一種在賽事足球中蓬勃發展的韌性團隊文化。",
        },
        "strengths": [
            {"en": "Mane's pace and finishing", "簡中": "马内的速度和射门", "繁中": "馬內的速度和射門"},
            {"en": "Defensive organization", "簡中": "防守组织", "繁中": "防守組織"},
            {"en": "Physical midfield", "簡中": "强壮的中场", "繁中": "強壯的中場"},
            {"en": "Team spirit and resilience", "簡中": "团队精神和韧性", "繁中": "團隊精神和韌性"},
        ],
        "weaknesses": [
            {"en": "Limited attacking depth beyond Mane", "簡中": "马内之外进攻深度有限", "繁中": "馬內之外進攻深度有限"},
            {"en": "Goalkeeping inconsistency", "簡中": "门将不稳定", "繁中": "門將不穩定"},
            {"en": "Struggle against possession teams", "簡中": "面对控球型球队吃力", "繁中": "面對控球型球隊吃力"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 17,
        "elo_rating": 1770,
    },

    "Iraq": {
        "coach": {
            "name": "Jesus Casas",
            "nationality": "Spanish",
            "age": 50,
            "style": "Balanced",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Aymen Hussein",
            "position": "ST",
            "nickname": {
                "en": "Aymen",
                "簡中": "艾门",
                "繁中": "艾門",
            },
        },
        "strategy": {
            "en": "Iraq play a balanced 4-3-3 influenced by Spanish coaching methodology. Hussein provides the focal point in attack while the midfield trio balances creativity with defensive work. They are technically competent but can struggle against physical opposition.",
            "簡中": "伊拉克踢受西班牙教练方法论影响的平衡4-3-3。侯赛因在进攻中提供支点，三中场平衡创造力与防守工作。他们技术过硬，但面对身体对抗型对手可能吃力。",
            "繁中": "伊拉克踢受西班牙教練方法論影響的平衡4-3-3。侯賽因在進攻中提供支點，三中場平衡創造力與防守工作。他們技術過硬，但面對身體對抗型對手可能吃力。",
        },
        "strengths": [
            {"en": "Technical midfield", "簡中": "技术型中场", "繁中": "技術型中場"},
            {"en": "Hussein's goal-scoring", "簡中": "侯赛因的进球能力", "繁中": "侯賽因的進球能力"},
            {"en": "Organized team shape", "簡中": "有序的队形", "繁中": "有序的隊形"},
        ],
        "weaknesses": [
            {"en": "Physical disadvantage", "簡中": "身体对抗劣势", "繁中": "身體對抗劣勢"},
            {"en": "Limited squad depth", "簡中": "阵容深度有限", "繁中": "陣容深度有限"},
            {"en": "Defensive lapses under pressure", "簡中": "高压下防守失误", "繁中": "高壓下防守失誤"},
            {"en": "Lack of elite-level experience", "簡中": "缺乏顶级赛事经验", "繁中": "缺乏頂級賽事經驗"},
        ],
        "style": "balanced",
        "fifa_ranking": 39,
        "elo_rating": 1560,
    },

    "Norway": {
        "coach": {
            "name": "Stale Solbakken",
            "nationality": "Norwegian",
            "age": 57,
            "style": "Balanced",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Erling Haaland",
            "position": "ST",
            "nickname": {
                "en": "The Robot",
                "簡中": "机器人",
                "繁中": "機器人",
            },
        },
        "strategy": {
            "en": "Norway build their entire attack around Haaland's phenomenal goal-scoring ability, using crosses and through balls to feed the striker. The midfield provides a balanced platform with Odegaard's creativity complementing Haaland's finishing. They are dangerous from set pieces and crosses.",
            "簡中": "挪威围绕哈兰德惊人的进球能力构建整个进攻，利用传中和直塞球喂给前锋。中场提供平衡平台，厄德高的创造力补充哈兰德的射门。他们在定位球和传中上很有威胁。",
            "繁中": "挪威圍繞哈蘭德驚人的進球能力構建整個進攻，利用傳中和直塞球餵給前鋒。中場提供平衡平台，厄德高的創造力補充哈蘭德的射門。他們在定位球和傳中上很有威脅。",
        },
        "strengths": [
            {"en": "Haaland's goal-scoring prowess", "簡中": "哈兰德的进球能力", "繁中": "哈蘭德的進球能力"},
            {"en": "Odegaard's creativity", "簡中": "厄德高的创造力", "繁中": "厄德高的創造力"},
            {"en": "Set-piece and crossing threat", "簡中": "定位球和传中威胁", "繁中": "定位球和傳中威脅"},
            {"en": "Physical presence", "簡中": "身体优势", "繁中": "身體優勢"},
        ],
        "weaknesses": [
            {"en": "Defensive vulnerability", "簡中": "防守脆弱", "繁中": "防守脆弱"},
            {"en": "Over-reliance on Haaland", "簡中": "过度依赖哈兰德", "繁中": "過度依賴哈蘭德"},
            {"en": "Limited depth beyond first XI", "簡中": "首发之外深度有限", "繁中": "首發之外深度有限"},
        ],
        "style": "balanced",
        "fifa_ranking": 21,
        "elo_rating": 1610,
    },

    # ======================================================================
    # Group J
    # ======================================================================
    "Argentina": {
        "coach": {
            "name": "Lionel Scaloni",
            "nationality": "Argentine",
            "age": 46,
            "style": "Pragmatic",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Lionel Messi",
            "position": "RW",
            "nickname": {
                "en": "Leo",
                "簡中": "梅老板",
                "繁中": "梅老闆",
            },
        },
        "strategy": {
            "en": "Argentina balance pragmatic defending with Messi's genius as the focal point of every attack. The midfield works tirelessly to win the ball and feed the forward line quickly. Scaloni's tactical flexibility allows them to adapt between possession and counter-attacking approaches.",
            "簡中": "阿根廷平衡务实的防守与梅西的天才作为每次进攻的焦点。中场不知疲倦地抢夺球权并快速喂给前锋线。斯卡洛尼的战术灵活性使他们能够在控球和反击之间切换。",
            "繁中": "阿根廷平衡務實的防守與梅西的天才作為每次進攻的焦點。中場不知疲倦地搶奪球權並快速餵給前鋒線。斯卡洛尼的戰術靈活性使他們能夠在控球和反擊之間切換。",
        },
        "strengths": [
            {"en": "Messi's individual brilliance", "簡中": "梅西的个人能力", "繁中": "梅西的個人能力"},
            {"en": "Tournament-winning mentality", "簡中": "冠军心态", "繁中": "冠軍心態"},
            {"en": "Defensive organization", "簡中": "防守组织", "繁中": "防守組織"},
            {"en": "Midfield work rate", "簡中": "中场跑动能力", "繁中": "中場跑動能力"},
            {"en": "Set-piece threat", "簡中": "定位球威胁", "繁中": "定位球威脅"},
        ],
        "weaknesses": [
            {"en": "Ageing core players", "簡中": "核心球员老化", "繁中": "核心球員老化"},
            {"en": "Over-reliance on Messi moments", "簡中": "过度依赖梅西的个人时刻", "繁中": "過度依賴梅西的個人時刻"},
            {"en": "Occasional slow starts", "簡中": "偶尔慢热", "繁中": "偶爾慢熱"},
        ],
        "style": "attacking_possession",
        "fifa_ranking": 1,
        "elo_rating": 2020,
    },

    "Algeria": {
        "coach": {
            "name": "Vladimir Petkovic",
            "nationality": "Bosnian-Swiss",
            "age": 61,
            "style": "Balanced",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Riyad Mahrez",
            "position": "RW",
            "nickname": {
                "en": "Riyad",
                "簡中": "里亚德",
                "繁中": "里亞德",
            },
        },
        "strategy": {
            "en": "Algeria play a balanced game with Mahrez as the primary creative force on the right flank. The double pivot provides defensive stability while the attacking midfielders support quick transitions. They are technically gifted but can be vulnerable against high-intensity pressing.",
            "簡中": "阿尔及利亚踢平衡的比赛，马赫雷斯是右路的主要创造力量。双后腰提供防守稳定性，攻击型中场支持快速转换。他们技术出色，但面对高强度逼抢可能脆弱。",
            "繁中": "阿爾及利亞踢平衡的比賽，馬赫雷斯是右路的主要創造力量。雙後腰提供防守穩定性，攻擊型中場支持快速轉換。他們技術出色，但面對高強度逼搶可能脆弱。",
        },
        "strengths": [
            {"en": "Mahrez's dribbling and creativity", "簡中": "马赫雷斯的盘带和创造力", "繁中": "馬赫雷斯的盤帶和創造力"},
            {"en": "Technical midfield", "簡中": "技术型中场", "繁中": "技術型中場"},
            {"en": "Counter-attacking quality", "簡中": "反击质量", "繁中": "反擊質量"},
            {"en": "AFCON experience", "簡中": "非洲杯经验", "繁中": "非洲盃經驗"},
        ],
        "weaknesses": [
            {"en": "Defensive lapses under pressure", "簡中": "高压下防守失误", "繁中": "高壓下防守失誤"},
            {"en": "Inconsistent goalkeeping", "簡中": "门将不稳定", "繁中": "門將不穩定"},
            {"en": "Vulnerable to high press", "簡中": "怕高位逼抢", "繁中": "怕高位逼搶"},
        ],
        "style": "balanced",
        "fifa_ranking": 31,
        "elo_rating": 1630,
    },

    "Austria": {
        "coach": {
            "name": "Ralf Rangnick",
            "nationality": "German",
            "age": 67,
            "style": "Gegenpressing",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Marcel Sabitzer",
            "position": "AM",
            "nickname": {
                "en": "Sabi",
                "簡中": "萨比",
                "繁中": "薩比",
            },
        },
        "strategy": {
            "en": "Austria under Rangnick are a relentless pressing machine, looking to win the ball high and attack quickly. Sabitzer provides creativity and goal threat from the number 10 position. Their intensity and organization make them dangerous opponents for any team.",
            "簡中": "朗尼克麾下的奥地利是一台无情的逼抢机器，力求高位夺回球权后快速进攻。萨比策在10号位提供创造力和进球威胁。他们的强度和组织使他们成为任何球队的危险对手。",
            "繁中": "朗尼克麾下的奧地利是一台無情的逼搶機器，力求高位奪回球權後快速進攻。薩比策在10號位提供創造力和進球威脅。他們的強度和組織使他們成為任何球隊的危險對手。",
        },
        "strengths": [
            {"en": "Rangnick's pressing system", "簡中": "朗尼克的逼抢体系", "繁中": "朗尼克的逼搶體系"},
            {"en": "Sabitzer's midfield drive", "簡中": "萨比策的中场推进", "繁中": "薩比策的中場推進"},
            {"en": "Team intensity and work rate", "簡中": "球队强度和跑动", "繁中": "球隊強度和跑動"},
            {"en": "Set-piece organization", "簡中": "定位球组织", "繁中": "定位球組織"},
        ],
        "weaknesses": [
            {"en": "Limited squad depth", "簡中": "阵容深度有限", "繁中": "陣容深度有限"},
            {"en": "Can be exposed by elite possession teams", "簡中": "顶级控球球队可暴露弱点", "繁中": "頂級控球球隊可暴露弱點"},
            {"en": "Lack of world-class striker", "簡中": "缺乏世界级前锋", "繁中": "缺乏世界級前鋒"},
        ],
        "style": "balanced",
        "fifa_ranking": 19,
        "elo_rating": 1740,
    },

    "Jordan": {
        "coach": {
            "name": "Hussein Ammouta",
            "nationality": "Moroccan",
            "age": 55,
            "style": "Defensive",
        },
        "formation": "4-4-1-1",
        "main_player": {
            "name": "Mousa Al-Taamari",
            "position": "RW",
            "nickname": {
                "en": "Mousa",
                "簡中": "穆萨",
                "繁中": "穆薩",
            },
        },
        "strategy": {
            "en": "Jordan play a defensive 4-4-1-1 with Al-Taamari providing the main counter-attacking threat. They stay compact and disciplined, looking to frustrate opponents and strike on the break. Ammouta's Moroccan influence adds tactical sophistication to their defensive approach.",
            "簡中": "约旦踢防守型4-4-1-1，塔马里提供主要的反击威胁。他们保持紧凑和纪律，力求限制对手并反击得分。阿穆塔的摩洛哥影响为他们的防守方式增添了战术复杂性。",
            "繁中": "約旦踢防守型4-4-1-1，塔馬里提供主要的反擊威脅。他們保持緊湊和紀律，力求限制對手並反擊得分。阿穆塔的摩洛哥影響為他們的防守方式增添了戰術複雜性。",
        },
        "strengths": [
            {"en": "Defensive discipline", "簡中": "防守纪律", "繁中": "防守紀律"},
            {"en": "Al-Taamari's dribbling", "簡中": "塔马里的盘带", "繁中": "塔馬里的盤帶"},
            {"en": "Team organization", "簡中": "团队组织", "繁中": "團隊組織"},
        ],
        "weaknesses": [
            {"en": "Limited technical quality", "簡中": "技术能力有限", "繁中": "技術能力有限"},
            {"en": "Lack of elite-level players", "簡中": "缺乏顶级球员", "繁中": "缺乏頂級球員"},
            {"en": "Poor ball retention", "簡中": "控球能力差", "繁中": "控球能力差"},
            {"en": "Shallow squad depth", "簡中": "阵容深度不足", "繁中": "陣容深度不足"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 44,
        "elo_rating": 1510,
    },

    # ======================================================================
    # Group K
    # ======================================================================
    "Portugal": {
        "coach": {
            "name": "Roberto Martinez",
            "nationality": "Spanish",
            "age": 51,
            "style": "Attacking",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Bruno Fernandes",
            "position": "AM",
            "nickname": {
                "en": "Bruno",
                "簡中": "布鲁诺",
                "繁中": "布魯諾",
            },
        },
        "strategy": {
            "en": "Portugal play an expansive attacking game with Fernandes pulling the strings from the number 10 role. The wide forwards provide pace and cutting-edge while the full-backs push high. Martinez's emphasis on attacking football maximizes their wealth of forward talent.",
            "簡中": "葡萄牙踢华丽的进攻足球，费尔南德斯在10号位组织进攻。边锋提供速度和杀伤力，边后卫高位压上。马丁内斯对进攻足球的强调最大化了他们丰富的前场天赋。",
            "繁中": "葡萄牙踢華麗的進攻足球，費爾南德斯在10號位組織進攻。邊鋒提供速度和殺傷力，邊後衛高位壓上。馬丁內斯對進攻足球的強調最大化了他們豐富的前場天賦。",
        },
        "strengths": [
            {"en": "Fernandes' creativity and passing", "簡中": "费尔南德斯的创造力和传球", "繁中": "費爾南德斯的創造力和傳球"},
            {"en": "Attacking depth and variety", "簡中": "进攻深度和多样性", "繁中": "進攻深度和多樣性"},
            {"en": "Technical quality across the pitch", "簡中": "全场技术质量", "繁中": "全場技術質量"},
            {"en": "Set-piece threat", "簡中": "定位球威胁", "繁中": "定位球威脅"},
            {"en": "Full-back attacking quality", "簡中": "边后卫进攻质量", "繁中": "邊後衛進攻質量"},
        ],
        "weaknesses": [
            {"en": "Defensive vulnerability in transitions", "簡中": "转换中防守脆弱", "繁中": "轉換中防守脆弱"},
            {"en": "Occasional lack of Plan B", "簡中": "偶尔缺乏B计划", "繁中": "偶爾缺乏B計劃"},
            {"en": "Striker position uncertainty", "簡中": "前锋位置不确定", "繁中": "前鋒位置不確定"},
        ],
        "style": "attacking_possession",
        "fifa_ranking": 6,
        "elo_rating": 1960,
    },

    "DR Congo": {
        "coach": {
            "name": "Sebastien Desabre",
            "nationality": "French",
            "age": 47,
            "style": "Counter-attacking",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Cedric Bakambu",
            "position": "ST",
            "nickname": {
                "en": "Cedric",
                "簡中": "塞德里克",
                "繁中": "塞德里克",
            },
        },
        "strategy": {
            "en": "DR Congo rely on Bakambu's pace and finishing on the counter-attack. They play a compact 4-3-3 that absorbs pressure before breaking quickly through wide areas. Their physicality and athleticism make them dangerous transition opponents.",
            "簡中": "刚果民主共和国依靠巴坎布在反击中的速度和射门。他们踢紧凑的4-3-3，吸收压力后通过边路快速突破。他们的身体对抗和运动能力使他们在转换中是危险的对手。",
            "繁中": "剛果民主共和國依靠巴坎布在反擊中的速度和射門。他們踢緊湊的4-3-3，吸收壓力後通過邊路快速突破。他們的身體對抗和運動能力使他們在轉換中是危險的對手。",
        },
        "strengths": [
            {"en": "Bakambu's pace and finishing", "簡中": "巴坎布的速度和射门", "繁中": "巴坎布的速度和射門"},
            {"en": "Physical athleticism", "簡中": "身体运动能力", "繁中": "身體運動能力"},
            {"en": "Counter-attacking speed", "簡中": "反击速度", "繁中": "反擊速度"},
        ],
        "weaknesses": [
            {"en": "Limited technical quality", "簡中": "技术能力有限", "繁中": "技術能力有限"},
            {"en": "Defensive lapses under sustained pressure", "簡中": "持续压力下防守失误", "繁中": "持續壓力下防守失誤"},
            {"en": "Poor ball retention", "簡中": "控球能力差", "繁中": "控球能力差"},
            {"en": "Lack of elite-level experience", "簡中": "缺乏顶级赛事经验", "繁中": "缺乏頂級賽事經驗"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 40,
        "elo_rating": 1480,
    },

    "Uzbekistan": {
        "coach": {
            "name": "Srecko Katanec",
            "nationality": "Slovenian",
            "age": 61,
            "style": "Defensive",
        },
        "formation": "4-4-2",
        "main_player": {
            "name": "Eldor Shomurodov",
            "position": "ST",
            "nickname": {
                "en": "Eldor",
                "簡中": "埃尔多尔",
                "繁中": "埃爾多爾",
            },
        },
        "strategy": {
            "en": "Uzbekistan play a compact 4-4-2 under Katanec, prioritizing defensive shape and discipline. Shomurodov provides the main attacking outlet with his movement and finishing. They are tough to break down but limited in possession and creativity.",
            "簡中": "乌兹别克斯坦在卡塔内茨带领下踢紧凑的4-4-2，优先考虑防守阵型和纪律。肖穆罗多夫凭借跑位和射门提供主要进攻出口。他们难以被攻破，但控球和创造力有限。",
            "繁中": "烏茲別克斯坦在卡塔內茨帶領下踢緊湊的4-4-2，優先考慮防守陣型和紀律。肖穆羅多夫憑藉跑位和射門提供主要進攻出口。他們難以被攻破，但控球和創造力有限。",
        },
        "strengths": [
            {"en": "Defensive discipline", "簡中": "防守纪律", "繁中": "防守紀律"},
            {"en": "Shomurodov's finishing", "簡中": "肖穆罗多夫的射门", "繁中": "肖穆羅多夫的射門"},
            {"en": "Physical presence", "簡中": "身体优势", "繁中": "身體優勢"},
        ],
        "weaknesses": [
            {"en": "Limited technical quality", "簡中": "技术能力有限", "繁中": "技術能力有限"},
            {"en": "Poor ball retention", "簡中": "控球能力差", "繁中": "控球能力差"},
            {"en": "Lack of creative midfielders", "簡中": "缺乏创造性中场", "繁中": "缺乏創造性中場"},
            {"en": "Vulnerable against pace", "簡中": "怕速度型球员", "繁中": "怕速度型球員"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 45,
        "elo_rating": 1520,
    },

    "Colombia": {
        "coach": {
            "name": "Nestor Lorenzo",
            "nationality": "Argentine",
            "age": 59,
            "style": "Counter-attacking",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "James Rodriguez",
            "position": "AM",
            "nickname": {
                "en": "James",
                "簡中": "哈梅斯",
                "繁中": "哈梅斯",
            },
        },
        "strategy": {
            "en": "Colombia blend defensive solidity with James' creative genius as the attacking fulcrum. The wide forwards provide pace while the midfield trio balances work rate with quality on the ball. They are dangerous on the counter and from set pieces with James' delivery.",
            "簡中": "哥伦比亚将防守稳固与哈梅斯的创造天才作为进攻支点相结合。边锋提供速度，三中场平衡跑动与持球质量。他们在反击和定位球上很有威胁，哈梅斯的传中是关键。",
            "繁中": "哥倫比亞將防守穩固與哈梅斯的創造天才作為進攻支點相結合。邊鋒提供速度，三中場平衡跑動與持球質量。他們在反擊和定位球上很有威脅，哈梅斯的傳中是關鍵。",
        },
        "strengths": [
            {"en": "James' passing and creativity", "簡中": "哈梅斯的传球和创造力", "繁中": "哈梅斯的傳球和創造力"},
            {"en": "Counter-attacking quality", "簡中": "反击质量", "繁中": "反擊質量"},
            {"en": "Pace on the flanks", "簡中": "边路速度", "繁中": "邊路速度"},
            {"en": "Defensive organization", "簡中": "防守组织", "繁中": "防守組織"},
        ],
        "weaknesses": [
            {"en": "Over-reliance on James' fitness", "簡中": "过度依赖哈梅斯的体能", "繁中": "過度依賴哈梅斯的體能"},
            {"en": "Striker inconsistency", "簡中": "前锋不稳定", "繁中": "前鋒不穩定"},
            {"en": "Vulnerable to high press", "簡中": "怕高位逼抢", "繁中": "怕高位逼搶"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 11,
        "elo_rating": 1850,
    },

    # ======================================================================
    # Group L
    # ======================================================================
    "England": {
        "coach": {
            "name": "Thomas Tuchel",
            "nationality": "German",
            "age": 51,
            "style": "Tactical flexibility",
        },
        "formation": "4-2-3-1",
        "main_player": {
            "name": "Jude Bellingham",
            "position": "AM",
            "nickname": {
                "en": "Jude",
                "簡中": "贝林",
                "繁中": "貝林",
            },
        },
        "strategy": {
            "en": "England under Tuchel combine tactical flexibility with Bellingham's dynamic midfield presence. The double pivot provides a stable base while the attacking quartet rotates fluidly. Tuchel's ability to adapt formations in-game gives England a significant tactical edge.",
            "簡中": "图赫尔麾下的英格兰将战术灵活性与贝林厄姆的动态中场存在相结合。双后腰提供稳定基础，攻击四人组灵活轮转。图赫尔在赛中调整阵型的能力给了英格兰显著的战术优势。",
            "繁中": "圖赫爾麾下的英格蘭將戰術靈活性與貝林厄姆的動態中場存在相結合。雙後腰提供穩定基礎，攻擊四人組靈活輪轉。圖赫爾在賽中調整陣型的能力給了英格蘭顯著的戰術優勢。",
        },
        "strengths": [
            {"en": "Bellingham's all-round ability", "簡中": "贝林厄姆的全面能力", "繁中": "貝林厄姆的全面能力"},
            {"en": "Tactical flexibility", "簡中": "战术灵活性", "繁中": "戰術靈活性"},
            {"en": "Squad depth", "簡中": "阵容深度", "繁中": "陣容深度"},
            {"en": "Set-piece threat", "簡中": "定位球威胁", "繁中": "定位球威脅"},
            {"en": "Attacking variety", "簡中": "进攻多样性", "繁中": "進攻多樣性"},
        ],
        "weaknesses": [
            {"en": "Pressure expectation from fans and media", "簡中": "球迷和媒体的期望压力", "繁中": "球迷和媒體的期望壓力"},
            {"en": "Occasional defensive lapses", "簡中": "偶尔防守失误", "繁中": "偶爾防守失誤"},
            {"en": "Goalkeeper position uncertainty", "簡中": "门将位置不确定", "繁中": "門將位置不確定"},
        ],
        "style": "balanced",
        "fifa_ranking": 4,
        "elo_rating": 1990,
    },

    "Croatia": {
        "coach": {
            "name": "Zlatko Dalic",
            "nationality": "Croatian",
            "age": 57,
            "style": "Defensive",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Luka Modric",
            "position": "CM",
            "nickname": {
                "en": "Luka",
                "簡中": "魔笛",
                "繁中": "魔笛",
            },
        },
        "strategy": {
            "en": "Croatia rely on Modric's orchestration in midfield combined with a disciplined defensive structure. The midfield trio controls possession and tempo while the team stays compact without the ball. Dalic's tournament experience makes them formidable knockout-round opponents.",
            "簡中": "克罗地亚依靠莫德里奇在中场的指挥和纪律严明的防守结构。三中场控制球权和节奏，无球时球队保持紧凑。达利奇的大赛经验使他们成为令人生畏的淘汰赛对手。",
            "繁中": "克羅地亞依靠莫德里奇在中場的指揮和紀律嚴明的防守結構。三中場控制球權和節奏，無球時球隊保持緊湊。達利奇的大賽經驗使他們成為令人生畏的淘汰賽對手。",
        },
        "strengths": [
            {"en": "Modric's passing and vision", "簡中": "莫德里奇的传球和视野", "繁中": "莫德里奇的傳球和視野"},
            {"en": "Midfield control", "簡中": "中场控制力", "繁中": "中場控制力"},
            {"en": "Tournament pedigree", "簡中": "大赛底蕴", "繁中": "大賽底蘊"},
            {"en": "Defensive discipline", "簡中": "防守纪律", "繁中": "防守紀律"},
        ],
        "weaknesses": [
            {"en": "Ageing midfield core", "簡中": "中场核心老化", "繁中": "中場核心老化"},
            {"en": "Lack of elite striker", "簡中": "缺乏顶级前锋", "繁中": "缺乏頂級前鋒"},
            {"en": "Limited attacking depth", "簡中": "进攻深度有限", "繁中": "進攻深度有限"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 12,
        "elo_rating": 1900,
    },

    "Ghana": {
        "coach": {
            "name": "Otto Addo",
            "nationality": "Ghanaian",
            "age": 49,
            "style": "Attacking",
        },
        "formation": "4-3-3",
        "main_player": {
            "name": "Mohammed Kudus",
            "position": "AM",
            "nickname": {
                "en": "Kudus",
                "簡中": "库杜斯",
                "繁中": "庫杜斯",
            },
        },
        "strategy": {
            "en": "Ghana play with attacking intent, using Kudus' dribbling and creativity as the primary weapon. The midfield is athletic and forward-thinking while the wide players provide pace and directness. They are dangerous going forward but can be exposed defensively.",
            "簡中": "加纳以进攻意图踢球，以库杜斯的盘带和创造力作为主要武器。中场运动能力强且富有前插意识，边路球员提供速度和直接性。他们进攻端很有威胁，但防守可能暴露问题。",
            "繁中": "加納以進攻意圖踢球，以庫杜斯的盤帶和創造力作為主要武器。中場運動能力強且富有前插意識，邊路球員提供速度和直接性。他們進攻端很有威脅，但防守可能暴露問題。",
        },
        "strengths": [
            {"en": "Kudus' dribbling and creativity", "簡中": "库杜斯的盘带和创造力", "繁中": "庫杜斯的盤帶和創造力"},
            {"en": "Athletic midfield", "簡中": "运动型中场", "繁中": "運動型中場"},
            {"en": "Pace on the flanks", "簡中": "边路速度", "繁中": "邊路速度"},
            {"en": "Attacking mentality", "簡中": "进攻心态", "繁中": "進攻心態"},
        ],
        "weaknesses": [
            {"en": "Defensive vulnerability", "簡中": "防守脆弱", "繁中": "防守脆弱"},
            {"en": "Transition lapses", "簡中": "转换失误", "繁中": "轉換失誤"},
            {"en": "Goalkeeping inconsistency", "簡中": "门将不稳定", "繁中": "門將不穩定"},
        ],
        "style": "attacking_possession",
        "fifa_ranking": 25,
        "elo_rating": 1690,
    },

    "Panama": {
        "coach": {
            "name": "Thomas Christiansen",
            "nationality": "Danish-Spanish",
            "age": 52,
            "style": "Defensive",
        },
        "formation": "5-4-1",
        "main_player": {
            "name": "Adalberto Carrasquilla",
            "position": "MF",
            "nickname": {
                "en": "Carrasquilla",
                "簡中": "卡拉斯基亚",
                "繁中": "卡拉斯基亞",
            },
        },
        "strategy": {
            "en": "Panama set up in a deep 5-4-1, prioritizing defensive compactness and discipline. Carrasquilla provides the main creative outlet from midfield with his passing range. They rely on set pieces and counter-attacks to pose any attacking threat.",
            "簡中": "巴拿马采用深度5-4-1阵型，优先考虑防守紧凑性和纪律。卡拉斯基亚凭借传球范围从中场提供主要创造出口。他们依靠定位球和反击来制造进攻威胁。",
            "繁中": "巴拿馬採用深度5-4-1陣型，優先考慮防守緊湊性和紀律。卡拉斯基亞憑藉傳球範圍從中場提供主要創造出口。他們依靠定位球和反擊來製造進攻威脅。",
        },
        "strengths": [
            {"en": "Defensive discipline", "簡中": "防守纪律", "繁中": "防守紀律"},
            {"en": "Carrasquilla's passing", "簡中": "卡拉斯基亚的传球", "繁中": "卡拉斯基亞的傳球"},
            {"en": "Team spirit and resilience", "簡中": "团队精神和韧性", "繁中": "團隊精神和韌性"},
        ],
        "weaknesses": [
            {"en": "Very limited technical quality", "簡中": "技术能力非常有限", "繁中": "技術能力非常有限"},
            {"en": "Lack of elite-level players", "簡中": "缺乏顶级球员", "繁中": "缺乏頂級球員"},
            {"en": "Poor ball retention", "簡中": "控球能力差", "繁中": "控球能力差"},
            {"en": "Vulnerable against quality opposition", "簡中": "面对强队脆弱", "繁中": "面對強隊脆弱"},
        ],
        "style": "defensive_counter",
        "fifa_ranking": 41,
        "elo_rating": 1570,
    },
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_team_profile(team: str) -> dict:
    """Return the full profile dict for a team."""
    return TEAM_PROFILES.get(team, {})


def get_team_coach(team: str) -> dict:
    """Return coach info dict for a team."""
    profile = TEAM_PROFILES.get(team, {})
    return profile.get("coach", {})


def get_team_formation(team: str) -> str:
    """Return formation string for a team."""
    profile = TEAM_PROFILES.get(team, {})
    return profile.get("formation", "")


def get_team_strategy(team: str, lang: str = "en") -> str:
    """Return strategy description in the specified language.

    Args:
        team: Team name.
        lang: Language key — 'en', '簡中', or '繁中'.

    Returns:
        Strategy string in the requested language, or empty string.
    """
    profile = TEAM_PROFILES.get(team, {})
    strategy = profile.get("strategy", {})
    return strategy.get(lang, strategy.get("en", ""))


def get_team_main_player(team: str, lang: str = "en") -> dict:
    """Return main player info with nickname in the specified language.

    Args:
        team: Team name.
        lang: Language key — 'en', '簡中', or '繁中'.

    Returns:
        Dict with 'name', 'position', and 'nickname' (str in requested lang).
    """
    profile = TEAM_PROFILES.get(team, {})
    player = profile.get("main_player", {})
    if not player:
        return {}
    nickname_dict = player.get("nickname", {})
    return {
        "name": player.get("name", ""),
        "position": player.get("position", ""),
        "nickname": nickname_dict.get(lang, nickname_dict.get("en", "")),
    }


def get_team_strengths(team: str, lang: str = "en") -> list:
    """Return list of strength strings in the specified language.

    Args:
        team: Team name.
        lang: Language key — 'en', '簡中', or '繁中'.

    Returns:
        List of strength description strings.
    """
    profile = TEAM_PROFILES.get(team, {})
    strengths = profile.get("strengths", [])
    return [s.get(lang, s.get("en", "")) for s in strengths]


def get_team_weaknesses(team: str, lang: str = "en") -> list:
    """Return list of weakness strings in the specified language.

    Args:
        team: Team name.
        lang: Language key — 'en', '簡中', or '繁中'.

    Returns:
        List of weakness description strings.
    """
    profile = TEAM_PROFILES.get(team, {})
    weaknesses = profile.get("weaknesses", [])
    return [w.get(lang, w.get("en", "")) for w in weaknesses]


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def quick_test() -> bool:
    """Validate all 48 teams have complete data.

    Checks:
      - All 48 teams from WC2026_GROUPS exist in TEAM_PROFILES.
      - Each team has all required fields with non-empty values.
      - All tri-lingual dicts have 'en', '簡中', '繁中' keys.
      - Style matches TEAM_STYLE_CLASSIFICATION.
      - FIFA ranking and ELO rating match reference data.

    Returns:
        True if all checks pass, raises AssertionError otherwise.
    """
    all_teams = []
    for group_teams in WC2026_GROUPS.values():
        all_teams.extend(group_teams)

    assert len(all_teams) == 48, f"Expected 48 teams in groups, got {len(all_teams)}"
    assert len(set(all_teams)) == 48, "Duplicate teams found in groups"

    required_fields = ["coach", "formation", "main_player", "strategy",
                       "strengths", "weaknesses", "style", "fifa_ranking",
                       "elo_rating"]

    coach_fields = ["name", "nationality", "age", "style"]
    player_fields = ["name", "position", "nickname"]
    lang_keys = {"en", "簡中", "繁中"}

    for team in all_teams:
        assert team in TEAM_PROFILES, f"Missing profile for {team}"
        profile = TEAM_PROFILES[team]

        for field in required_fields:
            assert field in profile, f"{team}: missing field '{field}'"
            assert profile[field], f"{team}: empty field '{field}'"

        # Coach checks
        coach = profile["coach"]
        for cf in coach_fields:
            assert cf in coach, f"{team}/coach: missing '{cf}'"
            assert coach[cf], f"{team}/coach: empty '{cf}'"
        assert isinstance(coach["age"], int), f"{team}/coach/age must be int"

        # Formation check
        assert "-" in profile["formation"], f"{team}: formation format invalid"

        # Main player checks
        player = profile["main_player"]
        for pf in player_fields:
            assert pf in player, f"{team}/main_player: missing '{pf}'"
        nickname = player["nickname"]
        for lk in lang_keys:
            assert lk in nickname, f"{team}/main_player/nickname: missing '{lk}'"
            assert nickname[lk], f"{team}/main_player/nickname: empty '{lk}'"

        # Strategy checks
        strategy = profile["strategy"]
        for lk in lang_keys:
            assert lk in strategy, f"{team}/strategy: missing '{lk}'"
            assert strategy[lk], f"{team}/strategy: empty '{lk}'"

        # Strengths checks
        strengths = profile["strengths"]
        assert 3 <= len(strengths) <= 5, f"{team}: strengths count {len(strengths)} not 3-5"
        for i, s in enumerate(strengths):
            for lk in lang_keys:
                assert lk in s, f"{team}/strengths[{i}]: missing '{lk}'"
                assert s[lk], f"{team}/strengths[{i}]: empty '{lk}'"

        # Weaknesses checks
        weaknesses = profile["weaknesses"]
        assert 3 <= len(weaknesses) <= 5, f"{team}: weaknesses count {len(weaknesses)} not 3-5"
        for i, w in enumerate(weaknesses):
            for lk in lang_keys:
                assert lk in w, f"{team}/weaknesses[{i}]: missing '{lk}'"
                assert w[lk], f"{team}/weaknesses[{i}]: empty '{lk}'"

        # Style check
        style = profile["style"]
        assert style in TEAM_STYLE_CLASSIFICATION, f"{team}: style '{style}' not in classification"
        assert team in TEAM_STYLE_CLASSIFICATION[style], f"{team}: not listed under style '{style}'"

        # FIFA ranking check
        assert profile["fifa_ranking"] == FIFA_RANKINGS.get(team), \
            f"{team}: fifa_ranking mismatch"

        # ELO rating check
        assert profile["elo_rating"] == ELO_RATINGS.get(team), \
            f"{team}: elo_rating mismatch"

    print(f"All 48 teams validated successfully.")
    return True


if __name__ == "__main__":
    quick_test()
