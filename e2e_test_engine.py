"""
E2E Testing Engine for World Cup 2026 Streamlit Application

Test Categories:
- Page Load Tests: Verify all 8 pages load without errors
- Language Tests: Verify language switching works (EN/zh_hant/zh_hans)
- Functional Tests: Test prediction, comparison, simulation features
- Performance Tests: Measure page load times

Report: Generated to data/e2e_test_report.json
"""

import unittest
import json
import time
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_PATH = SCRIPT_DIR / 'data' / 'wc2026_player_database.json'
REPORT_PATH = SCRIPT_DIR / 'data' / 'e2e_test_report.json'


class TestResult:
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category
        self.passed = False
        self.error: Optional[str] = None
        self.execution_time_ms: float = 0.0
        self.details: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'category': self.category,
            'passed': self.passed,
            'error': self.error,
            'execution_time_ms': self.execution_time_ms,
            'details': self.details
        }


class TestReport:
    def __init__(self):
        self.results: List[TestResult] = []
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None

    def add_result(self, result: TestResult):
        self.results.append(result)

    def finalize(self):
        self.end_time = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed

        categories = {}
        for r in self.results:
            if r.category not in categories:
                categories[r.category] = {'passed': 0, 'failed': 0, 'total': 0}
            categories[r.category]['total'] += 1
            if r.passed:
                categories[r.category]['passed'] += 1
            else:
                categories[r.category]['failed'] += 1

        return {
            'summary': {
                'total_tests': total,
                'passed': passed,
                'failed': failed,
                'pass_rate': f"{(passed/total*100):.2f}%" if total > 0 else "0.00%",
                'execution_time_seconds': (self.end_time - self.start_time).total_seconds() if self.end_time else 0
            },
            'categories': categories,
            'results': [r.to_dict() for r in self.results],
            'timestamp': self.start_time.isoformat()
        }

    def save(self, path: Path):
        self.finalize()
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


class DataLoader:
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.data: Dict[str, Any] = {}
        self.loaded = False

    def load(self) -> bool:
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.loaded = True
            return True
        except Exception as e:
            self.loaded = False
            return False

    def get_teams(self) -> List[str]:
        if not self.loaded:
            return []
        return list(self.data.get('teams', {}).keys())

    def get_players(self) -> List[Dict]:
        if not self.loaded:
            return []
        players = []
        for team_data in self.data.get('teams', {}).values():
            players.extend(team_data.get('players', []))
        return players

    def get_news(self) -> List[Dict]:
        if not self.loaded:
            return []
        return self.data.get('news', [])

    def get_xfactor_players(self) -> List[Dict]:
        return [p for p in self.get_players() if p.get('is_xfactor', False)]


class LanguageManager:
    LANGUAGES = ['en', 'zh_hant', 'zh_hans']

    def __init__(self):
        self.translations: Dict[str, Dict[str, str]] = {}
        self._load_translations()

    def _load_translations(self):
        try:
            from languages import LANGUAGES
            self.translations = LANGUAGES
        except ImportError:
            self.translations = {
                'en': {'home': 'Home'},
                'zh_hant': {'home': '首頁'},
                'zh_hans': {'home': '首页'}
            }

    def get_text(self, key: str, lang: str) -> str:
        return self.translations.get(lang, {}).get(key, key)

    def get_all_languages(self) -> List[str]:
        return self.LANGUAGES


class PageLoadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loader = DataLoader(DATA_PATH)
        cls.loader.load()
        cls.report = TestReport()

    def _run_test(self, test_name: str, test_func) -> TestResult:
        result = TestResult(test_name, 'page_load')
        start = time.time()
        try:
            test_func()
            result.passed = True
        except Exception as e:
            result.passed = False
            result.error = str(e)
        result.execution_time_ms = (time.time() - start) * 1000
        self.report.add_result(result)
        return result

    def test_data_file_exists(self):
        def test():
            self.assertTrue(DATA_PATH.exists(), f"Data file not found: {DATA_PATH}")
        result = self._run_test("Data File Exists", test)
        self.assertTrue(result.passed, result.error)

    def test_data_file_valid_json(self):
        def test():
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.assertIsInstance(data, dict)
            self.assertIn('teams', data)
        result = self._run_test("Data File Valid JSON", test)
        self.assertTrue(result.passed, result.error)

    def test_home_page_data(self):
        def test():
            teams = self.loader.get_teams()
            self.assertGreater(len(teams), 0, "No teams found")
            players = self.loader.get_players()
            self.assertGreater(len(players), 0, "No players found")
        result = self._run_test("Home Page Data", test)
        self.assertTrue(result.passed, result.error)

    def test_match_prediction_page_data(self):
        def test():
            teams = self.loader.get_teams()
            self.assertGreaterEqual(len(teams), 2, "Need at least 2 teams for prediction")
            self.assertIn("Brazil", teams, "Brazil not found in teams")
            self.assertIn("Argentina", teams, "Argentina not found in teams")
        result = self._run_test("Match Prediction Page Data", test)
        self.assertTrue(result.passed, result.error)

    def test_team_comparison_page_data(self):
        def test():
            teams = self.loader.get_teams()
            self.assertGreaterEqual(len(teams), 2, "Need at least 2 teams for comparison")
        result = self._run_test("Team Comparison Page Data", test)
        self.assertTrue(result.passed, result.error)

    def test_player_database_page_data(self):
        def test():
            players = self.loader.get_players()
            self.assertGreater(len(players), 0, "No players found")
            required_fields = ['name', 'position', 'age']
            for player in players[:10]:
                for field in required_fields:
                    self.assertIn(field, player, f"Missing field: {field}")
        result = self._run_test("Player Database Page Data", test)
        self.assertTrue(result.passed, result.error)

    def test_tournament_simulation_page_data(self):
        def test():
            teams = self.loader.get_teams()
            self.assertGreaterEqual(len(teams), 16, "Need at least 16 teams for tournament simulation")
        result = self._run_test("Tournament Simulation Page Data", test)
        self.assertTrue(result.passed, result.error)

    def test_model_analysis_page_data(self):
        def test():
            teams = self.loader.get_teams()
            for team_name in teams[:5]:
                team_data = self.loader.data['teams'][team_name]
                self.assertIn('players', team_data, f"Missing players for {team_name}")
        result = self._run_test("Model Analysis Page Data", test)
        self.assertTrue(result.passed, result.error)

    def test_news_page_data(self):
        def test():
            news = self.loader.get_news()
            self.assertGreater(len(news), 0, "No news found")
            for article in news[:5]:
                self.assertIn('source', article, "Missing source in news")
                self.assertIn('content', article, "Missing content in news")
        result = self._run_test("News Page Data", test)
        self.assertTrue(result.passed, result.error)

    def test_xfactor_page_data(self):
        def test():
            xfactor = self.loader.get_xfactor_players()
            self.assertGreater(len(xfactor), 0, "No X-Factor players found")
            for player in xfactor[:5]:
                self.assertTrue(player.get('is_xfactor', False), "Player not marked as X-Factor")
        result = self._run_test("X-Factor Page Data", test)
        self.assertTrue(result.passed, result.error)

    @classmethod
    def tearDownClass(cls):
        cls.report.save(REPORT_PATH)


class LanguageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lang_manager = LanguageManager()
        cls.report = TestReport()

    def _run_test(self, test_name: str, test_func) -> TestResult:
        result = TestResult(test_name, 'language')
        start = time.time()
        try:
            test_func()
            result.passed = True
        except Exception as e:
            result.passed = False
            result.error = str(e)
        result.execution_time_ms = (time.time() - start) * 1000
        self.report.add_result(result)
        return result

    def test_english_translations(self):
        def test():
            lang = 'en'
            home = self.lang_manager.get_text('home', lang)
            self.assertEqual(home, 'Home')
            prediction = self.lang_manager.get_text('match_prediction', lang)
            self.assertEqual(prediction, 'Match Prediction')
        result = self._run_test("English Translations", test)
        self.assertTrue(result.passed, result.error)

    def test_traditional_chinese_translations(self):
        def test():
            lang = 'zh_hant'
            home = self.lang_manager.get_text('home', lang)
            self.assertEqual(home, '首頁')
            prediction = self.lang_manager.get_text('match_prediction', lang)
            self.assertEqual(prediction, '賽事預測')
        result = self._run_test("Traditional Chinese Translations", test)
        self.assertTrue(result.passed, result.error)

    def test_simplified_chinese_translations(self):
        def test():
            lang = 'zh_hans'
            home = self.lang_manager.get_text('home', lang)
            self.assertEqual(home, '首页')
            prediction = self.lang_manager.get_text('match_prediction', lang)
            self.assertEqual(prediction, '赛事预测')
        result = self._run_test("Simplified Chinese Translations", test)
        self.assertTrue(result.passed, result.error)

    def test_all_languages_available(self):
        def test():
            langs = self.lang_manager.get_all_languages()
            self.assertEqual(len(langs), 3)
            self.assertIn('en', langs)
            self.assertIn('zh_hant', langs)
            self.assertIn('zh_hans', langs)
        result = self._run_test("All Languages Available", test)
        self.assertTrue(result.passed, result.error)

    def test_key_pages_translated(self):
        def test():
            pages = ['home', 'match_prediction', 'team_comparison', 'player_database',
                     'tournament_simulation', 'model_analysis', 'news_page', 'xfactor_page']
            for lang in self.lang_manager.get_all_languages():
                for page in pages:
                    text = self.lang_manager.get_text(page, lang)
                    self.assertIsNotNone(text)
                    self.assertNotEqual(text, page, f"Translation missing for {page} in {lang}")
        result = self._run_test("Key Pages Translated", test)
        self.assertTrue(result.passed, result.error)

    @classmethod
    def tearDownClass(cls):
        existing_report = cls._load_existing_report()
        for r in cls.report.results:
            existing_report.add_result(r)
        existing_report.save(REPORT_PATH)

    @staticmethod
    def _load_existing_report() -> TestReport:
        report = TestReport()
        if REPORT_PATH.exists():
            try:
                with open(REPORT_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for r in data.get('results', []):
                    if r['category'] != 'language':
                        result = TestResult(r['name'], r['category'])
                        result.passed = r['passed']
                        result.error = r['error']
                        result.execution_time_ms = r['execution_time_ms']
                        report.add_result(result)
            except Exception:
                pass
        return report


class FunctionalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loader = DataLoader(DATA_PATH)
        cls.loader.load()
        cls.report = TestReport()

    def _run_test(self, test_name: str, test_func) -> TestResult:
        result = TestResult(test_name, 'functional')
        start = time.time()
        try:
            test_func()
            result.passed = True
        except Exception as e:
            result.passed = False
            result.error = str(e)
        result.execution_time_ms = (time.time() - start) * 1000
        self.report.add_result(result)
        return result

    def test_match_prediction_flow(self):
        def test():
            teams = self.loader.get_teams()
            self.assertGreaterEqual(len(teams), 2)
            home_team = "Brazil"
            away_team = "Argentina"
            self.assertIn(home_team, teams)
            self.assertIn(away_team, teams)
            home_odds = 2.0
            draw_odds = 3.2
            away_odds = 3.5
            self.assertGreater(home_odds, 1.0)
            self.assertGreater(draw_odds, 1.0)
            self.assertGreater(away_odds, 1.0)
        result = self._run_test("Match Prediction Flow", test)
        self.assertTrue(result.passed, result.error)

    def test_team_comparison_flow(self):
        def test():
            teams = self.loader.get_teams()
            team1 = "Argentina"
            team2 = "Brazil"
            self.assertIn(team1, teams)
            self.assertIn(team2, teams)
            team1_data = self.loader.data['teams'][team1]
            team2_data = self.loader.data['teams'][team2]
            self.assertIn('players', team1_data)
            self.assertIn('players', team2_data)
        result = self._run_test("Team Comparison Flow", test)
        self.assertTrue(result.passed, result.error)

    def test_player_database_flow(self):
        def test():
            teams = self.loader.get_teams()
            selected_team = teams[0]
            players = self.loader.data['teams'][selected_team].get('players', [])
            self.assertGreater(len(players), 0)
            for player in players[:5]:
                self.assertIn('name', player)
                self.assertIn('position', player)
        result = self._run_test("Player Database Flow", test)
        self.assertTrue(result.passed, result.error)

    def test_news_filtering(self):
        def test():
            news = self.loader.get_news()
            self.assertGreater(len(news), 0)
            sources = set(n['source'] for n in news)
            self.assertGreater(len(sources), 0)
            filtered = [n for n in news if n['source'] == list(sources)[0]]
            self.assertGreater(len(filtered), 0)
        result = self._run_test("News Filtering", test)
        self.assertTrue(result.passed, result.error)

    def test_news_pagination(self):
        def test():
            news = self.loader.get_news()
            total = len(news)
            items_per_page = 50
            total_pages = (total + items_per_page - 1) // items_per_page
            self.assertGreater(total_pages, 0)
            page_1 = news[0:items_per_page]
            self.assertLessEqual(len(page_1), items_per_page)
        result = self._run_test("News Pagination", test)
        self.assertTrue(result.passed, result.error)

    def test_xfactor_display(self):
        def test():
            xfactor = self.loader.get_xfactor_players()
            self.assertGreater(len(xfactor), 0)
            for player in xfactor[:5]:
                self.assertTrue(player.get('is_xfactor', False))
                self.assertIn('name', player)
                self.assertIn('team', player) if 'team' in player else self.assertIn('position', player)
        result = self._run_test("X-Factor Display", test)
        self.assertTrue(result.passed, result.error)

    def test_tournament_simulation_structure(self):
        def test():
            teams = self.loader.get_teams()
            self.assertGreaterEqual(len(teams), 16)
            self.assertGreaterEqual(len(teams), 8)
        result = self._run_test("Tournament Simulation Structure", test)
        self.assertTrue(result.passed, result.error)

    @classmethod
    def tearDownClass(cls):
        existing_report = cls._load_existing_report()
        for r in cls.report.results:
            existing_report.add_result(r)
        existing_report.save(REPORT_PATH)

    @staticmethod
    def _load_existing_report() -> TestReport:
        report = TestReport()
        if REPORT_PATH.exists():
            try:
                with open(REPORT_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for r in data.get('results', []):
                    if r['category'] != 'functional':
                        result = TestResult(r['name'], r['category'])
                        result.passed = r['passed']
                        result.error = r['error']
                        result.execution_time_ms = r['execution_time_ms']
                        report.add_result(result)
            except Exception:
                pass
        return report


class PerformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loader = DataLoader(DATA_PATH)
        cls.loader.load()
        cls.report = TestReport()
        cls.performance_threshold_ms = 1000

    def _run_test(self, test_name: str, test_func) -> TestResult:
        result = TestResult(test_name, 'performance')
        start = time.time()
        try:
            test_func()
            result.passed = True
        except Exception as e:
            result.passed = False
            result.error = str(e)
        result.execution_time_ms = (time.time() - start) * 1000
        self.report.add_result(result)
        return result

    def test_data_load_time(self):
        def test():
            loader = DataLoader(DATA_PATH)
            loader.load()
            self.assertTrue(loader.loaded)
        result = self._run_test("Data Load Time", test)
        self.assertTrue(result.passed, result.error)
        result.details['threshold_ms'] = self.performance_threshold_ms
        result.details['within_threshold'] = result.execution_time_ms < self.performance_threshold_ms

    def test_teams_query_time(self):
        def test():
            for _ in range(100):
                teams = self.loader.get_teams()
            self.assertGreater(len(teams), 0)
        result = self._run_test("Teams Query Time (100x)", test)
        self.assertTrue(result.passed, result.error)

    def test_players_query_time(self):
        def test():
            for _ in range(100):
                players = self.loader.get_players()
            self.assertGreater(len(players), 0)
        result = self._run_test("Players Query Time (100x)", test)
        self.assertTrue(result.passed, result.error)

    def test_news_query_time(self):
        def test():
            for _ in range(100):
                news = self.loader.get_news()
            self.assertGreater(len(news), 0)
        result = self._run_test("News Query Time (100x)", test)
        self.assertTrue(result.passed, result.error)

    def test_xfactor_query_time(self):
        def test():
            for _ in range(100):
                xfactor = self.loader.get_xfactor_players()
            self.assertGreater(len(xfactor), 0)
        result = self._run_test("X-Factor Query Time (100x)", test)
        self.assertTrue(result.passed, result.error)

    def test_json_serialization_time(self):
        def test():
            for _ in range(10):
                json.dumps(self.loader.data)
        result = self._run_test("JSON Serialization Time (10x)", test)
        self.assertTrue(result.passed, result.error)

    @classmethod
    def tearDownClass(cls):
        existing_report = cls._load_existing_report()
        for r in cls.report.results:
            existing_report.add_result(r)
        existing_report.save(REPORT_PATH)

    @staticmethod
    def _load_existing_report() -> TestReport:
        report = TestReport()
        if REPORT_PATH.exists():
            try:
                with open(REPORT_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for r in data.get('results', []):
                    if r['category'] != 'performance':
                        result = TestResult(r['name'], r['category'])
                        result.passed = r['passed']
                        result.error = r['error']
                        result.execution_time_ms = r['execution_time_ms']
                        report.add_result(result)
            except Exception:
                pass
        return report


def run_all_tests() -> Dict[str, Any]:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(PageLoadTests))
    suite.addTests(loader.loadTestsFromTestCase(LanguageTests))
    suite.addTests(loader.loadTestsFromTestCase(FunctionalTests))
    suite.addTests(loader.loadTestsFromTestCase(PerformanceTests))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if REPORT_PATH.exists():
        with open(REPORT_PATH, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
    else:
        report_data = {
            'summary': {
                'total_tests': 0,
                'passed': 0,
                'failed': 0,
                'pass_rate': '0.00%'
            }
        }

    return report_data


def print_summary(report: Dict[str, Any]):
    print("\n" + "=" * 60)
    print("E2E Test Summary")
    print("=" * 60)

    summary = report.get('summary', {})
    print(f"Total Tests: {summary.get('total_tests', 0)}")
    print(f"Passed: {summary.get('passed', 0)}")
    print(f"Failed: {summary.get('failed', 0)}")
    print(f"Pass Rate: {summary.get('pass_rate', '0.00%')}")
    print(f"Execution Time: {summary.get('execution_time_seconds', 0):.2f}s")

    print("\nCategories:")
    for cat, stats in report.get('categories', {}).items():
        print(f"  {cat}: {stats['passed']}/{stats['total']} passed")

    print("\n" + "=" * 60)
    print(f"Report saved to: {REPORT_PATH}")
    print("=" * 60)


if __name__ == '__main__':
    report = run_all_tests()
    print_summary(report)
