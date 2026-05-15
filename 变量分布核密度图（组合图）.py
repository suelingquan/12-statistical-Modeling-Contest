import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 读取数据
# ============================================================
data = pd.read_excel(r'D:\Sueling\项目-比赛\12统模\centered_data.xlsx')

print("数据行数：", len(data))
print("变量列表：", data.columns.tolist())

# ============================================================
# 关键修正：只选择需要绘制的数值变量，排除 city 和 year
# ============================================================
# 需要绘制的变量列表
plot_vars = ['ln_Patent1', 'IT_Talent', 'ln_pgdp_c', 'Industry',
             'Gov', 'FDI_Ratio', 'ln_Internet_pc_c', 'ln_Student_pc_c']

# 只保留这些变量
data_plot = data[plot_vars].copy()

# 将数据转为长格式
data_long = data_plot.melt(var_name='变量', value_name='值')

# 变量中文标签映射
variable_labels = {
    'ln_Patent1': '创新产出',
    'IT_Talent': 'IT人才集聚度',
    'ln_pgdp_c': '经济发展水平',
    'Industry': '产业结构',
    'Gov': '政府支持',
    'FDI_Ratio': '外资依存度',
    'ln_Internet_pc_c': '数字基础设施',
    'ln_Student_pc_c': '人力资本'
}
data_long['变量名'] = data_long['变量'].map(variable_labels)

# 检查数据
print("\n数据长格式预览：")
print(data_long.head())
print("\n变量名唯一值：", data_long['变量名'].unique())

# ============================================================
# 绘制小提琴图 + 箱线图叠加
# ============================================================
fig, ax = plt.subplots(figsize=(14, 6))

# 使用 hue 参数避免类型问题
sns.violinplot(data=data_long, x='变量名', y='值', ax=ax,
               inner='box', linewidth=1, palette='Set2', cut=0)

ax.set_title('变量分布特征：小提琴图（含箱线图）', fontsize=14, fontweight='bold')
ax.set_xlabel('变量', fontsize=12)
ax.set_ylabel('取值', fontsize=12)
ax.tick_params(axis='x', rotation=45)
ax.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('小提琴图.png', dpi=300, bbox_inches='tight')
plt.show()