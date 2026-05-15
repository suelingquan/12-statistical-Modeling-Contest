import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 数据（高能级城市 vs 一般地级市）
categories = ['IT人才\n集聚度', '创新产出', '经济发展\n水平', '产业结构',
              '政府支持', '外资\n依存度', '数字\n基础设施', '人力资本']
high_city = [0.46, 1.00, 0.85, 0.62, 0.58, 0.45, 0.78, 0.82]
normal_city = [0.12, 0.80, 0.62, 0.55, 0.52, 0.48, 0.60, 0.58]

# 闭合数据
high_city += high_city[:1]
normal_city += normal_city[:1]
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]

# 绘图
fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))

# 设置背景网格
ax.set_theta_offset(0)
ax.set_theta_direction(1)

# 绘制
ax.plot(angles, high_city, 'o-', linewidth=2, label='高能级城市', color='#ECB66C')
ax.fill(angles, high_city, alpha=0.25, color='#ECB66C')
ax.plot(angles, normal_city, 'o-', linewidth=2, label='一般地级市', color='#51999F')
ax.fill(angles, normal_city, alpha=0.25, color='#51999F')

# 关键：设置刻度标签并解决中文显示问题
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=10, fontweight='bold')
ax.set_ylim(0, 1.1)
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=9)

ax.set_title('城市指标组间对比雷达图', fontsize=14, fontweight='bold', pad=30)
ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.05), fontsize=11)

plt.tight_layout()
plt.savefig('雷达图.png', dpi=300, bbox_inches='tight')
plt.show()