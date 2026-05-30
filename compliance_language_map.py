COMPLIANT_TERMS = {
    'predict': {
        'default': 'predict',
        'china': '预测',
        'hong_kong': '預測',
        'eu': 'forecast',
    },
    'betting': {
        'default': 'analytical insight',
        'china': '數據分析',
        'hong_kong': '數據分析',
        'eu': 'statistical analysis',
    },
    'odds': {
        'default': 'probability indicator',
        'china': '概率指標',
        'hong_kong': '概率指標',
        'eu': 'probability indicator',
    },
    'gambling': {
        'default': 'entertainment analytics',
        'china': '娛樂分析',
        'hong_kong': '娛樂分析',
        'eu': 'entertainment analytics',
    },
    'win': {
        'default': 'favored outcome',
        'china': '預測勝出',
        'hong_kong': '預測勝出',
        'eu': 'favored outcome',
    },
    'premium': {
        'default': 'Premium',
        'china': '高級版',
        'hong_kong': 'Premium',
        'eu': 'Premium',
    },
}

GAMBLING_TERMS = [
    'bet', 'betting', 'wager', 'gamble', 'gambling', 'stake',
    'bookmaker', 'bookie', 'odds', 'payout', 'jackpot',
    '下注', '賭博', '赌博', '投注', '博彩',
]


def compliant_text(key: str, jurisdiction: str = 'other') -> str:
    terms = COMPLIANT_TERMS.get(key)
    if not terms:
        return key
    return terms.get(jurisdiction, terms.get('default', key))


def check_compliance(text: str, jurisdiction: str = 'other') -> dict:
    violations = []
    text_lower = text.lower()
    for term in GAMBLING_TERMS:
        if term.lower() in text_lower:
            replacement = compliant_text('gambling', jurisdiction)
            violations.append({
                'term': term,
                'replacement': replacement,
                'severity': 'high' if jurisdiction in ('china', 'eu') else 'medium',
            })
    return {
        'compliant': len(violations) == 0,
        'violations': violations,
        'jurisdiction': jurisdiction,
    }
