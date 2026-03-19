# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 15:59:19 2024

@author: Qianqian Yang
"""


import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import matplotlib.colorbar as cbar

import os

from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon

import pandas as pd

# READ annual variation rate file
colors = np.array([(178/255,222/255,142/255),(237/255,151/255,200/255)])
color1 = (132/255,188/255,217/255)

filename = 'BootstrapRF_simulated_NEV_contribution_to_air_pollution_change_withBGC.xlsx'
filepath = 'D:\\3MTDNN_v2.0\\Yearly_scale_experiments\\Yearly_retrievals_analysis\\vehicle_data_analysis\\'+filename

excel_file = pd.ExcelFile(filepath)

pollutants = ['NO2', 'PM25', 'CO', 'PM10']


# data 1 12列，分别表示 0-all, 1-road, 2-motor, 3-trunk, 4-primary, 5-second,6-third, 7-crop, 8-forest, 9-grass, 10-barren, 11-impervious

cityshppath ='D:\\3MTDNN_v2.0\\Yearly_scale_experiments\\cityinformation\\merged_output_150cities.shp'

for j, metric in enumerate(pollutants):
    
    df1 = pd.read_excel(excel_file, sheet_name = metric)
    data1 = df1.to_numpy()
    new_data = data1[~np. isnan (data1)]
    
    for i in range(11,12):    # i=7 data for 2023     i=11 percent of change in 2023
        
        # # draw frequency map
        # fig0 = plt.figure(figsize=(7,5),dpi=300)
        # plt.hist(data1[:,i],50,facecolor = colors[1],edgecolor = 'k')
        # plt.xlabel("NEV contribution in 2023",fontsize=28)
        # plt.ylabel("Frequency",fontsize=28)
        
        # # 设置字体和字号
        # plt.rcParams['font.family'] = 'Arial'
        # plt.rcParams['font.size'] = 28
        
        
        # draw distribution map
        fig = plt.figure(figsize=(8,6),dpi=300)
        # fig = plt.figure(figsize=(12,6),dpi=300)
        ax = fig.add_subplot(111)  # 添加子图，这里 111 表示就一张图，返回该子图的坐标系对象  
        
        lons = 73
        lone = 136
        lats = 17
        late = 55
        
        m = Basemap(llcrnrlat = lats, urcrnrlat = late, llcrnrlon = lons, urcrnrlon = lone)
        
        shpfile = r'D:\China_map\utf-8\Export_Output_2'
        m.readshapefile(shpfile, 'states', drawbounds=True, linewidth=0.4)
        
        m.readshapefile(cityshppath[:-4], 'cities',  linewidth=0.2)
        cityinfo = m.cities_info #读取省份信息 
        
        colors = {}
        # cmap = plt.cm.RdBu_r       #指定色彩映射种类 GDP_max = max(df['2016年'])
        cmap = plt.cm.PiYG_r
        slope_min = min(data1[:,i].flatten())
        slope_max = max(data1[:,i].flatten())
        
       
        slope_min = -0.5
        slope_max = 0.5     
        
            
        if j==0:
            # slope_min = -5
            # slope_max = 5  
            metricstr = '$NO_2$'
            acode = "B"
        if j==1:
            # slope_min = -20
            # slope_max = 20   
            metricstr = metricstr = '$PM_{2.5}$'
            acode = "A"
        if j==2:
            # slope_min = -0.65
            # slope_max = 0.65  
            metricstr = 'CO'
            slope_min = -0.5
            slope_max = 0.5     
            acode = "C"
        if j==3:
            # slope_min = -25
            # slope_max = 25  
            metricstr = '$PM_{10}$'
            acode = "D"
        
        for each_city in cityinfo: #for循环中是对shapefile格式数据的处理，与主要程序逻辑无关 
        
            city_num = each_city['City_Numbe']
            
            # !!!!!!!
            slope = -1*data1[city_num-1,i]     #---------------调这里选择不同类型的土地-----------------#
            
            if np.isnan(slope):
                # print(city_num, 'nan value detected')
                colors[city_num-1] = 'w'
            
            # colors[city_num-1] = cmap(np.sqrt((slope - slope_min) / (slope_max - slope_min)))[:3] #构建色彩映射关系 
            else:
                colors[city_num-1] = cmap((slope - slope_min) / (slope_max - slope_min))[:3] #构建色彩映射关系 
            
        # # 为每个图形设置填充色  
        for info, shape in zip(m.cities_info, m.cities):
            cnum = info['City_Numbe']
          
            # color = rgb2hex(colors[cnum]) #将RGB色彩转为HEX色彩 
            color = colors[cnum-1] 
            poly = Polygon(shape, facecolor=color) #将每个省份对应的颜色进行填充 
         
            ax.add_patch(poly)
        
        # --------------------------------------绘制南海区域子图------------------------------------------- # 
        axins = zoomed_inset_axes(ax, 0.6, loc = 4)
        axins.set_xlim(lons + 38, lons + 52)
        axins.set_ylim(lons, lons + 20)
        
        map2 = Basemap(llcrnrlon = lons + 34, llcrnrlat = lats-14, urcrnrlon = lons + 52, urcrnrlat = lats + 9,ax = axins)           
        shapefile2= r'D:\China_map\SouthOcean'
        map2.readshapefile(shpfile, 'China',  linewidth=0.2)    
        map2.readshapefile(shapefile2, 'ChinaSouthSea')  
        map2.readshapefile(cityshppath[:-4], 'cities',  linewidth=0.1)
        
        patches2   = []    
        for info2, shape2 in zip(map2.cities_info, map2.cities):
            cnum = info2['City_Numbe']
          
            # color = rgb2hex(colors[cnum]) #将RGB色彩转为HEX色彩 
            color = colors[cnum-1] #将RGB色彩转为HEX色彩 
            poly = Polygon(shape2, facecolor=color) #将每个省份对应的颜色进行填充 
            axins.add_patch(poly)
            
        # axins.add_collection(PatchCollection(patches, facecolor= 'lightblue', edgecolor='k', linewidths=1., zorder=2))
        
        mark_inset(ax, axins, loc1=2, loc2=2, fc = "none", ec = "none")
        # --------------------------------------绘制南海区域子图------------------------------------------- # 
    
          # 添加 colorbar
        norm = cm.colors.Normalize(vmin=slope_min, vmax=slope_max)
        cb = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        cb.set_array([])
        # colorbar = plt.colorbar(cb, orientation='vertical', pad=0.01,  ax=ax, extend = 'both')  # 将colorbar位置设置为右侧
        colorbar = plt.colorbar(cb, orientation='horizontal', pad=0.01,  ax=ax, extend = 'both')  # 将colorbar位置设置为右侧 
     
    
        colorbar.ax.tick_params(labelsize=28)
        if j!=2:
            label = f'{metricstr} decrease ($\mu g/m^3$)'
        if j==2:
            label = f'{metricstr} decrease ($mg/m^3$)'
        colorbar.set_label(label, fontsize=28)  # 设置标签字体大小
        
        # outpath = 'D:\\3MTDNN_v2.0\\Yearly_scale_experiments\\Yearly_retrievals_analysis\\figures\\NEV_contributed_pollution_change\\'
        # outfig=outpath+'NEV_contributed_pollution_change_'+metric+'_'+str(i+2016)+'.png'
        # plt.savefig(outfig, bbox_inches='tight', pad_inches=0.02)


        outpath = 'D:\\3MTDNN_v2.0\\paper\\NatureHealth\\revised\\round2\\Figures\\'
        outfig=outpath+'Figure4'+acode+'2.svg'
        plt.savefig(outfig)
        plt.show()
        
        
        