"""
内生性检验：2SLS回归（完整版，无报错）
"""

import pandas as pd
import numpy as np
from linearmodels.iv import IV2SLS
from linearmodels.panel import PanelOLS
import os

#1. 读取数据
file_path = r'centered_data.xlsx'
df = pd.read_excel(file_path)
print(f"原始数据形状: {df.shape}")

# 设置面板索引
df = df.set_index(['city', 'year'])
df = df.sort_index()

# 2. 生成滞后变量
df['L_IT_Talent'] = df.groupby('city')['IT_Talent'].shift(1)
df_clean = df.dropna()
print(f"清洗后样本量: {len(df_clean)}")

# 3. 2SLS回归
iv_model = IV2SLS.from_formula(
    'ln_Patent1 ~ ln_pgdp_c + Industry + Gov + FDI_Ratio + ln_Internet_pc_c + ln_Student_pc_c + [IT_Talent ~ L_IT_Talent]',
    data=df_clean
)
iv_result = iv_model.fit(cov_type='robust')

# 4. 输出结果
print("\n" + "="*70)
print("2SLS估计结果（内生性检验）")
print("="*70)
print(iv_result)

# 5. 结果表格
results_df = pd.DataFrame({
    '变量': iv_result.params.index,
    '系数': iv_result.params.values,
    '标准误': iv_result.std_errors.values,
    't值': iv_result.tstats.values,
    'P值': iv_result.pvalues.values
})
results_df['显著性'] = results_df['P值'].apply(
    lambda x: '***' if x < 0.001 else ('**' if x < 0.01 else ('*' if x < 0.05 else ''))
)

print("\n" + "="*70)
print("完整结果表")
print("="*70)
print(results_df.to_string(index=False))

# ========== 6. 诊断性检验 ==========
print("\n" + "="*70)
print("诊断性检验")
print("="*70)

# 获取第一阶段结果
first_stage = iv_result.first_stage
if first_stage is not None:
    # 获取内生变量的第一阶段统计量
    # first_stage 是一个字典，键是内生变量名
    endog_names = list(first_stage.params.columns) if hasattr(first_stage.params, 'columns') else []
    print(f"内生变量: {endog_names}")

    # 计算F统计量
    for endog in endog_names:
        if endog in first_stage.rsquared:
            rsq = first_stage.rsquared[endog]
            n = len(df_clean)
            k = first_stage.params.shape[0] - 1  # 工具变量个数
            f_stat = (rsq / (1 - rsq)) * ((n - k - 1) / k) if rsq < 1 else 999
            print(f"\n第一阶段（{endog}）:")
            print(f"  R² = {rsq:.4f}")
            print(f"  F统计量 = {f_stat:.2f}")
            if f_stat > 10:
                print("  结论: F > 10，不存在弱工具变量问题 ")
            else:
                print("  结论: F < 10，可能存在弱工具变量问题 ")

# J统计量
print(f"\nHansen J统计量: {iv_result.j_stat.stat:.4f}")
print(f"Hansen J p值: {iv_result.j_stat.pval:.4f}")
if iv_result.j_stat.pval > 0.05:
    print("结论: p > 0.05，工具变量外生性成立 ")
else:
    print("结论: p < 0.05，工具变量可能存在外生性问题 ")

# ========== 7. 与OLS对比 ==========
print("\n" + "="*70)
print("与基准OLS（双向固定效应）对比")
print("="*70)

ols_model = PanelOLS(df_clean['ln_Patent1'],
                     df_clean[['IT_Talent', 'ln_pgdp_c', 'Industry', 'Gov',
                               'FDI_Ratio', 'ln_Internet_pc_c', 'ln_Student_pc_c']],
                     entity_effects=True, time_effects=True)
ols_result = ols_model.fit(cov_type='clustered', cluster_entity=True)

print(f"\nOLS（固定效应）: IT_Talent系数 = {ols_result.params['IT_Talent']:.4f}, P值 = {ols_result.pvalues['IT_Talent']:.4f}")
print(f"2SLS（工具变量）: IT_Talent系数 = {iv_result.params['IT_Talent']:.4f}, P值 = {iv_result.pvalues['IT_Talent']:.4f}")

diff = iv_result.params['IT_Talent'] - ols_result.params['IT_Talent']
print(f"\n系数差异 (2SLS - OLS): {diff:.4f}")


results_df.to_excel('2sls_results.xlsx', index=False)
print("\n结果已保存到 2sls_results.xlsx")

# 9. 生成论文用表格
print("\n" + "="*70)
print("【可直接复制到Word的表格】")
print("="*70)

print("\n表X 2SLS估计结果（内生性检验）")
print("-" * 70)
print(f"{'变量':<20} {'系数':<12} {'标准误':<12} {'t值':<10} {'P值':<10}")
print("-" * 70)

for _, row in results_df.iterrows():
    # 添加显著性星号
    sig = row['显著性']
    coef_str = f"{row['系数']:.4f}{sig}"
    print(f"{row['变量']:<20} {coef_str:<12} {row['标准误']:<12.4f} {row['t值']:<10.2f} {row['P值']:<10.4f}")

print("-" * 70)
print("注：*** p<0.001, ** p<0.01, * p<0.05；工具变量为L.IT_Talent；")

print("\n" + "="*70)
print("【可直接复制到论文的文字描述】")
print("="*70)


print("\n" + "="*70)
print("分析完成！")
print("="*70)