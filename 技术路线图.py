import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(12, 16))
ax.set_xlim(0, 10)
ax.set_ylim(0, 20)
ax.axis('off')

# 节点坐标和内容
nodes = [
    (5, 18.5, "第一阶段：理论准备与文献梳理\n• 人才集聚与创新产出：从线性促进到非线性反思\n• 门槛效应、拥挤效应、知识溢出机制\n• 提出研究假设：存在显著单门槛效应"),
    (5, 15.5, "第二阶段：数据收集与变量构建\n• 样本：长三角26城，2014-2023年\n• 被解释变量：ln(发明专利授权数+1)\n• 核心解释变量/门槛变量：IT人才集聚度\n• 控制变量：经济、产业、政府、开放、数字基建、人力资本"),
    (5, 11.5, "第三阶段：实证分析流程\n• 基准回归（双向固定效应模型）\n• 面板门槛效应检验（Hansen, 1999）\n• 分区制回归与机制解释\n• 异质性分析（城市能级、创新维度）\n• 稳健性检验（调节效应、剔除样本、分时段、全变量滞后）"),
    (5, 7, "第四阶段：结论提炼与政策启示\n• 核心发现：显著单门槛效应，低区制抑制，高区制弱促进\n• 理论贡献：揭示线性不显著背后的非线性机制\n• 政策建议：识阈分类、因城施策")
]

for x, y, text in nodes:
    rect = patches.FancyBboxPatch((x-4.5, y-0.8), 9, 1.6, boxstyle="round,pad=0.1",
                                    facecolor='lightblue', edgecolor='navy', linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold')

# 添加箭头
for i in range(len(nodes)-1):
    ax.annotate('', xy=(5, nodes[i+1][1]+0.8), xytext=(5, nodes[i][1]-0.8),
                arrowprops=dict(arrowstyle='->', color='gray', lw=2))

ax.set_title("技术路线图", fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('技术路线图.png', dpi=300, bbox_inches='tight')
plt.show()