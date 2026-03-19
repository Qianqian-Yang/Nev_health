# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt

colors = np.array([(178/255,222/255,142/255),(237/255,151/255,200/255)])

fig, axs = plt.subplots(5,1,figsize=(10, 30),dpi=300)

countf = -1
for pollut in [0,1,2,4]:
    countf = countf+1
    
    if pollut == 0:
        pollstr = 'PM25'
    if pollut == 1:
        pollstr = 'NO2'        
    if pollut == 2:
        pollstr = 'CO'
    if pollut == 3:
        pollstr = 'O3'        
    if pollut == 4:
        pollstr = 'PM10'     
        
    filename1 = 'mean_values_for_different_landtypes_'+pollstr+'.xlsx'
    excel_file1 = pd.ExcelFile(filename1)

    filename2 = 'mean_values_for_different_landtypes_'+pollstr+'_2.xlsx'
    excel_file2 = pd.ExcelFile(filename2)
    
    sheet_names1 = excel_file1.sheet_names
              
    df11 = pd.read_excel(excel_file1, sheet_name='forest')
    data11 = df11.to_numpy()
    data11 = data11[:100,1:]
    
    df12 = pd.read_excel(excel_file2, sheet_name='forest')
    data12 = df12.to_numpy()
    data12 = data12[100:,1:]
    
    data1 = np.vstack((data11,data12))
    mean1 = np.nanmean(data1,0)
    
    df21 = pd.read_excel(excel_file1, sheet_name='road')
    data21 = df21.to_numpy()
    data21 = data21[:100,1:]
    
    df22 = pd.read_excel(excel_file2, sheet_name='road')
    data22 = df22.to_numpy()
    data22 = data22[100:,1:]    
    
    data2 = np.vstack((data21,data22))
    mean2 = np.nanmean(data2,0)


    for yy in range(2013,2024):
        
          d1 = data1[:, yy - 2013]
          d2 = data2[:, yy - 2013]
        
          # 去除 NaN（关键）
          d1 = d1[~np.isnan(d1)]
          d2 = d2[~np.isnan(d2)]
 
          axs[countf].boxplot(d1, positions=[yy-0.2], widths=0.3, notch=True, patch_artist=True, showfliers=False,showmeans=True, 
                      medianprops={'lw': 1, 'color': 'k'},
                      boxprops={'facecolor': colors[0], 'lw':1},
                      # capprops={'lw': 1, 'color': colors[1]},
                      # whiskerprops={'ls': '-', 'lw': 1, 'color': ;k},
                      meanprops=dict(marker='o', markerfacecolor='k', markeredgecolor='k',markersize=3))
         
          axs[countf].boxplot(d2, positions=[yy+0.2], widths=0.3, notch=True, patch_artist=True, showfliers=False,showmeans=True, 
                      medianprops={'lw': 1, 'color': 'k'},
                      boxprops={'facecolor': colors[1], 'lw':1},
                      # capprops={'lw': 1, 'color': colors[1]},
                      # whiskerprops={'ls': '-', 'lw': 1, 'color': ;k},
                      meanprops=dict(marker='o', markerfacecolor='k', markeredgecolor='k',markersize=3))

    slope1, intercept1, _, _, _ = linregress(range(2013, 2024), mean1)

    axs[countf].plot(range(2013, 2024), slope1 * np.array(range(2013, 2024)) + intercept1, color=colors[0], linestyle='--', linewidth = 2, label=f'y={slope1:.3f}x+{intercept1:.2f}')
    

    slope2, intercept2, _, _, _ = linregress(range(2013, 2024), mean2)

    axs[countf].plot(range(2013, 2024), slope2 * np.array(range(2013, 2024)) + intercept2, color=colors[1], linestyle='--', linewidth = 2, label=f'y={slope2:.3f}x+{intercept2:.2f}')
    
    axs[countf].set_xlabel('Year',fontsize=20)#设置x轴刻度标签
    if pollut==0:
        axs[countf].set_ylabel('$PM_{2.5}$($\mu$g/${m^3}$)', fontsize=20)
    if pollut==1:
        axs[countf].set_ylabel('$NO_{2}$($\mu$g/${m^3}$)', fontsize=20)    
    if pollut==2:
        axs[countf].set_ylabel('CO(mg/${m^3}$)', fontsize=20) 
    if pollut==3:
        axs[countf].set_ylabel('$O_{3}$($\mu$g/${m^3}$)', fontsize=20)             
    if pollut==4:
        axs[countf].set_ylabel('$PM_{10}$($\mu$g/${m^3}$)', fontsize=20) 
    
    axs[countf].set_xticks(range(2013, 2024, 2),[str(y) for y in range(2013, 2024, 2)],fontsize=20)
    axs[countf].legend(loc='upper right', bbox_to_anchor=(1, 0.99), edgecolor='w', fontsize=20)
    
fig.delaxes(axs[-1])

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 20

plt.show()
     
       
        
       