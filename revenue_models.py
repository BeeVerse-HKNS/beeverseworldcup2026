PRICING_TIERS = {
    'free': {
        'name': 'Free',
        'price': {'default': '$0', 'china': '¥0'},
        'period': '',
        'features': [
            'Basic match predictions (Win/Draw/Lose)',
            'Top 10 team rankings',
            'Player database browse',
            'Tournament bracket view',
            'News feed (limited)',
        ],
        'limits': {
            'predictions_per_day': 5,
            'factor_breakdown': False,
            'xfactor_details': False,
            'historical_comparison': False,
            'api_access': False,
        },
    },
    'pro': {
        'name': 'Pro',
        'price': {'default': '$7.99/mo', 'china': '¥39/月', 'hong_kong': 'HK$58/月'},
        'period': 'monthly',
        'features': [
            'Unlimited match predictions',
            'Full factor breakdown (5 factors)',
            'X-Factor player analysis',
            'Historical comparison data',
            'Tournament simulation (unlimited)',
            'Real-time match alerts',
            'Ad-free experience',
        ],
        'limits': {
            'predictions_per_day': -1,
            'factor_breakdown': True,
            'xfactor_details': True,
            'historical_comparison': True,
            'api_access': False,
        },
        'stripe_link': {
            'default': 'https://buy.stripe.com/pro_monthly',
            'china': '',
        },
    },
    'enterprise': {
        'name': 'Enterprise',
        'price': {'default': '$49.99/mo', 'china': '¥249/月', 'hong_kong': 'HK$388/月'},
        'period': 'monthly',
        'features': [
            'Everything in Pro',
            'API access (1000 calls/day)',
            'Custom model parameters',
            'Bulk predictions',
            'Priority support',
            'White-label options',
            'Data export (CSV/JSON)',
        ],
        'limits': {
            'predictions_per_day': -1,
            'factor_breakdown': True,
            'xfactor_details': True,
            'historical_comparison': True,
            'api_access': True,
        },
        'stripe_link': {
            'default': 'https://buy.stripe.com/enterprise_monthly',
            'china': '',
        },
    },
}

AFFILIATE_PRODUCTS = {
    'jersey': {
        'name': {'default': 'Official WC Jersey', 'china': '世界盃正版球衣'},
        'url': {
            'default': 'https://www.fifa.com/fifaplus/en/tournaments/mens/worldcup/canadamexicousa2026/shop/jerseys',
            'china': 'https://s.click.taobao.com/wc2026_jersey',
        },
        'description': {'default': 'Official licensed jerseys', 'china': '官方授權球衣，支持你嘅球隊'},
        'category': 'merchandise',
        'is_gambling': False,
        'commission_rate': 0.05,
    },
    'tickets': {
        'name': {'default': 'Match Tickets', 'china': '世界盃門票'},
        'url': {
            'default': 'https://www.fifa.com/fifaplus/en/tournaments/mens/worldcup/canadamexicousa2026/tickets',
            'china': 'https://s.click.taobao.com/wc2026_tickets',
        },
        'description': {'default': 'FIFA World Cup 2026 tickets', 'china': '2026 美加墨世界盃現場門票'},
        'category': 'tickets',
        'is_gambling': False,
        'commission_rate': 0.10,
    },
    'travel': {
        'name': {'default': 'Travel Packages', 'china': '世界盃旅行套餐'},
        'url': {
            'default': 'https://www.booking.com/searchresults.html?ss=world+cup+2026',
            'china': 'https://s.click.taobao.com/wc2026_travel',
        },
        'description': {'default': 'Flight + Hotel + Ticket bundles', 'china': '機票+酒店+門票一站式服務'},
        'category': 'travel',
        'is_gambling': False,
        'commission_rate': 0.06,
    },
    'streaming': {
        'name': {'default': 'Streaming Subscriptions', 'china': '直播訂閱'},
        'url': {
            'default': 'https://www.fifa.com/fifaplus/en/tournaments/mens/worldcup/canadamexicousa2026/broadcast',
            'china': 'https://s.click.taobao.com/wc2026_streaming',
        },
        'description': {'default': 'Official broadcast streaming', 'china': '官方授權直播平台'},
        'category': 'streaming',
        'is_gambling': False,
        'commission_rate': 0.08,
    },
}

FEATURE_COMPARISON = [
    {'feature': 'Daily Predictions', 'free': '5', 'pro': 'Unlimited', 'enterprise': 'Unlimited'},
    {'feature': 'Factor Breakdown', 'free': '—', 'pro': '✓', 'enterprise': '✓'},
    {'feature': 'X-Factor Analysis', 'free': '—', 'pro': '✓', 'enterprise': '✓'},
    {'feature': 'Historical Comparison', 'free': '—', 'pro': '✓', 'enterprise': '✓'},
    {'feature': 'Tournament Simulation', 'free': '1/day', 'pro': 'Unlimited', 'enterprise': 'Unlimited'},
    {'feature': 'Real-time Alerts', 'free': '—', 'pro': '✓', 'enterprise': '✓'},
    {'feature': 'API Access', 'free': '—', 'pro': '—', 'enterprise': '1000/day'},
    {'feature': 'Custom Parameters', 'free': '—', 'pro': '—', 'enterprise': '✓'},
    {'feature': 'Data Export', 'free': '—', 'pro': '—', 'enterprise': '✓'},
    {'feature': 'White-label', 'free': '—', 'pro': '—', 'enterprise': '✓'},
    {'feature': 'Priority Support', 'free': '—', 'pro': 'Email', 'enterprise': 'Dedicated'},
    {'feature': 'Ad-free', 'free': '—', 'pro': '✓', 'enterprise': '✓'},
]

API_DOCS_URL = 'https://docs.wc2026predictor.com/api'


class RevenueManager:
    def get_pricing_tiers(self, jurisdiction: str = 'other') -> list:
        tiers = []
        for tier_id, tier in PRICING_TIERS.items():
            price = tier['price'].get(jurisdiction, tier['price'].get('default', '$0'))
            stripe_link = ''
            if 'stripe_link' in tier:
                links = tier['stripe_link']
                stripe_link = links.get(jurisdiction, links.get('default', ''))
            tiers.append({
                'id': tier_id,
                'name': tier['name'],
                'price': price,
                'period': tier['period'],
                'features': tier['features'],
                'limits': tier['limits'],
                'stripe_link': stripe_link,
            })
        return tiers

    def get_compliant_affiliate_products(self, jurisdiction: str = 'other') -> list:
        products = []
        for product_id, product in AFFILIATE_PRODUCTS.items():
            if product.get('is_gambling', False):
                continue
            name = product['name'].get(jurisdiction, product['name'].get('default', ''))
            url = product['url'].get(jurisdiction, product['url'].get('default', ''))
            desc = product['description'].get(jurisdiction, product['description'].get('default', ''))
            products.append({
                'id': product_id,
                'name': name,
                'url': url,
                'description': desc,
                'category': product['category'],
                'commission_rate': product['commission_rate'],
            })
        return products

    def get_feature_comparison(self) -> list:
        return FEATURE_COMPARISON

    def get_api_docs_url(self) -> str:
        return API_DOCS_URL
