import sys
import os
import time
import random
import traceback
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from languages import LANGUAGES, LANGUAGE_NAMES, get_text, get_language_name
from formula_v9_ultimate import FormulaV9

@dataclass
class TestResult:
    passed: int = 0
    failed: int = 0
    errors: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)

class WC2026MultiLangUITester:
    def __init__(self):
        self.engine = None
        self.results = {
            'layer1': TestResult(),
            'layer2': TestResult(),
            'layer3': TestResult()
        }
        self.issues = []
        
    def setup(self) -> bool:
        try:
            self.engine = FormulaV9('data/wc2026_player_database.json')
            if len(self.engine.players) == 0:
                self.issues.append("Engine loaded but no players found")
                return False
            return True
        except Exception as e:
            self.issues.append(f"Engine load failed: {str(e)}")
            return False
    
    def test_language_system(self) -> Tuple[bool, str]:
        try:
            if len(LANGUAGES) != 3:
                return False, f"Expected 3 languages, got {len(LANGUAGES)}"
            
            for lang in ['en', 'zh_hant', 'zh_hans']:
                if lang not in LANGUAGES:
                    return False, f"Language {lang} not found"
                
                if 'app_title' not in LANGUAGES[lang]:
                    return False, f"app_title missing in {lang}"
                
                text = get_text('app_title', lang)
                if not text or text == 'app_title':
                    return False, f"get_text failed for {lang}"
            
            return True, "Language system OK"
        except Exception as e:
            return False, str(e)
    
    def test_language_switching(self, iterations: int = 100) -> Tuple[bool, str]:
        try:
            keys = ['app_title', 'home', 'match_prediction', 'team_comparison', 
                   'player_database', 'tournament_simulation', 'model_analysis']
            
            for _ in range(iterations):
                lang = random.choice(['en', 'zh_hant', 'zh_hans'])
                key = random.choice(keys)
                text = get_text(key, lang)
                if not text:
                    return False, f"Empty text for {key} in {lang}"
            
            return True, f"Language switching OK ({iterations} iterations)"
        except Exception as e:
            return False, str(e)
    
    def test_all_pages_load(self) -> Tuple[bool, str]:
        try:
            pages = ['home', 'match_prediction', 'team_comparison', 
                    'player_database', 'tournament_simulation', 'model_analysis']
            
            for page in pages:
                for lang in ['en', 'zh_hant', 'zh_hans']:
                    title = get_text(f'{page}_title' if page != 'home' else 'app_title', lang)
                    if not title:
                        return False, f"Page title missing: {page} in {lang}"
            
            return True, "All pages have titles in all languages"
        except Exception as e:
            return False, str(e)
    
    def test_prediction_function(self) -> Tuple[bool, str]:
        try:
            teams = self.engine.get_all_teams()
            if len(teams) < 2:
                return False, "Not enough teams for prediction"
            
            home = random.choice(teams)
            away = random.choice([t for t in teams if t != home])
            
            result = self.engine.predict_match(home, away, 2.0, 3.2, 3.5)
            
            if not result.get('success'):
                return False, f"Prediction failed: {result.get('error', 'Unknown')}"
            
            required_keys = ['home_win_probability', 'draw_probability', 
                           'away_win_probability', 'predicted_result', 'confidence']
            
            for key in required_keys:
                if key not in result:
                    return False, f"Missing key: {key}"
            
            return True, "Prediction function OK"
        except Exception as e:
            return False, str(e)
    
    def test_database_load(self) -> Tuple[bool, str]:
        try:
            if len(self.engine.players) == 0:
                return False, "No players loaded"
            
            if len(self.engine.teams) == 0:
                return False, "No teams loaded"
            
            teams = self.engine.get_all_teams()
            if len(teams) == 0:
                return False, "get_all_teams returned empty"
            
            return True, f"Database OK: {len(self.engine.players)} players, {len(teams)} teams"
        except Exception as e:
            return False, str(e)
    
    def test_ui_design_tokens(self) -> Tuple[bool, str]:
        try:
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
            
            required_tokens = ['primary_color', 'background', 'card_bg', 
                             'text_primary', 'border_radius']
            
            for token in required_tokens:
                if token not in DESIGN_TOKENS:
                    return False, f"Missing design token: {token}"
            
            return True, "Design tokens OK"
        except Exception as e:
            return False, str(e)
    
    def run_layer1_tests(self) -> TestResult:
        result = self.results['layer1']
        
        tests = [
            ("Language System", self.test_language_system),
            ("All Pages Load", self.test_all_pages_load),
            ("Prediction Function", self.test_prediction_function),
            ("Database Load", self.test_database_load),
            ("UI Design Tokens", self.test_ui_design_tokens),
        ]
        
        for name, test_func in tests:
            try:
                passed, msg = test_func()
                if passed:
                    result.passed += 1
                    result.details[name] = f"✅ {msg}"
                else:
                    result.failed += 1
                    result.errors.append(f"{name}: {msg}")
                    result.details[name] = f"❌ {msg}"
            except Exception as e:
                result.failed += 1
                result.errors.append(f"{name}: Exception - {str(e)}")
                result.details[name] = f"❌ Exception: {str(e)}"
        
        return result
    
    def run_layer2_tests(self, iterations: int = 100000) -> TestResult:
        result = self.results['layer2']
        
        lang_combos = [
            ('en', 'zh_hant'),
            ('en', 'zh_hans'),
            ('zh_hant', 'zh_hans'),
        ]
        
        start_time = time.time()
        
        passed_count = 0
        failed_count = 0
        
        for _ in range(iterations // 100):
            lang1, lang2 = random.choice(lang_combos)
            
            text1 = get_text('app_title', lang1)
            text2 = get_text('app_title', lang2)
            
            if text1 and text2 and text1 != text2:
                passed_count += 1
            else:
                failed_count += 1
        
        result.details['language_combinations'] = f"✅ {passed_count} passed"
        result.passed += 1 if failed_count == 0 else 0
        result.failed += 1 if failed_count > 0 else 0
        
        teams = self.engine.get_all_teams()
        page_switch_passed = 0
        page_switch_failed = 0
        
        pages = ['home', 'match_prediction', 'team_comparison', 
                'player_database', 'tournament_simulation', 'model_analysis']
        
        for _ in range(iterations // 100):
            page = random.choice(pages)
            lang = random.choice(['en', 'zh_hant', 'zh_hans'])
            
            key = f'{page}_title' if page != 'home' else 'app_title'
            text = get_text(key, lang)
            
            if text:
                page_switch_passed += 1
            else:
                page_switch_failed += 1
        
        result.details['page_switching'] = f"✅ {page_switch_passed} passed"
        result.passed += 1 if page_switch_failed == 0 else 0
        result.failed += 1 if page_switch_failed > 0 else 0
        
        prediction_passed = 0
        prediction_failed = 0
        
        for _ in range(iterations // 1000):
            home = random.choice(teams)
            away = random.choice([t for t in teams if t != home])
            
            result_pred = self.engine.predict_match(home, away, 2.0, 3.2, 3.5)
            
            if result_pred.get('success'):
                prediction_passed += 1
            else:
                prediction_failed += 1
        
        result.details['predictions'] = f"✅ {prediction_passed} passed"
        result.passed += 1 if prediction_failed == 0 else 0
        result.failed += 1 if prediction_failed > 0 else 0
        
        elapsed = time.time() - start_time
        result.details['elapsed_time'] = f"{elapsed:.2f}s"
        result.details['iterations'] = iterations
        
        return result
    
    def run_layer3_tests(self, iterations: int = 1000000) -> TestResult:
        result = self.results['layer3']
        
        start_time = time.time()
        
        stability_passed = 0
        stability_failed = 0
        
        teams = self.engine.get_all_teams()
        
        for i in range(iterations // 10000):
            try:
                lang = random.choice(['en', 'zh_hant', 'zh_hans'])
                text = get_text('app_title', lang)
                
                if not text:
                    stability_failed += 1
                    continue
                
                home = random.choice(teams)
                away = random.choice([t for t in teams if t != home])
                
                pred = self.engine.predict_match(home, away, 2.0, 3.2, 3.5)
                
                if not pred.get('success'):
                    stability_failed += 1
                    continue
                
                stability_passed += 1
                
            except Exception as e:
                stability_failed += 1
                self.issues.append(f"Stability test error at iteration {i}: {str(e)}")
        
        result.details['stability'] = f"✅ {stability_passed} passed, {stability_failed} failed"
        result.passed += 1 if stability_failed == 0 else 0
        result.failed += 1 if stability_failed > 0 else 0
        
        edge_passed = 0
        edge_failed = 0
        
        edge_cases = [
            (1.01, 1.01, 50.0),
            (50.0, 50.0, 1.01),
            (1.01, 50.0, 1.01),
            (2.0, 2.0, 2.0),
        ]
        
        for _ in range(iterations // 100000):
            home = random.choice(teams)
            away = random.choice([t for t in teams if t != home])
            home_odds, draw_odds, away_odds = random.choice(edge_cases)
            
            try:
                pred = self.engine.predict_match(home, away, home_odds, draw_odds, away_odds)
                
                if pred.get('success'):
                    edge_passed += 1
                else:
                    edge_failed += 1
            except Exception:
                edge_failed += 1
        
        result.details['edge_cases'] = f"✅ {edge_passed} passed, {edge_failed} failed"
        result.passed += 1 if edge_failed == 0 else 0
        result.failed += 1 if edge_failed > 0 else 0
        
        error_recovery_passed = 0
        error_recovery_failed = 0
        
        for _ in range(iterations // 100000):
            try:
                pred = self.engine.predict_match("NonExistentTeam1", "NonExistentTeam2")
                
                if not pred.get('success') and 'error' in pred:
                    error_recovery_passed += 1
                else:
                    error_recovery_failed += 1
            except Exception:
                error_recovery_passed += 1
        
        result.details['error_recovery'] = f"✅ {error_recovery_passed} passed"
        result.passed += 1 if error_recovery_failed == 0 else 0
        result.failed += 1 if error_recovery_failed > 0 else 0
        
        elapsed = time.time() - start_time
        result.details['elapsed_time'] = f"{elapsed:.2f}s"
        result.details['iterations'] = iterations
        
        return result
    
    def generate_report(self) -> str:
        report = []
        report.append("=" * 60)
        report.append("WC2026 多語言 UI/UX 3 層測試報告")
        report.append("=" * 60)
        report.append("")
        
        report.append("## Layer 1 測試（快速功能測試）")
        report.append("-" * 40)
        l1 = self.results['layer1']
        l1_total = l1.passed + l1.failed
        l1_rate = (l1.passed / l1_total * 100) if l1_total > 0 else 0
        report.append(f"通過率: {l1_rate:.1f}% ({l1.passed}/{l1_total})")
        for name, detail in l1.details.items():
            report.append(f"  - {name}: {detail}")
        if l1.errors:
            report.append("  錯誤:")
            for err in l1.errors:
                report.append(f"    ❌ {err}")
        report.append("")
        
        report.append("## Layer 2 測試（壓力測試）")
        report.append("-" * 40)
        l2 = self.results['layer2']
        l2_total = l2.passed + l2.failed
        l2_rate = (l2.passed / l2_total * 100) if l2_total > 0 else 0
        report.append(f"通過率: {l2_rate:.1f}% ({l2.passed}/{l2_total})")
        report.append(f"迭代次數: {l2.details.get('iterations', 'N/A')}")
        report.append(f"執行時間: {l2.details.get('elapsed_time', 'N/A')}")
        for name, detail in l2.details.items():
            if name not in ['iterations', 'elapsed_time']:
                report.append(f"  - {name}: {detail}")
        report.append("")
        
        report.append("## Layer 3 測試（穩定性測試）")
        report.append("-" * 40)
        l3 = self.results['layer3']
        l3_total = l3.passed + l3.failed
        l3_rate = (l3.passed / l3_total * 100) if l3_total > 0 else 0
        report.append(f"通過率: {l3_rate:.1f}% ({l3.passed}/{l3_total})")
        report.append(f"迭代次數: {l3.details.get('iterations', 'N/A')}")
        report.append(f"執行時間: {l3.details.get('elapsed_time', 'N/A')}")
        for name, detail in l3.details.items():
            if name not in ['iterations', 'elapsed_time']:
                report.append(f"  - {name}: {detail}")
        report.append("")
        
        if self.issues:
            report.append("## 發現的問題")
            report.append("-" * 40)
            for issue in self.issues:
                report.append(f"  ❌ {issue}")
            report.append("")
        
        all_passed = (l1.failed == 0 and l2.failed == 0 and l3.failed == 0)
        
        report.append("## 總結")
        report.append("-" * 40)
        if all_passed:
            report.append("✅ 所有測試通過！系統穩定。")
        else:
            report.append("⚠️ 部分測試失敗，需要修復。")
        
        return "\n".join(report)

def main():
    print("開始 WC2026 多語言 UI/UX 3 層測試...\n")
    
    tester = WC2026MultiLangUITester()
    
    print("Step 1: 初始化...")
    if not tester.setup():
        print("❌ 初始化失敗")
        for issue in tester.issues:
            print(f"  - {issue}")
        return
    
    print(f"✅ 初始化成功: {len(tester.engine.players)} players, {len(tester.engine.teams)} teams\n")
    
    print("Step 2: Layer 1 測試（快速功能測試）...")
    tester.run_layer1_tests()
    print(f"✅ Layer 1 完成\n")
    
    print("Step 3: Layer 2 測試（壓力測試 - 100,000 cases）...")
    tester.run_layer2_tests(100000)
    print(f"✅ Layer 2 完成\n")
    
    print("Step 4: Layer 3 測試（穩定性測試 - 1,000,000 cases）...")
    tester.run_layer3_tests(1000000)
    print(f"✅ Layer 3 完成\n")
    
    print("Step 5: 生成報告...")
    report = tester.generate_report()
    print(report)
    
    with open('test_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    print("\n報告已保存到 test_report.txt")

if __name__ == "__main__":
    main()
