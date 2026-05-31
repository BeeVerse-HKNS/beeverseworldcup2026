PHONE_TO_JURISDICTION = {
    '+86': 'china',
    '+852': 'hong_kong',
    '+886': 'hong_kong',
    '+44': 'uk',
    '+49': 'eu',
    '+33': 'eu',
    '+34': 'eu',
    '+39': 'eu',
    '+31': 'eu',
    '+46': 'eu',
    '+47': 'eu',
    '+351': 'eu',
    '+1': 'us',
    '+81': 'japan',
    '+82': 'south_korea',
    '+65': 'singapore',
    '+60': 'other',
    '+61': 'other',
    '+55': 'other',
    '+52': 'other',
    '+54': 'other',
    '+56': 'other',
    '+57': 'other',
    '+91': 'other',
    '+92': 'other',
    '+62': 'other',
    '+66': 'other',
    '+84': 'other',
    '+63': 'other',
    '+234': 'other',
    '+27': 'other',
    '+971': 'other',
    '+966': 'other',
    '+965': 'other',
    '+20': 'other',
}

JURISDICTION_INFO = {
    'china': {
        'name': 'China',
        'regulation': 'PIPL + 生成式AI法規',
        'risk_level': 'high',
        'requires_consent': True,
        'requires_data_localization': True,
        'gambling_prohibited': True,
    },
    'hong_kong': {
        'name': 'Hong Kong',
        'regulation': 'PDPO',
        'risk_level': 'medium',
        'requires_consent': True,
        'requires_data_localization': False,
        'gambling_prohibited': True,
    },
    'eu': {
        'name': 'European Union',
        'regulation': 'AI Act + GDPR',
        'risk_level': 'high',
        'requires_consent': True,
        'requires_data_localization': True,
        'gambling_prohibited': False,
    },
    'uk': {
        'name': 'United Kingdom',
        'regulation': 'UK GDPR',
        'risk_level': 'medium',
        'requires_consent': True,
        'requires_data_localization': False,
        'gambling_prohibited': False,
    },
    'us': {
        'name': 'United States',
        'regulation': 'CCPA + State AI Laws',
        'risk_level': 'medium',
        'requires_consent': False,
        'requires_data_localization': False,
        'gambling_prohibited': False,
    },
    'japan': {
        'name': 'Japan',
        'regulation': 'Voluntary AI Guidelines',
        'risk_level': 'low',
        'requires_consent': False,
        'requires_data_localization': False,
        'gambling_prohibited': False,
    },
    'south_korea': {
        'name': 'South Korea',
        'regulation': 'PIPA + AI Ethics Policy',
        'risk_level': 'medium',
        'requires_consent': True,
        'requires_data_localization': False,
        'gambling_prohibited': True,
    },
    'singapore': {
        'name': 'Singapore',
        'regulation': 'Model AI Framework + PDPA',
        'risk_level': 'low',
        'requires_consent': True,
        'requires_data_localization': False,
        'gambling_prohibited': False,
    },
    'other': {
        'name': 'Other',
        'regulation': 'General',
        'risk_level': 'low',
        'requires_consent': False,
        'requires_data_localization': False,
        'gambling_prohibited': False,
    },
}


class JurisdictionDetector:
    def detect_from_phone(self, country_code: str) -> str:
        return PHONE_TO_JURISDICTION.get(country_code, 'other')

    def get_jurisdiction_info(self, jurisdiction: str) -> dict:
        return JURISDICTION_INFO.get(jurisdiction, JURISDICTION_INFO['other'])

    def is_gambling_prohibited(self, jurisdiction: str) -> bool:
        info = self.get_jurisdiction_info(jurisdiction)
        return info.get('gambling_prohibited', False)

    def requires_consent(self, jurisdiction: str) -> bool:
        info = self.get_jurisdiction_info(jurisdiction)
        return info.get('requires_consent', False)
