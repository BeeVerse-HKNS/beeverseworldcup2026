"""
測試 DeepResearchLoopEngine 同 ProgressVisualizer
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deep_research_loop_engine import DeepResearchLoopEngine, IterationResult
from progress_visualizer import ProgressVisualizer
import json


def test_deep_research_loop_engine():
    print("========== 測試 DeepResearchLoopEngine ==========")
    
    engine = DeepResearchLoopEngine(
        target_iterations=10,
        target_xfactor=30,
        target_news=100,
        target_accuracy=0.75,
        data_path="data/wc2026_player_database.json"
    )
    
    assert engine.target_iterations == 10, "target_iterations 設置失敗"
    assert engine.target_xfactor == 30, "target_xfactor 設置失敗"
    assert engine.data is not None, "數據載入失敗"
    
    print("✅ __init__ 測試通過")
    
    report = engine.run(max_hours=0.01)
    
    assert engine.iteration_count == 10, f"迭代次數錯誤：{engine.iteration_count}"
    assert "summary" in report, "報告缺少 summary"
    assert "targets_achieved" in report, "報告缺少 targets_achieved"
    
    print(f"✅ run() 測試通過")
    print(f"   - 迭代次數：{report['summary']['total_iterations']}")
    print(f"   - X-Factor：{report['summary']['total_xfactor']}")
    print(f"   - 新聞數：{report['summary']['total_news']}")
    print(f"   - 準確率：{report['summary']['final_accuracy']*100:.2f}%")
    
    return True


def test_progress_visualizer():
    print("\n========== 測試 ProgressVisualizer ==========")
    
    visualizer = ProgressVisualizer(output_dir="data/visualizations")
    
    test_data = {
        "迭代次數": 100,
        "X-Factor": 45,
        "新聞數": 1100,
        "準確率(%)": 78.5
    }
    
    test_target = {
        "迭代次數": 100,
        "X-Factor": 30,
        "新聞數": 10000,
        "準確率(%)": 75.0
    }
    
    fig1 = visualizer.generate_bar_chart(test_data, "目標達成狀態", test_target)
    assert fig1 is not None, "generate_bar_chart 失敗"
    print("✅ generate_bar_chart 測試通過")
    
    path1 = visualizer.save_chart(fig1, "test_target_achievement.png")
    assert os.path.exists(path1), f"圖表保存失敗：{path1}"
    print(f"✅ save_chart 測試通過：{path1}")
    
    iteration_history = [
        {"iteration": i, "news_collected": 11, "xfactor_identified": 0, "accuracy": 0.1 + i * 0.07}
        for i in range(1, 11)
    ]
    
    fig2 = visualizer.generate_progress_chart(iteration_history, "測試進度追蹤")
    assert fig2 is not None, "generate_progress_chart 失敗"
    print("✅ generate_progress_chart 測試通過")
    
    path2 = visualizer.save_chart(fig2, "test_progress_chart.png")
    assert os.path.exists(path2), f"進度圖保存失敗：{path2}"
    print(f"✅ 進度圖保存通過：{path2}")
    
    summary = {
        "total_iterations": 100,
        "total_xfactor": 45,
        "total_news": 1100,
        "final_accuracy": 0.785,
        "total_time_hours": 2.5
    }
    
    targets = {
        "iterations": 100,
        "xfactor": 30,
        "news": 10000,
        "accuracy": 0.75
    }
    
    fig3 = visualizer.generate_summary_dashboard(summary, targets)
    assert fig3 is not None, "generate_summary_dashboard 失敗"
    print("✅ generate_summary_dashboard 測試通過")
    
    path3 = visualizer.save_chart(fig3, "test_summary_dashboard.png")
    assert os.path.exists(path3), f"儀表板保存失敗：{path3}"
    print(f"✅ 儀表板保存通過：{path3}")
    
    return True


def test_xfactor_field():
    print("\n========== 測試 is_xfactor 字段 ==========")
    
    with open("data/wc2026_player_database.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    xfactor_count = 0
    total_count = 0
    correct_count = 0
    
    for team_name, team_data in data.get("teams", {}).items():
        for player in team_data.get("players", []):
            total_count += 1
            rating = player.get("rating", 0)
            is_xfactor = player.get("is_xfactor", False)
            
            if rating >= 85:
                xfactor_count += 1
            
            if is_xfactor == (rating >= 85):
                correct_count += 1
    
    assert total_count > 0, "沒有球員數據"
    assert correct_count == total_count, f"is_xfactor 字段錯誤：{correct_count}/{total_count}"
    
    print(f"✅ is_xfactor 字段測試通過")
    print(f"   - 總球員數：{total_count}")
    print(f"   - X-Factor 球員：{xfactor_count}")
    print(f"   - 正確標記：{correct_count}/{total_count}")
    
    return True


def main():
    print("\n" + "=" * 60)
    print("World Cup 2026 Deep Research Loop Engine 測試")
    print("=" * 60 + "\n")
    
    results = []
    
    try:
        results.append(("DeepResearchLoopEngine", test_deep_research_loop_engine()))
    except Exception as e:
        print(f"❌ DeepResearchLoopEngine 測試失敗：{e}")
        results.append(("DeepResearchLoopEngine", False))
    
    try:
        results.append(("ProgressVisualizer", test_progress_visualizer()))
    except Exception as e:
        print(f"❌ ProgressVisualizer 測試失敗：{e}")
        results.append(("ProgressVisualizer", False))
    
    try:
        results.append(("is_xfactor 字段", test_xfactor_field()))
    except Exception as e:
        print(f"❌ is_xfactor 字段測試失敗：{e}")
        results.append(("is_xfactor 字段", False))
    
    print("\n" + "=" * 60)
    print("測試結果摘要")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status} - {name}")
    
    print(f"\n總計：{passed}/{total} 通過")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
