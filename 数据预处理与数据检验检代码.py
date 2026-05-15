#数据文件：centered_data.xlsx
import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy.stats import chi2, norm
import warnings
warnings.filterwarnings('ignore')
# ====================== 1. 读取数据 ======================
df = pd.read_excel('centered_data.xlsx')
df['city'] = df['city'].astype('category')
df['year'] = df['year'].astype(int)
df = df.set_index(['city', 'year']).sort_index()
print("数据形状:", df.shape)
# ====================== 2. 异常值处理======================
def winsorize(df, cols, limits=(0.01, 0.01)):
    for col in cols:
        low, high = df[col].quantile([limits[0], 1-limits[1]]).values
        df[col] = df[col].clip(low, high)
    return df
# 需要缩尾的变量
cols_win = ['IT_Talent', 'Industry', 'Gov', 'FDI_Ratio', 'ln_Student_pc_c']
df_wins = winsorize(df.copy(), cols_win)
print("缩尾完成（1% 和 99% 分位）")
# ====================== 3. 多重共线性=====================
def demean(arr, groups):
    """组内去均值"""
    out = np.empty_like(arr)
    for g in np.unique(groups):
        idx = (groups == g)
        out[idx] = arr[idx] - arr[idx].mean()
    return out
# 选择自变量
X_vars = ['IT_Talent', 'ln_pgdp_c', 'Industry', 'Gov', 'FDI_Ratio', 'ln_Internet_pc_c', 'ln_Student_pc_c']
X = df_wins[X_vars].dropna()
cities = X.index.get_level_values('city').values
X_demeaned = np.column_stack([demean(X[var].values, cities) for var in X_vars])
vif = [variance_inflation_factor(X_demeaned, i) for i in range(X_demeaned.shape[1])]
vif_df = pd.DataFrame({'Variable': X_vars, 'VIF': vif})
print("\n多重共线性 VIF：")
print(vif_df)
# ====================== 4. 截面相关性======================
from linearmodels.panel import PanelOLS
y = df_wins['ln_Patent1']
X_fe = df_wins[['IT_Talent'] + X_vars[1:]]
model = PanelOLS(y, X_fe, entity_effects=True, time_effects=True)
res = model.fit()
resid = res.resids
# 将残差转换为宽格式
resid_df = resid.reset_index().pivot(index='year', columns='city', values='residual')
T, N = resid_df.shape
corr_mat = resid_df.corr().values
# 计算CD统计量
cd = np.sqrt(2*T/(N*(N-1))) * np.sum(corr_mat[np.triu_indices(N, k=1)])
p_cd = 2*(1 - norm.cdf(abs(cd)))
print(f"\n截面相关检验（Pesaran CD）: CD = {cd:.4f}, p = {p_cd:.4f}")
if p_cd < 0.05:
    print("→ 存在显著截面相关，建议使用聚类稳健标准误")
else:
    print("→ 未发现显著截面相关")
# ====================== 5. 面板单位根======================
from statsmodels.tsa.stattools import adfuller
def panel_adf_fisher(df, var):
    """计算ADF检验p值，然后组合Fisher统计量"""
    p_vals = []
    for city in df.index.get_level_values('city').unique():
        ser = df.xs(city, level='city')[var].dropna()
        if len(ser) < 3:
            continue
        ser_demeaned = ser - ser.mean()
        p = adfuller(ser_demeaned, maxlag=1, autolag=None)[1]
        p_vals.append(p)
    if not p_vals:
        return np.nan, np.nan
    fisher_stat = -2 * np.sum(np.log(p_vals))
    dof = 2 * len(p_vals)
    p_fisher = 1 - chi2.cdf(fisher_stat, dof)
    return fisher_stat, p_fisher
print("\n面板单位根检验（ADF-Fisher，个体去均值后）:")
for var in ['ln_Patent1', 'IT_Talent'] + X_vars[1:]:
    stat, p = panel_adf_fisher(df_wins, var)
    if not np.isnan(stat):
        print(f"{var:20s}: Fisher统计量 = {stat:.2f}, p = {p:.4f} -> {'平稳' if p<0.05 else '不平稳'}")
else:
  print(f"{var:20s}: 数据不足，跳过")
print("\n数据预处理与检验完成。")