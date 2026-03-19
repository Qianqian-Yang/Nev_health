# -*- coding: utf-8 -*-

import copy
import matplotlib as mpl

from matplotlib.pyplot import MultipleLocator
import math
from scipy.stats import linregress
from osgeo import gdal 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

font2 = {'family' : 'Arial','weight' : 'normal','size'   : 18,}

for pollut in range(0,1):
       
    if pollut == 0:
        pollstr = 'PM25'
        # minv = 1
        # maxv = 8
        x_major_locator=MultipleLocator(1)
        maxd = 3
        mind = -1*maxd
        
    if pollut == 1:
        pollstr = 'NO2'   
        # minv = 0.5
        # maxv = 2.8
        x_major_locator=MultipleLocator(0.5)
        maxd = 1.5
        mind = -1*maxd
        
    if pollut == 2:
        pollstr = 'CO'
        # minv = 0.02
        # maxv = 0.11
        x_major_locator=MultipleLocator(0.02)
        maxd = 0.06
        mind = -1*maxd
        
    if pollut == 3:
        pollstr = 'O3'        
        # minv = -2
        # maxv = 1.5
        x_major_locator=MultipleLocator(1)
        maxd = 2
        mind = -1*maxd
        
        
    if pollut == 4:
        pollstr = 'PM10'       
        # minv = 2
        # maxv = 11
        x_major_locator=MultipleLocator(2)
        maxd = 6
        mind = -1*maxd
        
    filename = 'Annual_variation_rate_for_different_cities_'+pollstr+'_fillnan_forest.xlsx'
    excel_file = pd.ExcelFile(filename)
    
    df = pd.read_excel(excel_file)
    data0 = df.to_numpy()
    
    # 2 road  3 cityroad  4 motroway      10 forest  13 imperivous
    x = -1*data0[:,10]
    y = -1*data0[:,2]
    
    diff = y-x
    num1 = sum(diff>0)
    num2 = sum(diff<0)
     
    minv=math.floor(min([min(x),min(y)]))
    maxv=math.ceil(max([max(x),max(y)]))
 
    if pollut == 1:
        minv = 0.3
        maxv = 2.6
    if pollut == 2:
        minv = 0.01
        maxv = 0.15
        
    plt.figure(figsize=(6, 5),dpi=300)
    plt.scatter(x, y, c=diff, s=70, cmap='PiYG_r', vmin = mind, vmax =maxd)
        
    cmap2 = copy.copy(mpl.cm.PiYG_r)
    cmap2.set_under(cmap2(0))
    cmap2.set_over(cmap2(1.0))
    norm2 = mpl.colors.Normalize(vmin= mind, vmax =maxd)
    im2 = mpl.cm.ScalarMappable(norm=norm2, cmap=cmap2)
    cbar2 = plt.colorbar(im2,
        # orientation='horizontal',
        extend='both', ticks=np.linspace(mind, maxd, 5),
        label='Difference'
    )
    cbar2.ax.tick_params(labelsize=18) 
    cbar2.set_label('Difference',fontdict=font2) 

    
    # number of city
    plt.text(0.25*maxv, 0.75*maxv, num1, size = 18, color = cmap2(1.0), weight='bold',  alpha = 1)
    plt.text(0.86*maxv, 0.7*maxv, num2, size = 18, color = cmap2(0), weight='bold', alpha = 1)
    
    # 1:1 line
    plt.plot((minv, maxv), (minv, maxv), ls='--',c='k', linewidth=1)

    
    ax=plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(x_major_locator)
    
    plt.xlim(minv,maxv)
    plt.ylim(minv,maxv)
    
    plt.tick_params(labelsize=18)

    if pollut != 2:
        plt.xlabel(r'Decreasing rate of background($\mu$g/${m^3}$/y)', font2)
        plt.ylabel(r'Decreasing rate of roads($\mu$g/${m^3}$/y)', font2)
    if pollut == 2:
        plt.xlabel(r'Decreasing rate of background(mg/${m^3}$/y)', font2)
        plt.ylabel(r'Decreasing rate of roads(mg/${m^3}$/y)', font2)
        
    
    
    