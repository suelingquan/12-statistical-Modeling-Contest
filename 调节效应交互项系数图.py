import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 方法1：直接使用论文中的系数（无需读取Excel文件）
# ============================================================

# 数据（根据你论文中的表10填写）
moderators = ['政府支持 (Gov)', '数字基础设施 (Internet)', '对外开放 (FDI)']
coefs = [18.5840, 0.0782, 2.5736]  # 交互项系数
p_values = [0.001, 0.125, 0.292]  # p值
ci_low = [8.9171, -0.0233, -2.4422]  # 95%置信区间下限
ci_high = [28.2509, 0.1797, 7.5894]  # 95%置信区间上限

# 根据显著性设置颜色
colors = []
for p in p_values:
    if p < 0.01:
        colors.append('darkgreen')
    elif p < 0.05:
        colors.append('lightgreen')
    elif p < 0.1:
        colors.append('orange')
    else:
        colors.append('gray')

# 绘图
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(moderators, coefs, color=colors, edgecolor='black', linewidth=1.2)

# 添加误差线（置信区间）
ax.errorbar(moderators, coefs,
            yerr=[np.array(coefs) - np.array(ci_low), np.array(ci_high) - np.array(coefs)],
            fmt='none', ecolor='black', capsize=5, elinewidth=1.5)

# 添加显著性标注
for bar, coef, p in zip(bars, coefs, p_values):
    if p < 0.01:
        sig_text = '***'
    elif p < 0.05:
        sig_text = '**'
    elif p < 0.1:
        sig_text = '*'
    else:
        sig_text = 'n.s.'

    y_pos = bar.get_height()
    offset = 0.5 if y_pos >= 0 else -1.5
    va = 'bottom' if y_pos >= 0 else 'top'
    ax.text(bar.get_x() + bar.get_width() / 2, y_pos + offset,
            f'{coef:.3f} {sig_text}', ha='center', va=va,
            fontsize=10, fontweight='bold')

# 添加参考线
ax.axhline(y=0, linestyle='--', color='red', alpha=0.7, linewidth=1.5)

# 设置标签和标题
ax.set_ylabel('交互项系数 (IT × 调节变量)', fontsize=12)
ax.set_xlabel('调节变量', fontsize=12)
ax.set_title('调节效应交互项系数及95%置信区间', fontsize=14, fontweight='bold')
ax.grid(True, axis='y', alpha=0.3)

# 添加显著性图例说明
ax.text(0.98, 0.95, '显著性水平：*** p<0.01  ** p<0.05  * p<0.1  n.s. 不显著',
        transform=ax.transAxes, ha='right', va='top', fontsize=9,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('调节效应交互项系数图.png', dpi=300, bbox_inches='tight')
plt.show()