import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# ========== 1. 读取数据 ==========
df = pd.read_excel('centered_data.xlsx', sheet_name='Sheet1')

# ========== 2. 计算各年度均值 ==========
yearly_mean = df.groupby('year')[['IT_Talent', 'ln_Patent1']].mean().reset_index()

# ========== 色组定义 ==========
# 主色调渐变序列
color_gradient = ['#BFDFD2', '#7BC0CD', '#4198AC', '#51999F']  # 浅到深蓝绿系
# 辅助暖色（可用于标签或强调）
warm_colors = ['#DBCB92', '#ECB66C', '#EA9E58', '#ED8D5A']

# ========== 3. 绘制双轴趋势图 ==========
fig, ax1 = plt.subplots(figsize=(12, 6), facecolor='white')

# 左y轴：IT_Talent（IT人才集聚度）
# 使用渐变色：颜色随年份从浅到深
years = yearly_mean['year'].values
it_talent = yearly_mean['IT_Talent'].values

# 为每个线段分配颜色（渐变效果）
for i in range(len(years) - 1):
    # 根据年份位置计算颜色比例
    t = (years[i] - 2014) / (2023 - 2014)
    color_idx = t * len(color_gradient)
    # 在渐变色序列中插值取色
    if color_idx <= 1:
        color = color_gradient[0]
    elif color_idx <= 2:
        color = color_gradient[1]
    elif color_idx <= 3:
        color = color_gradient[2]
    else:
        color = color_gradient[3]

    ax1.plot(years[i:i + 2], it_talent[i:i + 2],
             color=color, linewidth=2.5, alpha=0.9)

# 添加数据点
scatter1 = ax1.scatter(years, it_talent, c=years, cmap='Blues',
                       s=60, zorder=5, edgecolor='white', linewidth=1.5)
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('IT Talent Agglomeration (%)', fontsize=12, color='#2c5f6e')
ax1.tick_params(axis='y', labelcolor='#2c5f6e')
ax1.set_xticks(years)
ax1.set_xticklabels(years, rotation=45)

# 右y轴：ln_Patent1（创新产出）
ax2 = ax1.twinx()
ln_patent = yearly_mean['ln_Patent1'].values

for i in range(len(years) - 1):
    t = (years[i] - 2014) / (2023 - 2014)
    if t < 0.25:
        color = warm_colors[0]
    elif t < 0.5:
        color = warm_colors[1]
    elif t < 0.75:
        color = warm_colors[2]
    else:
        color = warm_colors[3]

    ax2.plot(years[i:i + 2], ln_patent[i:i + 2],
             color=color, linewidth=2.5, alpha=0.9, linestyle='--')

scatter2 = ax2.scatter(years, ln_patent, c=years, cmap='Oranges',
                       s=60, zorder=5, edgecolor='white', linewidth=1.5, marker='s')
ax2.set_ylabel('Innovation Output (ln_Patent)', fontsize=12, color='#c46a3a')
ax2.tick_params(axis='y', labelcolor='#c46a3a')

# 标题
plt.title('IT Talent Agglomeration and Innovation Output Trends (2014-2023)',
          fontsize=14, fontweight='bold', pad=15)

# 图例（自定义）
legend_elements = [
    Line2D([0], [0], color=color_gradient[0], linewidth=2.5, label='IT Talent Agglomeration'),
    Line2D([0], [0], color=warm_colors[0], linewidth=2.5, linestyle='--', label='Innovation Output')
]
ax1.legend(handles=legend_elements, loc='upper left', fontsize=10, frameon=True, fancybox=True)

# 网格
ax1.grid(True, linestyle=':', alpha=0.3, axis='y')
ax1.set_axisbelow(True)

# 设置y轴范围（根据数据调整）
ax1.set_ylim(0, 6.5)
ax2.set_ylim(7, 10.5)

# 装饰：背景色
ax1.set_facecolor('#FAFAFA')
fig.patch.set_facecolor('white')

plt.tight_layout()
plt.savefig('IT_talent_innovation_trend.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# ========== 4. 打印年度数据 ==========
print("=" * 60)
print("年度均值数据")
print("=" * 60)
print(yearly_mean.round(4))