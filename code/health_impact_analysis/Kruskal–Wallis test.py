# -*- coding: utf-8 -*-

from scipy import stats
import itertools
import numpy as np
import pandas as pd

# READ annual variation rate file
colors = np.array([(178/255,222/255,142/255),(237/255,151/255,200/255)])
color1 = (192/255,219/255,95/255)

# filename = 'Health_impact_results_withBGC.xlsx'
filename = 'Health_impact_results_withBGC_2023.xlsx'
filepath = 'D:\\3MTDNN_v2.0\\Yearly_scale_experiments\\health_impact_analysis\\'+filename

excel_file = pd.ExcelFile(filepath)

cityshppath ='D:\\3MTDNN_v2.0\\Yearly_scale_experiments\\cityinformation\\merged_output_150cities.shp'

pollutants = ['NO2', 'PM25', 'CO', 'PM10']

filename2 = 'BootstrapRF_simulated_NEV_contribution_to_air_pollution_change_withBGC.xlsx'
filepath2 = 'D:\\3MTDNN_v2.0\\Yearly_scale_experiments\\Yearly_retrievals_analysis\\vehicle_data_analysis\\'+filename2

excel_file2 = pd.ExcelFile(filepath2)


result_df = pd.DataFrame(columns=[
    'Group1', 'Group2', 'Statistic', 'P-value', 
    'Adjusted P-value', 'Significant'
])

for j, metric in enumerate(pollutants):

    
    if j==1:
        # for PM2.5
        metricstr = metricstr = '$PM_{2.5}$'
        df1 = pd.read_excel(excel_file, sheet_name = 'GEMM-age')
        data1 = df1.to_numpy()
        city_mb = data1[:150,13]

    if j==0:
        # for NO2
        metricstr = '$NO_2$'
        df1 = pd.read_excel(excel_file, sheet_name = 'NO2_TMREL=0')
        data1 = df1.to_numpy()
        city_mb = data1[:150,3]
 
    if j==2:
        # for CO
        metricstr = 'CO'
        df1 = pd.read_excel(excel_file, sheet_name = 'CO_TMREL=0')
        data1 = df1.to_numpy()
        city_mb = data1[:150,3]

    if j==3:
        # for PM10  
        metricstr = '$PM_{2.5-10}$'
        df1 = pd.read_excel(excel_file, sheet_name = 'PM2.5-10_TMREL=0')
        data1 = df1.to_numpy()
        city_mb = data1[:150,3]
    
        
    df2 = pd.read_excel(excel_file2, sheet_name = metric)
    data2 = df2.to_numpy()
    
    cities = data2[:150,0]
    gdp = data2[:150,13]
    
    quantiles = np.nanquantile(gdp, [0.2, 0.4, 0.6, 0.8])
    bins = [-np.inf] + quantiles.tolist() + [np.inf]
    labels = ['G1', 'G2', 'G3', 'G4', 'G5']
    groups = pd.cut(gdp, bins=bins, labels=labels, include_lowest=True)
    grouped_data = {label: city_mb[groups == label] for label in labels}
    
    # Kruskal-Wallis test
    kw_stat, kw_p = stats.kruskal(*[grouped_data[label] for label in labels])
    
    result_df = pd.concat([
        pd.DataFrame([{
            'Group1': 'ALL',
            'Group2': 'ALL',
            'Statistic': kw_stat,
            'P-value': kw_p,
            'Adjusted P-value': kw_p,
            'Significant': kw_p < 0.05
        }]),
        result_df
    ], ignore_index=True)
    

    result_df['P-value'] = result_df['P-value'].apply(
        lambda x: f"{x:.4f}" if isinstance(x, float) else x)
    result_df['Adjusted P-value'] = result_df['Adjusted P-value'].apply(
        lambda x: f"{x:.4f}" if isinstance(x, float) else x)
    
    print("\n result：")
        
        
        
        