import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# 颜色配置
# ============================================================
colors = {
    'primary': '#51999F',
    'secondary': '#4198AC',
    'light': '#7BC0CD',
    'accent1': '#DBCB92',
    'accent2': '#ECB66C',
    'accent3': '#EA9E58',
    'accent4': '#ED8D5A',
    'dark': '#2C3E50',
    'text': '#333333',
    'grid': '#E8E8E8'
}

# 设置全局样式
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12

sns.set_style("whitegrid")


# ============================================================
# 图2：区制系数对比柱状图（细柱子版本）
# ============================================================
def create_regime_comparison_plot():
    fig, ax = plt.subplots(figsize=(10, 7), facecolor='white')
    ax.set_facecolor('white')

    # 数据
    regimes = ['Low Regime\n(IT Talent ≤ 0.2387)', 'High Regime\n(IT Talent > 0.2387)']
    coefficients = [2.631011, -0.1035061]
    std_errors = [0.32, 0.030]
    p_values = [0.000, 0.012]
    sig_stars = ['***', '**']

    # 颜色
    bar_colors = [colors['accent3'], colors['primary']]

    # 绘制柱状图 - 柱子宽度改为0.35（原来0.6）
    bars = ax.bar(regimes, coefficients, width=0.38, color=bar_colors,
                  edgecolor='white', linewidth=2, alpha=0.85, zorder=3)

    # 添加误差线和标注
    for i, (bar, coef, err, p_val, star) in enumerate(zip(bars, coefficients, std_errors, p_values, sig_stars)):
        # 误差线
        ax.errorbar(i, coef, yerr=err, fmt='none', ecolor=colors['dark'],
                    elinewidth=2, capsize=10, capthick=2, zorder=4)

        # 系数值标签
        if coef >= 0:
            ax.text(i, coef + err + 0.12, f'{coef:.4f}',
                    ha='center', va='bottom', fontsize=13, fontweight='bold',
                    color=colors['dark'])
            ax.text(i, coef + err + 0.35, star,
                    ha='center', va='bottom', fontsize=14, fontweight='bold',
                    color=colors['accent4'])
            ax.text(i, coef + err + 0.58, f'(p = {p_val:.3f})',
                    ha='center', va='bottom', fontsize=10, style='italic',
                    color=colors['secondary'])
        else:
            ax.text(i, coef - err - 0.12, f'{coef:.4f}',
                    ha='center', va='top', fontsize=13, fontweight='bold',
                    color=colors['dark'])
            ax.text(i, coef - err - 0.32, star,
                    ha='center', va='top', fontsize=14, fontweight='bold',
                    color=colors['accent4'])
            ax.text(i, coef - err - 0.55, f'(p = {p_val:.3f})',
                    ha='center', va='top', fontsize=10, style='italic',
                    color=colors['secondary'])

    # 0参考线
    ax.axhline(y=0, color=colors['dark'], linewidth=1.5, linestyle='-', alpha=0.5, zorder=2)

    # 添加柱内背景渐变效果（适应细柱子）
    for i, (coef, color) in enumerate(zip(coefficients, bar_colors)):
        if coef > 0:
            ax.fill_between([i - 0.19, i + 0.19], 0, coef, alpha=0.1, color=color, zorder=1)
        else:
            ax.fill_between([i - 0.19, i + 0.19], coef, 0, alpha=0.1, color=color, zorder=1)

    # ===== 信息框 =====
    info_text = f"Threshold Effect Test Results (Excluding Extreme Samples):\n"
    info_text += f"  • Single-threshold Bootstrap Prob = 0.0067 (p < 0.01)\n"
    info_text += f"  • Threshold estimate = 0.2387\n"
    info_text += f"  • 95% CI = [0.2249, 0.2438]\n"
    info_text += f"  • Within R² = 0.5506"

    ax.text(0.97, 0.97, info_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['accent1'],
                      alpha=0.15, edgecolor=colors['accent1'], linewidth=1),
            color=colors['dark'], family='monospace')

    # ===== 坐标轴标签 =====
    ax.set_ylabel('Regression Coefficient', fontsize=13, fontweight='bold', color=colors['text'])
    ax.set_xlabel('IT Talent Agglomeration Regime', fontsize=13, fontweight='bold', color=colors['text'])
    ax.set_title('Regime-Specific Effects of IT Talent Agglomeration\n(After Excluding Extreme Samples)',
                 fontsize=14, fontweight='bold', pad=18, color=colors['dark'])

    # 设置y轴范围
    y_min = -0.5
    y_max = 3.5
    ax.set_ylim(y_min, y_max)

    # 添加y轴辅助线
    ax.axhline(y=1, color=colors['grid'], linewidth=0.8, linestyle=':', alpha=0.5)
    ax.axhline(y=2, color=colors['grid'], linewidth=0.8, linestyle=':', alpha=0.5)
    ax.axhline(y=3, color=colors['grid'], linewidth=0.8, linestyle=':', alpha=0.5)
    ax.axhline(y=-0.2, color=colors['grid'], linewidth=0.8, linestyle=':', alpha=0.5)

    # 坐标轴样式
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(colors['dark'])
    ax.spines['bottom'].set_color(colors['dark'])
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)

    # 网格
    ax.grid(True, axis='y', linestyle='--', alpha=0.25, color=colors['grid'], linewidth=0.8)

    # 设置x轴标签样式
    ax.set_xticklabels(regimes, fontsize=11, color=colors['dark'])

    plt.tight_layout()
    plt.savefig('regime_coefficients_plot.png', dpi=350, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.show()
    print("✓ Figure 2 saved: regime_coefficients_plot.png")


# ============================================================
# 运行图2
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Generating Figure 2: Regime Coefficient Comparison".center(60))
    print("=" * 60)
    create_regime_comparison_plot()
    print("\n✓ Figure 2 completed!")