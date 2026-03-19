# -*- coding: utf-8 -*-

"""
Boxplot visualization of bootstrap model performance metrics.

This script reads bootstrap model accuracy results from an Excel file and
visualizes the distributions of four evaluation metrics (R2, RMSE, MAPE, MAE)
for different pollutants using boxplots. The figure is formatted following
a Nature-style visualization scheme with customized colors and fonts.

Metrics are displayed in four subplots and include dual-axis visualization
for CO in RMSE and MAE due to different units.

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read Excel file
file_path = 'Bootstrap_models_accuracy_withBGC.xlsx' 
data = pd.read_excel(file_path, header=[0, 1])

# List of pollutants
pollutants = ['NO2', 'PM25', 'CO', 'PM10']

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(11, 8), dpi=300, sharex=True)

# metrics = ['R2', 'RMSE', 'MAE', 'MAPE']

metrics = ['R2', 'RMSE', 'MAPE', 'MAE']

# Color scheme
colors = ['#91BFFA', '#FFE0C1', '#8CC5BE', '#FF7F00']


for i, metric in enumerate(metrics):

   
    # Set metric label and add superscript formatting for R2
    if metric == 'R2':
        metric_label = r'$R^2$'
        co_metric_label = r'$R^2$ for  CO'
    elif metric == 'MAPE':
        metric_label = metric+'(%)'
        co_metric_label = f'{metric} for CO'
    else:
        metric_label = metric + '($\mu g/m^3$)'
        co_metric_label = f'{metric} for CO ($mg/m^3$)'
        
        
    ax = axes[i // 2, i % 2]
    

    # Organize data as a list for each pollutant
    data_list = data[metrics[i]]

    # Draw boxplots for the left y-axis
    bplot1 = ax.boxplot(data_list.iloc[:, 0], positions=[1], widths=0.8, patch_artist=True,
                        boxprops=dict(facecolor=colors[0], linewidth=2), 
                        medianprops=dict(color='black', linewidth=2),
                        whiskerprops=dict(color='black', linewidth=2), 
                        capprops=dict(color='black', linewidth=2),
                        showmeans=True, meanprops=dict(marker='o', markerfacecolor='white', markeredgecolor='black', markersize=10))
    
    bplot2 = ax.boxplot(data_list.iloc[:,1], positions=[2], widths=0.8, patch_artist=True,
                        boxprops=dict(facecolor=colors[1], linewidth=2), 
                        medianprops=dict(color='black', linewidth=2),
                        whiskerprops=dict(color='black', linewidth=2), 
                        capprops=dict(color='black', linewidth=2),
                        showmeans=True, meanprops=dict(marker='o', markerfacecolor='white', markeredgecolor='black', markersize=10))    
 
    bplot4 = ax.boxplot(data_list.iloc[:, 3], positions=[3], widths=0.8, patch_artist=True,
                        boxprops=dict(facecolor=colors[3], linewidth=2), 
                        medianprops=dict(color='black', linewidth=2),
                        whiskerprops=dict(color='black', linewidth=2), 
                        capprops=dict(color='black', linewidth=2),
                        showmeans=True, meanprops=dict(marker='o', markerfacecolor='white', markeredgecolor='black', markersize=10))  

    

    # Draw boxplot for the right y-axis
    if metric == 'R2' or (metric == 'MAPE'):
        print(metric)
        bplot3 = ax.boxplot([data_list.iloc[:, 2]], positions=[4], widths=0.8, patch_artist=True,
                                  boxprops=dict(facecolor=colors[2], linewidth=2), 
                                  medianprops=dict(color='black', linewidth=2),
                                  whiskerprops=dict(color='black', linewidth=2), 
                                  capprops=dict(color='black', linewidth=2),
                                  showmeans=True, meanprops=dict(marker='o', markerfacecolor='white', markeredgecolor='black', markersize=10))
        
        ax.set_ylabel(metric_label, fontsize=20, fontname='Arial')
        
        # Set axis font properties
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname('Arial')
            label.set_fontsize(20)
            
        
    if metric == 'RMSE'or (metric == 'MAE'):
        print(metric)
        ax_right = ax.twinx()
        
        bplot3 = ax_right.boxplot([data_list.iloc[:, 2]], positions=[4], widths=0.8, patch_artist=True,
                                  boxprops=dict(facecolor=colors[2], linewidth=2), 
                                  medianprops=dict(color='black', linewidth=2),
                                  whiskerprops=dict(color='black', linewidth=2), 
                                  capprops=dict(color='black', linewidth=2),
                                  showmeans=True, meanprops=dict(marker='o', markerfacecolor='white', markeredgecolor='black', markersize=10))
   
        # Set right y-axis color to match the CO box color
        ax_right.spines['right'].set_color(colors[2])
        ax_right.spines['right'].set_linewidth(2)
        ax_right.yaxis.label.set_color(colors[2])
        ax_right.tick_params(axis='y', colors=colors[2])
        
        ax.set_ylabel(metric_label, fontsize=20, fontname='Arial')
        ax_right.set_ylabel(co_metric_label, fontsize=20, fontname='Arial')
       
        # Set axis font properties
        for label in (ax.get_xticklabels() + ax.get_yticklabels() + ax_right.get_yticklabels()):
            label.set_fontname('Arial')
            label.set_fontsize(20)


    # Set x-axis ticks and labels
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(['$NO_2$', '$PM_{2.5}$', '$PM_{10}$', 'CO'], fontsize=20, fontname='Arial')
    
    
    # Set axis spine line widths
    ax.spines['top'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    # ax_right.spines['top'].set_linewidth(2)
    # ax_right.spines['bottom'].set_linewidth(2)   
 
plt.tight_layout()
plt.show()