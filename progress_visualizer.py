"""
World Cup 2026 Progress Visualizer
生成進度圖表（bar chart）
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
from typing import Dict, List, Any, Optional
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ProgressVisualizer:
    """
    進度可視化器
    生成 bar chart 追蹤迭代進度
    """
    
    def __init__(self, output_dir: str = "data/visualizations"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
    
    def generate_bar_chart(
        self,
        data: Dict[str, Any],
        title: str,
        target: Optional[Dict[str, float]] = None,
        figsize: tuple = (12, 6)
    ) -> plt.Figure:
        """
        生成 bar chart
        
        Args:
            data: 數據字典，key 為標籤，value 為數值
            title: 圖表標題
            target: 目標值字典（可選）
            figsize: 圖表大小
        
        Returns:
            matplotlib Figure 對象
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        labels = list(data.keys())
        values = list(data.values())
        
        colors = []
        for i, label in enumerate(labels):
            if target and label in target:
                if values[i] >= target[label]:
                    colors.append('#2ecc71')
                else:
                    colors.append('#3498db')
            else:
                colors.append('#3498db')
        
        bars = ax.bar(labels, values, color=colors, edgecolor='black', linewidth=1.2)
        
        if target:
            for i, label in enumerate(labels):
                if label in target:
                    ax.axhline(y=target[label], color='red', linestyle='--', linewidth=1.5, 
                              xmin=(i + 0.1) / len(labels), xmax=(i + 0.9) / len(labels))
        
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.annotate(f'{value:.1f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       fontsize=10, fontweight='bold')
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('指標', fontsize=12)
        ax.set_ylabel('數值', fontsize=12)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        logger.info(f"已生成 bar chart：{title}")
        return fig
    
    def generate_progress_chart(
        self,
        iteration_history: List[Dict[str, Any]],
        title: str = "迭代進度追蹤"
    ) -> plt.Figure:
        """
        生成迭代進度折線圖
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        iterations = [h['iteration'] for h in iteration_history]
        news = [h['news_collected'] for h in iteration_history]
        xfactor = [h['xfactor_identified'] for h in iteration_history]
        accuracy = [h['accuracy'] * 100 for h in iteration_history]
        
        ax1 = axes[0, 0]
        ax1.plot(iterations, news, 'b-o', linewidth=2, markersize=4)
        ax1.fill_between(iterations, news, alpha=0.3)
        ax1.set_title('新聞收集進度', fontsize=12, fontweight='bold')
        ax1.set_xlabel('迭代次數')
        ax1.set_ylabel('新聞數量')
        ax1.grid(True, alpha=0.3)
        
        ax2 = axes[0, 1]
        ax2.plot(iterations, xfactor, 'g-o', linewidth=2, markersize=4)
        ax2.fill_between(iterations, xfactor, alpha=0.3, color='green')
        ax2.set_title('X-Factor 識別進度', fontsize=12, fontweight='bold')
        ax2.set_xlabel('迭代次數')
        ax2.set_ylabel('X-Factor 數量')
        ax2.grid(True, alpha=0.3)
        
        ax3 = axes[1, 0]
        ax3.plot(iterations, accuracy, 'r-o', linewidth=2, markersize=4)
        ax3.fill_between(iterations, accuracy, alpha=0.3, color='red')
        ax3.set_title('準確率變化', fontsize=12, fontweight='bold')
        ax3.set_xlabel('迭代次數')
        ax3.set_ylabel('準確率 (%)')
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim(0, 100)
        
        ax4 = axes[1, 1]
        cumulative_news = np.cumsum(news)
        cumulative_xfactor = np.cumsum(xfactor)
        ax4.plot(iterations, cumulative_news, 'b-', linewidth=2, label='累計新聞')
        ax4.plot(iterations, cumulative_xfactor, 'g-', linewidth=2, label='累計 X-Factor')
        ax4.set_title('累計進度', fontsize=12, fontweight='bold')
        ax4.set_xlabel('迭代次數')
        ax4.set_ylabel('累計數量')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        logger.info(f"已生成進度折線圖：{title}")
        return fig
    
    def save_chart(self, fig: plt.Figure, filename: str) -> str:
        """
        保存圖片
        
        Args:
            fig: matplotlib Figure 對象
            filename: 文件名（不含路徑）
        
        Returns:
            保存的完整路徑
        """
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        
        logger.info(f"圖表已保存：{filepath}")
        return filepath
    
    def generate_summary_dashboard(
        self,
        summary: Dict[str, Any],
        targets: Dict[str, Any]
    ) -> plt.Figure:
        """
        生成摘要儀表板
        """
        fig = plt.figure(figsize=(16, 10))
        
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        ax1 = fig.add_subplot(gs[0, :])
        metrics = ['迭代次數', 'X-Factor', '新聞數', '準確率(%)']
        actual = [
            summary.get('total_iterations', 0),
            summary.get('total_xfactor', 0),
            summary.get('total_news', 0),
            summary.get('final_accuracy', 0) * 100
        ]
        target_vals = [
            targets.get('iterations', 100),
            targets.get('xfactor', 30),
            targets.get('news', 10000),
            targets.get('accuracy', 0.75) * 100
        ]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, actual, width, label='實際', color='#3498db')
        bars2 = ax1.bar(x + width/2, target_vals, width, label='目標', color='#e74c3c', alpha=0.7)
        
        ax1.set_ylabel('數值')
        ax1.set_title('目標達成對比', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(metrics)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        for bar in bars1:
            height = bar.get_height()
            ax1.annotate(f'{height:.0f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=9)
        
        ax2 = fig.add_subplot(gs[1, 0])
        progress = [
            min(100, actual[0] / target_vals[0] * 100),
            min(100, actual[1] / target_vals[1] * 100),
            min(100, actual[2] / target_vals[2] * 100),
            min(100, actual[3] / target_vals[3] * 100)
        ]
        colors = ['#2ecc71' if p >= 100 else '#3498db' for p in progress]
        ax2.barh(metrics, progress, color=colors)
        ax2.axvline(x=100, color='red', linestyle='--', linewidth=1.5)
        ax2.set_xlabel('完成度 (%)')
        ax2.set_title('目標完成度', fontsize=12, fontweight='bold')
        ax2.set_xlim(0, 120)
        
        ax3 = fig.add_subplot(gs[1, 1])
        time_hours = summary.get('total_time_hours', 0)
        time_data = [time_hours, 8.0 - time_hours]
        time_labels = ['已用時間', '剩餘時間']
        time_colors = ['#e74c3c', '#95a5a6']
        ax3.pie(time_data, labels=time_labels, colors=time_colors, autopct='%1.1f%%',
               startangle=90)
        ax3.set_title(f'時間使用（總計 {time_hours:.2f} 小時）', fontsize=12, fontweight='bold')
        
        ax4 = fig.add_subplot(gs[1, 2])
        achieved = sum([
            1 for k, v in targets.items() if 
            (k == 'iterations' and summary.get('total_iterations', 0) >= v) or
            (k == 'xfactor' and summary.get('total_xfactor', 0) >= v) or
            (k == 'news' and summary.get('total_news', 0) >= v) or
            (k == 'accuracy' and summary.get('final_accuracy', 0) >= v)
        ])
        total = len(targets)
        not_achieved = total - achieved
        
        status_data = [achieved, not_achieved]
        status_labels = ['已達成', '未達成']
        status_colors = ['#2ecc71', '#e74c3c']
        ax4.pie(status_data, labels=status_labels, colors=status_colors, autopct='%1.0f%%',
               startangle=90)
        ax4.set_title(f'目標達成狀態（{achieved}/{total}）', fontsize=12, fontweight='bold')
        
        ax5 = fig.add_subplot(gs[2, :])
        ax5.axis('off')
        
        info_text = f"""
        ========== World Cup 2026 深度研究循環摘要 ==========
        
        📊 總迭代次數：{summary.get('total_iterations', 0)}
        ⏱️ 總運行時間：{summary.get('total_time_hours', 0):.2f} 小時
        📰 總新聞數：{summary.get('total_news', 0)}
        ⭐ 總 X-Factor：{summary.get('total_xfactor', 0)}
        🎯 最終準確率：{summary.get('final_accuracy', 0)*100:.2f}%
        
        生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        ax5.text(0.5, 0.5, info_text, transform=ax5.transAxes,
                fontsize=11, verticalalignment='center', horizontalalignment='center',
                fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        fig.suptitle('World Cup 2026 深度研究循環儀表板', fontsize=16, fontweight='bold', y=0.98)
        
        logger.info("已生成摘要儀表板")
        return fig


if __name__ == "__main__":
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
    visualizer.save_chart(fig1, "target_achievement.png")
    
    print("ProgressVisualizer 測試完成")
