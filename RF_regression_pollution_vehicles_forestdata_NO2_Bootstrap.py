# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 10:53:22 2024

@author: Qianqian Yang
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression

import statsmodels.api as sm

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

city1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,21,22,24]

city2 = [14,18,19,20,23,25,26,28,29,30,31,32,33,34,35,36,38,40,41,46,50,51,53,54,56,58,69,73,85,97]

city12 = city1 + city2

city3 = [27,37,39,43,44,45,47,48,52,55,57,59,60,61,62,63,64,65,66,67,70,71,72,74,75,77,78,80,82,83,84,86,88,89,90,91,92,93,94,96,98,100,\
          101,102,103,104,105,106,108,109,110,112,119,121,125,128,131,132,135,137,144,145,149]
    
city4 = [42,49,68,76,79,81,87,95,99,107,111,113,114,115,116,117,118,120,122,123,124,126,127,129,130,133,136,138,139,140,141,143,146,147,\
          148,150,134,142]

city34 = city3 + city4

# file1 = r'D:\3MTDNN_v2.0\Yearly_scale_experiments\Yearly_retrievals_analysis\vehicle_data_analysis\Matchpair_air_polutants_vehicles_meteorological_forest_2023_fillnan.xlsx'

# file1 = r'D:\3MTDNN_v2.0\Yearly_scale_experiments\Yearly_retrievals_analysis\vehicle_data_analysis\Matchpair_air_polutants_vehicles_meteorological_forest_2023_fillnan_correct_vehicle_data.xlsx'

# file1 = r'D:\3MTDNN_v2.0\Yearly_scale_experiments\Yearly_retrievals_analysis\vehicle_data_analysis\Matchpair_air_polutants_vehicles_meteorological_forest_crop_grass_impervious_2023_fillnan_v3.xlsx'
file1 = r'D:\3MTDNN_v2.0\Yearly_scale_experiments\Yearly_retrievals_analysis\vehicle_data_analysis\Matchpair_air_polutants_vehicles_meteorological_forest_crop_grass_impervious_barren_2023_fillnan_v3.xlsx'


excel_file1 = pd.ExcelFile(file1)
df0 = pd.read_excel(excel_file1)

df1 = df0[df0['city'].isin(city1)]
df2 = df0[df0['city'].isin(city2)]
df3 = df0[df0['city'].isin(city3)]
df4 = df0[df0['city'].isin(city4)]

df12 = df0[df0['city'].isin(city12)]
df34 = df0[df0['city'].isin(city34)]

df = df0.dropna(axis=0,how='any')

data1 = df.to_numpy()

citypm25 = df['PM25_city'].to_numpy()
cityno2 = df['NO2_city'].to_numpy()
cityco = df['CO_city'].to_numpy()

forestpm25 = df['PM25_forest'].to_numpy()
forestno2 = df['NO2_forest'].to_numpy()
forestco = df['CO_forest'].to_numpy()

barrenpm25 = df['PM25_barren'].to_numpy()
barrenno2 = df['NO2_barren'].to_numpy()
barrenco = df['CO_barren'].to_numpy()

# croppm25 = df['PM25_crop'].to_numpy()
# cropno2 = df['NO2_crop'].to_numpy()
# cropco = df['CO_crop'].to_numpy()

# grasspm25 = df['PM25_grass'].to_numpy()
# grassno2 = df['NO2_grass'].to_numpy()
# grassco = df['CO_grass'].to_numpy()

# imperviouspm25 = df['PM25_impervious'].to_numpy()
# imperviousno2 = df['NO2_impervious'].to_numpy()
# imperviousco = df['CO_impervious'].to_numpy()

citynum = df['city'].to_numpy()

nevehicle = df['NEvehicle'].to_numpy()
vehicle = df['vehicle'].to_numpy()
tvehicle = df['fuelvehicle'].to_numpy() 
nevratio = nevehicle/vehicle

roadpm25 = df['PM25_road'].to_numpy()
roadno2 = df['NO2_road'].to_numpy()
roadco = df['CO_road'].to_numpy()

# bgc2 = cityno2*2 - imperviousno2
# bgc3 = (cropno2 + forestno2 + grassno2)/3

# x = np.hstack((forestno2.reshape(-1,1), tvehicle.reshape(-1,1), nevehicle.reshape(-1,1), data1[:,14:19]))
x = np.hstack((barrenno2.reshape(-1,1), tvehicle.reshape(-1,1), nevehicle.reshape(-1,1), data1[:,14:19]))
# x = np.hstack((forestno2.reshape(-1,1), tvehicle.reshape(-1,1), nevehicle.reshape(-1,1), data1[:,14:19]))
# x = np.hstack((bgc2.reshape(-1,1), vehicle.reshape(-1,1), nevehicle.reshape(-1,1), data1[:,14:19]))
# x = np.hstack((bgc3.reshape(-1,1), vehicle.reshape(-1,1), nevehicle.reshape(-1,1), data1[:,14:19]))

# x = np.hstack((tvehicle.reshape(-1,1), nevehicle.reshape(-1,1), data1[:,14:19]))
# x = np.hstack((vehicle.reshape(-1,1), nevratio.reshape(-1,1), data1[:,14:19]))
nan_rows = np.any(np.isnan(x), axis=1)
# 删除含有 NaN 的行
x = x[~nan_rows]

# x1 = np.hstack((forestno2.reshape(-1,1), tvehicle.reshape(-1,1), nevehicle.reshape(-1,1), data1[:,14:19]))
x1 = np.hstack((barrenno2.reshape(-1,1), tvehicle.reshape(-1,1), nevehicle.reshape(-1,1), data1[:,14:19]))
# x1 = np.hstack((bgc2.reshape(-1,1), vehicle.reshape(-1,1), nevehicle.reshape(-1,1), data1[:,14:19]))
# x1 = np.hstack((bgc3.reshape(-1,1), vehicle.reshape(-1,1), nevehicle.reshape(-1,1), data1[:,14:19]))
# x1 = np.hstack((vehicle.reshape(-1,1), nevratio.reshape(-1,1), data1[:,14:19]))
# x1 = np.hstack((forestno2.reshape(-1,1), vehicle.reshape(-1,1), nevratio.reshape(-1,1), data1[:,14:19]))

scaler = MinMaxScaler()
x_norm = scaler.fit_transform(x)

y = roadno2
y = y[~nan_rows]

# feature_names = ['forest_NO2', 'fuelvehicle', 'NEV', 't2m', 'd2m', 'sp', 'u10', 'v10']
feature_names = ['BGC','FV', 'NEV', 'T2M', 'D2M', 'SP', 'U10', 'V10']
# feature_names = ['VE', 'RN', 'T2M', 'D2M', 'SP', 'U10', 'V10']
# feature_names = ['BGC', 'VE', 'RN', 'T2M', 'D2M', 'SP', 'U10', 'V10']

df_x = pd.DataFrame(x, columns=feature_names)
df_y = pd.DataFrame(y.reshape(-1,1), columns=['road_NO2'])

# 将数据划分为训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 创建随机森林回归模型
rf = RandomForestRegressor(n_estimators=200,min_samples_split = 2, random_state=42)

# 训练模型
# rf.fit(x_train, y_train)
rf.fit(df_x, df_y)

# 模型重要性
feature_importances = rf.feature_importances_


# --------构造模拟情境下x并预测-------------
newx = x1
newx[:,1]=x1[:,1]+x1[:,2]
newx[:,2]=x1[:,2]-x1[:,2]

df_newx = pd.DataFrame(newx, columns=feature_names)

newpre = rf.predict(df_newx)

# -------------------------十折交叉验证---------------------------------#
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split, KFold

def cross_validate_and_plot(model, x, y, n_splits=10, random_state=42):
    # 初始化 KFold
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    # 初始化存储评价指标的列表
    r2_scores = []
    rmse_scores = []
    mae_scores = []
    mape_scores = []

    # 存储所有的真实值和预测值
    all_y_true = []
    all_y_pred = []

    # 进行 K 折交叉验证
    for train_index, test_index in kf.split(x):
        x_cv_train, x_cv_test = x[train_index], x[test_index]
        y_cv_train, y_cv_test = y[train_index], y[test_index]

        # 训练模型并进行预测
        model.fit(x_cv_train, y_cv_train)
        y_predcv = model.predict(x_cv_test)

        # 计算评价指标
        r2 = r2_score(y_cv_test, y_predcv)
        rmse = mean_squared_error(y_cv_test, y_predcv, squared=False)
        mae = mean_absolute_error(y_cv_test, y_predcv)
        mape = np.mean(np.abs((y_cv_test - y_predcv) / y_cv_test)) * 100

        # 将指标添加到列表
        r2_scores.append(r2)
        rmse_scores.append(rmse)
        mae_scores.append(mae)
        mape_scores.append(mape)

        # 存储真实值和预测值
        all_y_true.extend(y_cv_test)
        all_y_pred.extend(y_predcv)

    # 计算十折交叉验证的平均评价指标
    mean_r2 = np.mean(r2_scores)
    mean_rmse = np.mean(rmse_scores)
    mean_mae = np.mean(mae_scores)
    mean_mape = np.mean(mape_scores)

    # 打印结果
    print("十折交叉验证 R² 平均值:", mean_r2)
    print("十折交叉验证 RMSE 平均值:", mean_rmse)
    print("十折交叉验证 MAE 平均值:", mean_mae)
    print("十折交叉验证 MAPE 平均值:", mean_mape)

    # 绘制散点图并显示定量评价指标
    plt.figure(figsize=(6, 6), dpi=300)
    plt.scatter(all_y_true, all_y_pred, c='#66c2a5', edgecolor='k', alpha=0.7)
    # 1:1线 (灰色直线)
    plt.plot([min(all_y_true), max(all_y_true)], [min(all_y_true), max(all_y_true)], 'gray', alpha=0.5)

    # 拟合直线 (红色虚线)
    coefficients = np.polyfit(all_y_true, all_y_pred, 1)
    poly1d_fn = np.poly1d(coefficients)
    plt.plot(all_y_true, poly1d_fn(all_y_true), 'r--')

    plt.xlabel('True Values', fontsize=20)
    plt.ylabel('Predicted Values', fontsize=20)

    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    # 显示定量评价指标
    textstr = '\n'.join((
        f'R²: {mean_r2:.2f}',
        f'RMSE: {mean_rmse:.2f} $\mu g/m^3$',
        f'MAE: {mean_mae:.2f} $\mu g/m^3$',
        f'MAPE: {mean_mape:.2f}%'))

    plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=18,
             verticalalignment='top')

    plt.show()

    # 返回评价指标向量
    return np.array([mean_r2, mean_rmse, mean_mae, mean_mape])

# 示例调用
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators=200,min_samples_split = 2, random_state=42)
# 调用函数进行十折交叉验证并绘图
valmetric = cross_validate_and_plot(rf, x, y)


# -------------------------Bootstrapping 不确定性定量评估---------------------------------#

# 设置bootstrapping参数
B = 100  # 重采样次数
n = len(y)

# 存储每个bootstrap样本的预测结果
bootstrap_predictions0 = np.zeros((B, len(y)))
bootstrap_predictions1 = np.zeros((B, len(y)))

tempval = np.zeros((B, 4))
# 进行bootstrap重采样和模型训练
allshap= np.zeros((len(y), 8, B))
for i in range(B):
    # 有放回的重采样
    print('bootstrapping: ', i, ' of ', B)
    indices = np.random.choice(range(n), size=n, replace=True)
    X_sample = x[indices]
    y_sample = y[indices]
    
    # cross validation
    rf = RandomForestRegressor(n_estimators=200,min_samples_split = 2, random_state=42)
    tempval[i,:] = cross_validate_and_plot(rf, X_sample, y_sample)
    
    # 训练模型
    modelB=rf.fit(X_sample, y_sample)
    
    # -----------SHAP--------------
    import shap
    
    shap.initjs()
    # 使用整个训练集数据计算SHAP值
    explainer = shap.TreeExplainer(modelB)
    explanation = explainer(df_x)
    shap_values = explanation.values
    
    # explainer = shap.Explainer(rf)
    # shap_values = explainer(x)
    allshap[:,:,i] = shap_values


    # 对整个数据集进行预测
    bootstrap_predictions0[i] = modelB.predict(x)
    bootstrap_predictions1[i] = modelB.predict(df_newx)



#---------------------1. 特征重要性图-------------------------

from matplotlib.font_manager import FontProperties
font_prop = FontProperties(size=18, family='Arial' )

meanshap = np.mean(allshap,2)
# 对于 shap.plots.bar，我们需要设置全局的字体大小和字体类型
plt.rcParams['font.size'] = 18
plt.rcParams['font.family'] = 'Arial'

# 可视化特征重要性（全局）
plt.figure(dpi=300)
# plt.set_cmap("PiYG_r")
shap.summary_plot(meanshap, df_x, show = False)
# shap.summary_plot(shap_values, df_x, plot_type = 'violin', show = False)

fig = plt.gcf()
ax = fig.axes[0]

# 设置轴标题和轴标签的字体
ax.set_xlabel(ax.get_xlabel(), fontproperties=font_prop, color='black')
ax.set_ylabel(ax.get_ylabel(), fontproperties=font_prop, color='black')

# 设置轴刻度标签的字体和大小
for label in ax.get_xticklabels():
    label.set_fontproperties(font_prop)
    label.set_color('black')
for label in ax.get_yticklabels():
    label.set_fontproperties(font_prop)
    label.set_color('black')

# for cbar_ax in fig.axes[1:]:  # 假设颜色条在第二个轴对象中
#     cbar = fig.colorbar(ax.collections[0], cax=cbar_ax)
#     cbar.ax.set_title('Feature values', fontproperties=font_prop, color='black')

# 显示图形
plt.show()
plt.close()
#-------------------------1. 特征重要性图--------------------------


# 计算每个数据点的预测均值和标准误差
mean_predictions0 = np.mean(bootstrap_predictions0, axis=0)
std_predictions0 = np.std(bootstrap_predictions0, axis=0)

mean_predictions1 = np.mean(bootstrap_predictions1, axis=0)
std_predictions1 = np.std(bootstrap_predictions1, axis=0)
ste_predictions1 = std_predictions1/np.sqrt(len(bootstrap_predictions0))


# # 输出结果
# print("预测均值:", mean_predictions)
# print("预测标准误差:", std_predictions)

# 计算95%置信区间
lower_bounds = mean_predictions1 - 1.96 * ste_predictions1
upper_bounds = mean_predictions1 + 1.96 * ste_predictions1

rett000 = np.vstack((newpre, mean_predictions1,std_predictions1,ste_predictions1,lower_bounds,upper_bounds)).T

print("95%置信区间下限:", lower_bounds)
print("95%置信区间上限:", upper_bounds)



#------2. 特征依赖图------

# shap.plots.beeswarm(shap_values)
for i in range(8):
    shap.dependence_plot(i, shap_values, df_x, interaction_index='BGC', show = False)
    # shap.dependence_plot(i, shap_values, df_x, show = False)
    
    fig = plt.gcf()
    
    # 获取当前图形的第一个轴对象（通常只有一个）
    ax = fig.axes[0]
    font_prop = FontProperties(size=18, family='Arial' )
    
    # 设置轴标题和轴标签的字体
    ax.set_xlabel(ax.get_xlabel(), fontproperties=font_prop, color='black')
    ax.set_ylabel(ax.get_ylabel(), fontproperties=font_prop, color='black')
    
    # 设置轴刻度标签的字体和大小
    for label in ax.get_xticklabels():
        label.set_fontproperties(font_prop)
        label.set_color('black')
    for label in ax.get_yticklabels():
        label.set_fontproperties(font_prop)
        label.set_color('black')
        
    for ax in fig.axes:
        if isinstance(ax, plt.Axes):  # 检查是否为Axes对象
            cbar = ax.collections[0].colorbar
            if cbar:  # 如果存在颜色条
                cbar.ax.title.set_fontproperties(font_prop)
                for label in cbar.ax.get_yticklabels():
                    label.set_fontproperties(font_prop)
                
            
    plt.show()
# plt.close()




# ------------------------------------差值计算以及统计指标获取，不确定度量化------------------------------------

ddold = newpre-y
dd = mean_predictions1-y

dd_lower = lower_bounds-y
dd_upper = upper_bounds-y

meandd = np.mean(dd)
stddd = np.std(dd, ddof=1)
stedd = stddd/np.sqrt(len(dd))

sigrange1 = [meandd-1.96*stedd,meandd+1.96*stedd]
rett = [meandd,meandd-1.96*stedd,meandd+1.96*stedd]

pdd = dd/newpre

# # 计算95%置信区间--------结果同上
# import scipy.stats as stats
# confidence_level = 0.95
# degrees_freedom = len(dd) - 1
# confidence_interval = stats.t.interval(confidence_level, degrees_freedom, meandd, stedd)

# 分年份进行统计
dd2 = dd.reshape(150,7,order = 'F')
column_means = np.mean(dd2, axis=0)
column_stds = np.std(dd2, axis=0)
column_varis = column_stds**2
column_stes = column_stds/np.sqrt(len(dd))
# 计算 95% 置信区间的范围
ci_lower = column_means - 1.96 * column_stes 
ci_upper = column_means + 1.96 * column_stes


# 计算不同城市的均值，同时考虑模型导致的每个城市的数据的误差，以及用均值代表不同城市的个体差异导致的误差，用两部分误差共同计算最后的置信区间
vari = std_predictions1**2
vari2 = vari.reshape(150,7,order = 'F')
vari_mean = np.mean(vari2, axis=0)


totalvari = column_varis+vari_mean
totalste = np.sqrt(totalvari/150)
total_lower = column_means - 1.96 * totalste 
total_upper = column_means + 1.96 * totalste

# rett0 = np.vstack((column_means,column_stds,column_stes,ci_lower,ci_upper))
rett00 = np.vstack((column_means,np.sqrt(totalvari),totalste,total_lower,total_upper))



dd2_lower = dd_lower.reshape(150,7,order = 'F')
column_means_low = np.mean(dd2_lower, axis=0)
column_stds_low = np.std(dd2_lower, axis=0)
column_stes_low = column_stds_low/np.sqrt(dd2.shape[0])
# 计算 95% 置信区间的范围
ci_lower_low = column_means_low - 1.96 * column_stes_low 
ci_upper_low = column_means_low + 1.96 * column_stes_low
rett01 = np.vstack((column_means_low,column_stds_low,column_stes_low,ci_lower_low,ci_upper_low))

dd2_upper = dd_upper.reshape(150,7,order = 'F')
column_means_up = np.mean(dd2_upper, axis=0)
column_stds_up = np.std(dd2_upper, axis=0)
column_stes_up = column_stds_up/np.sqrt(dd2.shape[0])
# 计算 95% 置信区间的范围
ci_lower_up = column_means_up - 1.96 * column_stes_up
ci_upper_up = column_means_up + 1.96 * column_stes_up
rett02 = np.vstack((column_means_up,column_stds_up,column_stes_up,ci_lower_up,ci_upper_up))


# # -------------------------------将结果写入到xlsx文件中---------------------------------

# outname = r'D:\3MTDNN_v2.0\Yearly_scale_experiments\Yearly_retrievals_analysis\vehicle_data_analysis\simulation_experiments_results_Bootstrap_withBGC.xlsx'
# sheetname = 'NO2'

# outdf_dd2 = pd.DataFrame(dd2)
# outdf_rett00 = pd.DataFrame(rett00)

# outdf_dd2_lower = pd.DataFrame(dd2_lower)
# outdf_rett01 = pd.DataFrame(rett01)

# outdf_dd2_upper = pd.DataFrame(dd2_upper)
# outdf_rett02 = pd.DataFrame(rett02)

# outdf_rett000 = pd.DataFrame(rett000)

# # 使用 openpyxl 引擎加载 Excel 文件
# with pd.ExcelWriter(outname, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
#     # 将 DataFrame 写入到指定的sheet的指定位置
#     outdf_rett000.to_excel(writer, sheet_name=sheetname, startrow=2, startcol=3, header=False, index=False)
    
#     outdf_dd2.to_excel(writer, sheet_name=sheetname, startrow=2, startcol=14, header=False, index=False)
#     outdf_rett00.to_excel(writer, sheet_name=sheetname, startrow=152, startcol=14, header=False, index=False)
    
#     outdf_dd2_lower.to_excel(writer, sheet_name=sheetname, startrow=2, startcol=23, header=False, index=False)
#     outdf_rett01.to_excel(writer, sheet_name=sheetname, startrow=152, startcol=23, header=False, index=False)
    
#     outdf_dd2_upper.to_excel(writer, sheet_name=sheetname, startrow=2, startcol=32, header=False, index=False)
#     outdf_rett02.to_excel(writer, sheet_name=sheetname, startrow=152, startcol=32, header=False, index=False)
    




# ------------------------------------ 热力图------------------------------------

# 绘制热力图

cities = df['city']
years = df['year']

dd= -1*dd

# 构建新的 DataFrame，并设置索引
df_dd = pd.DataFrame({ 'year': years, 'city': cities, 'difference': dd})
df_dd_pivot = df_dd.pivot(index='year', columns='city', values='difference')


# 绘制热力图
fig, ax = plt.subplots(figsize=(15, 5), dpi=300)

vmax=max(abs(dd))
vmin=-1*vmax

# vmax=18
# vmin=-18

cax = ax.matshow(df_dd_pivot, cmap='PiYG_r', aspect='auto', vmin = vmin, vmax = vmax)

# 添加颜色条
cbar = fig.colorbar(cax, pad=0.01,  ax=ax, extend = 'both')
cbar.set_label('difference', fontname='Arial', fontsize=24)
cbar.ax.tick_params(labelsize=24)

# 设置 x 和 y 轴刻度及标签
ax.set_xticks(np.arange(len(df_dd_pivot.columns)))
ax.set_yticks(np.arange(len(df_dd_pivot.index)))

ax.set_xticklabels(df_dd_pivot.columns, fontname='Arial', fontsize=24, rotation=90)
ax.set_yticklabels(df_dd_pivot.index, fontname='Arial', fontsize=24)

# 调整x轴标签的间隔，使其更加美观
ax.xaxis.set_major_locator(plt.MaxNLocator(15))  # 每15个城市显示一个标签

# 设置轴标签和标题
plt.xlabel('City', fontname='Arial', fontsize=24)
plt.ylabel('Year', fontname='Arial', fontsize=24)
# plt.title('Heatmap of difference', fontname='Arial', fontsize=20)

# 显示图像
plt.tight_layout()
plt.show()


# --------------------------------- 直方图--------------------------------
plt.figure(figsize=(7, 5), dpi=300)
plt.hist(dd, bins=30, color='#97cc5e', edgecolor='black')

plt.xlabel('Difference', fontname='Arial', fontsize=24)
plt.ylabel('Frequency', fontname='Arial', fontsize=24)
plt.title('Histogram of Prediction Errors', fontname='Arial', fontsize=24)

plt.xticks(fontname='Arial', fontsize=24)
plt.yticks(fontname='Arial', fontsize=24)

plt.grid(False)
plt.tight_layout()
plt.show()
# newx = x_norm
# newx[:,1]=x[:,1]+x[:,2]
# newx[:,2]=x[:,2]-x[:,2]
# newpre = result.predict(newx)





