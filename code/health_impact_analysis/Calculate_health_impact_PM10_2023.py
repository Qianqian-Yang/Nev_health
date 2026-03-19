# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

filepath = 'D:\\3MTDNN_v2.0\\Yearly_scale_experiments\\health_impact_analysis\\'
# Cname1 =  'City_pollution_concentration_data.xlsx'
Cname1 =  'Road_pollution_concentration_data_2023.xlsx'
excel_file1 = pd.ExcelFile(filepath+Cname1)
df1 = pd.read_excel(excel_file1)
con1 = df1.to_numpy()

# Cname2 =  'City_pollution_concentration_data_simulated_noNEV.xlsx'
Cname2 =  'Road_pollution_concentration_data_simulated_noNEV_2023_withBGC.xlsx'
excel_file2 = pd.ExcelFile(filepath+Cname2)
df2 = pd.read_excel(excel_file2)
con2 = df2.to_numpy()

mortality =  'Mortality_data_2023.xlsx'
excel_file3 = pd.ExcelFile(filepath+mortality)
df31 = pd.read_excel(excel_file3, sheet_name = 'All_caluse_mortality_data_2023')
mr_allcause = df31.to_numpy()

popfile ='Population_data_age.xlsx'
excel_file4 = pd.ExcelFile(filepath+popfile)
df4 = pd.read_excel(excel_file4)
pop = df4.to_numpy()

rr_pm10 = 1.0023
rr_pm10_LOWER = 1.0013
rr_pm10_UPPER = 1.0033
TMREL_pm10 = 0
scale_pm10 = 10

delta_mb = np.zeros((150,1))
apaf1 = np.zeros((150,1))
apaf2 = np.zeros((150,1))
mb1 = np.zeros((150,1))
mb2 = np.zeros((150,1))

delta_mb_LOWER = np.zeros((150,1))
apaf1_LOWER = np.zeros((150,1))
apaf2_LOWER = np.zeros((150,1))
mb1_LOWER = np.zeros((150,1))
mb2_LOWER = np.zeros((150,1))


delta_mb_UPPER = np.zeros((150,1))
apaf1_UPPER = np.zeros((150,1))
apaf2_UPPER = np.zeros((150,1))
mb1_UPPER = np.zeros((150,1))
mb2_UPPER = np.zeros((150,1))


for city in range(150):

    pm10_1 = con1[city,4]-con1[city,2]
    pm10_2 = con2[city,4] -con2[city,2]
    
    popcity = pop[city,22]

    # I0 = mr_NCDLRI[12,1]
    I0 = mr_allcause[12,1]
      
    rr1 = rr_pm10**((pm10_1-TMREL_pm10)/scale_pm10)
    paf1 = (rr1-1)/rr1 
    mb1[city,0] = paf1*I0*popcity
    apaf1[city,0] = paf1
    
    rr2 = rr_pm10**((pm10_2-TMREL_pm10)/scale_pm10)
    paf2 = (rr2-1)/rr2 
    mb2[city,0] = paf2*I0*popcity
    apaf2[city,0] = paf2
    
    delta_mb[city,0] = mb2[city,0]-mb1[city,0]
    dratio = delta_mb/mb2
    
    
    # LOWER
    paf1_LOWER = (rr_pm10_LOWER**((pm10_1-TMREL_pm10)/scale_pm10)-1)/rr_pm10_LOWER**((pm10_1-TMREL_pm10)/scale_pm10)
    mb1_LOWER[city,0] = paf1_LOWER*I0*popcity
    apaf1_LOWER[city,0] = paf1_LOWER
    
    paf2_LOWER = (rr_pm10_LOWER**((pm10_2-TMREL_pm10)/scale_pm10)-1)/rr_pm10_LOWER**((pm10_2-TMREL_pm10)/scale_pm10)
    mb2_LOWER[city,0] = paf2_LOWER*I0*popcity
    apaf2_LOWER[city,0] = paf2_LOWER
    
    delta_mb_LOWER[city,0] = mb2_LOWER[city,0]-mb1_LOWER[city,0]
    dratio_LOWER = delta_mb_LOWER/mb2_LOWER
    

    # UPPER
    paf1_UPPER = (rr_pm10_UPPER**((pm10_1-TMREL_pm10)/scale_pm10)-1)/rr_pm10_UPPER**((pm10_1-TMREL_pm10)/scale_pm10)
    mb1_UPPER[city,0] = paf1_UPPER*I0*popcity
    apaf1_UPPER[city,0] = paf1_UPPER
    
    paf2_UPPER = (rr_pm10_UPPER**((pm10_2-TMREL_pm10)/scale_pm10)-1)/rr_pm10_UPPER**((pm10_2-TMREL_pm10)/scale_pm10)
    mb2_UPPER[city,0] = paf2_UPPER*I0*popcity
    apaf2_UPPER[city,0] = paf2_UPPER
    
    delta_mb_UPPER[city,0] = mb2_UPPER[city,0]-mb1_UPPER[city,0]
    dratio_UPPER = delta_mb_UPPER/mb2_UPPER


re = np.hstack((mb1, mb2, delta_mb,mb1_UPPER,mb2_UPPER,delta_mb_UPPER,mb1_LOWER,mb2_LOWER,delta_mb_LOWER))
