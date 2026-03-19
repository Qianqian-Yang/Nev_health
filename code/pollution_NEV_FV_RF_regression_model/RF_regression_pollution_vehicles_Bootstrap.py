"""
Example code for machine learning analysis used in the study.

This script demonstrates:
1. Random Forest model training
2. Cross-validation performance evaluation
3. Bootstrapping-based uncertainty quantification
4. SHAP feature importance analysis
5. Visualization of prediction differences

Author: Qianqian Yang
Repository: https://github.com/Qianqian-Yang/Nev_health
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

file1 = r'D:\3MTDNN_v2.0\Yearly_scale_experiments\Yearly_retrievals_analysis\vehicle_data_analysis\Matchpair_example.xlsx'

excel_file1 = pd.ExcelFile(file1)
df0 = pd.read_excel(excel_file1)

df = df0.dropna(axis=0,how='any')

data1 = df.to_numpy()

citypm25 = df['PM25_city'].to_numpy()
cityno2 = df['NO2_city'].to_numpy()
cityco = df['CO_city'].to_numpy()
citypm10 = df['PM10_city'].to_numpy()

forestpm25 = df['PM25_forest'].to_numpy()
forestno2 = df['NO2_forest'].to_numpy()
forestco = df['CO_forest'].to_numpy()
forestpm10 = df['PM10_forest'].to_numpy()

citynum = df['city'].to_numpy()

nevehicle = df['NEvehicle'].to_numpy()
vehicle = df['vehicle'].to_numpy()
tvehicle = df['fuelvehicle'].to_numpy() 
nevratio = nevehicle/vehicle

roadpm25 = df['PM25_road'].to_numpy()
roadno2 = df['NO2_road'].to_numpy()
roadco = df['CO_road'].to_numpy()
roadpm10 = df['PM10_road'].to_numpy()

x = np.hstack((forestno2.reshape(-1,1), tvehicle.reshape(-1,1), nevehicle.reshape(-1,1), data1[:,14:19]))

nan_rows = np.any(np.isnan(x), axis=1)

# Remove rows containing NaN values
x = x[~nan_rows]

x1 = np.hstack((forestno2.reshape(-1,1), tvehicle.reshape(-1,1), nevehicle.reshape(-1,1), data1[:,14:19]))

scaler = MinMaxScaler()
x_norm = scaler.fit_transform(x)

# change the target variable here
y = roadpm25
y = y[~nan_rows]

feature_names = ['BGC','FV', 'NEV', 'T2M', 'D2M', 'SP', 'U10', 'V10']

df_x = pd.DataFrame(x, columns=feature_names)
df_y = pd.DataFrame(y.reshape(-1,1), columns=['roadpm25'])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

rf = RandomForestRegressor(n_estimators=100, random_state=42)

rf.fit(df_x, df_y)

feature_importances = rf.feature_importances_

# -------- simulation scenario -------------
newx = x1
newx[:,1]=x1[:,1]+x1[:,2]
newx[:,2]=x1[:,2]-x1[:,2]

df_newx = pd.DataFrame(newx, columns=feature_names)

newpre = rf.predict(df_newx)

# -------------------------10-fold CV---------------------------------#
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split, KFold

def cross_validate_and_plot(model, x, y, n_splits=10, random_state=42):

    kf = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    r2_scores = []
    rmse_scores = []
    mae_scores = []
    mape_scores = []

    all_y_true = []
    all_y_pred = []

    for train_index, test_index in kf.split(x):
        x_cv_train, x_cv_test = x[train_index], x[test_index]
        y_cv_train, y_cv_test = y[train_index], y[test_index]

        model.fit(x_cv_train, y_cv_train)
        y_predcv = model.predict(x_cv_test)

        r2 = r2_score(y_cv_test, y_predcv)
        rmse = mean_squared_error(y_cv_test, y_predcv, squared=False)
        mae = mean_absolute_error(y_cv_test, y_predcv)
        mape = np.mean(np.abs((y_cv_test - y_predcv) / y_cv_test)) * 100

        r2_scores.append(r2)
        rmse_scores.append(rmse)
        mae_scores.append(mae)
        mape_scores.append(mape)

        all_y_true.extend(y_cv_test)
        all_y_pred.extend(y_predcv)

    mean_r2 = np.mean(r2_scores)
    mean_rmse = np.mean(rmse_scores)
    mean_mae = np.mean(mae_scores)
    mean_mape = np.mean(mape_scores)

    # Print cross-validation metrics
    print("CV R² mean:", mean_r2)
    print("CV RMSE mean:", mean_rmse)
    print("CV MAE mean:", mean_mae)
    print("CV MAPE mean:", mean_mape)

    # Scatter plot of observed vs predicted values
    plt.figure(figsize=(6, 6), dpi=300)
    plt.scatter(all_y_true, all_y_pred, c='#66c2a5', edgecolor='k', alpha=0.7)

    # 1:1 reference line
    plt.plot([min(all_y_true), max(all_y_true)], [min(all_y_true), max(all_y_true)], 'gray', alpha=0.5)

    # Linear regression fit line
    coefficients = np.polyfit(all_y_true, all_y_pred, 1)
    poly1d_fn = np.poly1d(coefficients)
    plt.plot(all_y_true, poly1d_fn(all_y_true), 'r--')

    plt.xlabel('True Values', fontsize=20)
    plt.ylabel('Predicted Values', fontsize=20)

    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    textstr = '\n'.join((
        f'R²: {mean_r2:.2f}',
        f'RMSE: {mean_rmse:.2f} $\mu g/m^3$',
        f'MAE: {mean_mae:.2f} $\mu g/m^3$',
        f'MAPE: {mean_mape:.2f}%'))

    plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=18,
             verticalalignment='top')

    plt.show()

    return np.array([mean_r2, mean_rmse, mean_mae, mean_mape])

from sklearn.ensemble import RandomForestRegressor

valmetric = cross_validate_and_plot(rf, x, y)

# -------------------------Bootstrapping-based uncertainty quantification---------------------------------#

B = 100 
n = len(y)

bootstrap_predictions0 = np.zeros((B, len(y)))
bootstrap_predictions1 = np.zeros((B, len(y)))

tempval = np.zeros((B, 4))

allshap= np.zeros((len(y), 8, B))
for i in range(B):

    print('bootstrapping: ', i, ' of ', B)
    indices = np.random.choice(range(n), size=n, replace=True)
    X_sample = x[indices]
    y_sample = y[indices]

    # cross validation
    tempval[i,:] = cross_validate_and_plot(rf, X_sample, y_sample)

    modelB=rf.fit(X_sample, y_sample)

    # -----------SHAP analysis--------------
    import shap

    shap.initjs()
    explainer = shap.TreeExplainer(modelB)
    explanation = explainer(df_x)
    shap_values = explanation.values

    allshap[:,:,i] = shap_values

    bootstrap_predictions0[i] = modelB.predict(x)
    bootstrap_predictions1[i] = modelB.predict(df_newx)

# --------------------- Feature importance analysis using SHAP ---------------------

from matplotlib.font_manager import FontProperties
font_prop = FontProperties(size=18, family='Arial' )

meanshap = np.mean(allshap,2)

plt.rcParams['font.size'] = 18
plt.rcParams['font.family'] = 'Arial'

plt.figure(dpi=300)
shap.summary_plot(meanshap, df_x, show = False)

fig = plt.gcf()
ax = fig.axes[0]

ax.set_xlabel(ax.get_xlabel(), fontproperties=font_prop, color='black')
ax.set_ylabel(ax.get_ylabel(), fontproperties=font_prop, color='black')

for label in ax.get_xticklabels():
    label.set_fontproperties(font_prop)
    label.set_color('black')
for label in ax.get_yticklabels():
    label.set_fontproperties(font_prop)
    label.set_color('black')

plt.show()
plt.close()

# Calculate mean prediction and uncertainty statistics

mean_predictions0 = np.mean(bootstrap_predictions0, axis=0)
std_predictions0 = np.std(bootstrap_predictions0, axis=0)

mean_predictions1 = np.mean(bootstrap_predictions1, axis=0)
std_predictions1 = np.std(bootstrap_predictions1, axis=0)
ste_predictions1 = std_predictions1/np.sqrt(len(bootstrap_predictions0))

# Compute the 95% confidence interval

lower_bounds = mean_predictions1 - 1.96 * ste_predictions1
upper_bounds = mean_predictions1 + 1.96 * ste_predictions1

rett000 = np.vstack((newpre, mean_predictions1,std_predictions1,ste_predictions1,lower_bounds,upper_bounds)).T

print("95% confidence interval lower bound:", lower_bounds)
print("95% confidence interval upper bound:", upper_bounds)

# ------------------------------------Difference calculation and uncertainty quantification------------------------------------

ddold = newpre-y
dd = mean_predictions1-y

dd_lower = lower_bounds-y
dd_upper = upper_bounds-y

pdd = dd/newpre

meandd = np.mean(dd)
stddd = np.std(dd, ddof=1)
stedd = stddd/np.sqrt(len(dd))

sigrange1 = [meandd-1.96*stedd,meandd+1.96*stedd]
rett = [meandd,meandd-1.96*stedd,meandd+1.96*stedd]

# Compute statistics for each year

dd2 = dd.reshape(150,7,order = 'F')
column_means = np.mean(dd2, axis=0)
column_stds = np.std(dd2, axis=0)
column_varis = column_stds**2
column_stes = column_stds/np.sqrt(len(dd))

ci_lower = column_means - 1.96 * column_stes 
ci_upper = column_means + 1.96 * column_stes

# Combine model uncertainty and inter-city variability

vari = std_predictions1**2
vari2 = vari.reshape(150,7,order = 'F')
vari_mean = np.mean(vari2, axis=0)

totalvari = column_varis+vari_mean
totalste = np.sqrt(totalvari/150)
total_lower = column_means - 1.96 * totalste 
total_upper = column_means + 1.96 * totalste

rett00 = np.vstack((column_means,np.sqrt(totalvari),totalste,total_lower,total_upper))

# -------------------------------Write results to Excel file---------------------------------

outname = r'D:\3MTDNN_v2.0\Yearly_scale_experiments\Yearly_retrievals_analysis\vehicle_data_analysis\simulation_experiments_results_Bootstrap_withBGC.xlsx'
sheetname = 'PM25'

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

outdf_dd2 = pd.DataFrame(dd2)
outdf_rett00 = pd.DataFrame(rett00)

outdf_dd2_lower = pd.DataFrame(dd2_lower)
outdf_rett01 = pd.DataFrame(rett01)

outdf_dd2_upper = pd.DataFrame(dd2_upper)
outdf_rett02 = pd.DataFrame(rett02)

outdf_rett000 = pd.DataFrame(rett000)

with pd.ExcelWriter(outname, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:

    outdf_rett000.to_excel(writer, sheet_name=sheetname, startrow=2, startcol=3, header=False, index=False)

    outdf_dd2.to_excel(writer, sheet_name=sheetname, startrow=2, startcol=14, header=False, index=False)
    outdf_rett00.to_excel(writer, sheet_name=sheetname, startrow=152, startcol=14, header=False, index=False)

# ------------------------------------ Heatmap visualization ------------------------------------

cities = df['city']
years = df['year']

dd= -1*dd

df_dd = pd.DataFrame({ 'year': years, 'city': cities, 'difference': dd})
df_dd_pivot = df_dd.pivot(index='year', columns='city', values='difference')

fig, ax = plt.subplots(figsize=(15, 5), dpi=300)

vmax=max(abs(dd))
vmin=-1*vmax

cax = ax.matshow(df_dd_pivot, cmap='PiYG_r', aspect='auto', vmin = vmin, vmax = vmax)

# Add colorbar
cbar = fig.colorbar(cax, pad=0.01,  ax=ax, extend = 'both')
cbar.set_label('difference', fontname='Arial', fontsize=24)
cbar.ax.tick_params(labelsize=24)

# Set axis ticks and labels
ax.set_xticks(np.arange(len(df_dd_pivot.columns)))
ax.set_yticks(np.arange(len(df_dd_pivot.index)))

ax.set_xticklabels(df_dd_pivot.columns, fontname='Arial', fontsize=24, rotation=90)
ax.set_yticklabels(df_dd_pivot.index, fontname='Arial', fontsize=24)

# Adjust x-axis label spacing
ax.xaxis.set_major_locator(plt.MaxNLocator(15))

plt.xlabel('City', fontname='Arial', fontsize=24)
plt.ylabel('Year', fontname='Arial', fontsize=24)

plt.tight_layout()
plt.show()

# --------------------------------- Histogram --------------------------------

plt.figure(figsize=(7, 5), dpi=300)
plt.hist(dd, bins=30, color='#97cc5e', edgecolor='black')

plt.xlabel('Difference', fontname='Arial', fontsize=20)
plt.ylabel('Frequency', fontname='Arial', fontsize=20)
plt.title('Histogram of Prediction Errors', fontname='Arial', fontsize=24)

plt.xticks(fontname='Arial', fontsize=24)
plt.yticks(fontname='Arial', fontsize=24)

plt.grid(False)
plt.tight_layout()


plt.show()