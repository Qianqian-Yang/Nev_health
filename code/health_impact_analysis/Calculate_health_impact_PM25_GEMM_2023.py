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

mortality = 'Mortality_data_2023.xlsx'
excel_file3 = pd.ExcelFile(filepath+mortality)
df31 = pd.read_excel(excel_file3, sheet_name = 'All_caluse_mortality_data_2023')
mr_allcause = df31.to_numpy()

df32 = pd.read_excel(excel_file3, sheet_name = 'LRI_NCD_mortality_data_2023')
mr_NCDLRI = df32.to_numpy()


popfile ='Population_data_age.xlsx'
excel_file4 = pd.ExcelFile(filepath+popfile)
df4 = pd.read_excel(excel_file4)
pop = df4.to_numpy()


#---3. GEMM model
def calRR_GEMM(C_i, C_cf, theta_jk, alpha_jk, mu_jk, v_jk):
    
    if C_i <= C_cf:
        return 1
    else:
        log_term = np.log((C_i - C_cf) / alpha_jk + 1)
        exp_term = np.exp(-(C_i - C_cf - mu_jk) / v_jk)
        rr = np.exp(theta_jk * log_term / (1 + exp_term))
        return rr

# divide 12 age groups 

# AGE >25	27.5	32.5	37.5	42.5	47.5	52.5	57.5	62.5	67.5	72.5	77.5	85
C_cf = 2.38
theta_list = np.array([0.1585, 0.1577, 0.157, 0.1558, 0.1532, 0.1499, 0.1462,	0.1421,	0.1374,	0.1319,	0.1253,	0.1141] )
theta_SE_list = np.array([0.01477, 0.01470, 0.01463, 0.01450, 0.01425, 0.01394, 0.01361, 0.01325, 0.01284, 0.01234, 0.01174, 0.01071] )
theta_upper_list = theta_list + 1.96*theta_SE_list
theta_lower_list = theta_list - 1.96*theta_SE_list

alpha = 1.6
mu = 15.5  
v = 36.8   

pop_80above = pop[:,19]+pop[:,20]
pop_80above = pop_80above.reshape((-1,1))
popage = np.hstack((pop[:,8:19], pop_80above))
mrage_allcause = mr_allcause[:12,1]
mrage_NCDLRI = mr_NCDLRI[:12,1]
mrage_NCDLRI_upper = mr_NCDLRI[:12,2]
mrage_NCDLRI_lower = mr_NCDLRI[:12,3]

delta_mb = np.zeros((150,12))
arr1 = np.zeros((150,12))
arr2 = np.zeros((150,12))
mb1 = np.zeros((150,12))
mb2 = np.zeros((150,12))

for city in range(150):
    conpm1 = con1[city,2]
    conpm2 = con2[city,2]
    
    # AGE group 27.5	32.5	37.5	42.5	47.5	52.5	57.5	62.5	67.5	72.5	77.5	>80   in total 12 groups
    for agegroup in range(12):
        
        popcity = popage[city,agegroup]
        
        # I0 = mrage_allcause[agegroup]
        
        # I0 = mrage_NCDLRI[agegroup]
        # I0 = mrage_NCDLRI_upper[agegroup]
        I0 = mrage_NCDLRI_lower[agegroup]
        
        # theta = theta_list[agegroup]
        # theta = theta_upper_list[agegroup]
        theta = theta_lower_list[agegroup]
        
        
        rr1 = calRR_GEMM(conpm1, C_cf, theta, alpha, mu, v)
        arr1[city,agegroup] = rr1
        
        rr2 = calRR_GEMM(conpm2, C_cf, theta, alpha, mu, v)
        arr2[city,agegroup] = rr2
        
        mb1[city,agegroup] = ((rr1-1)/rr1)*I0*popcity
        mb2[city,agegroup] = ((rr2-1)/rr2)*I0*popcity
        
        delta_mb[city,agegroup] = mb2[city,agegroup]-mb1[city,agegroup]
        dratio = delta_mb/mb2
        ret = np.hstack((mb1,mb2, delta_mb ))

# # don't distinct age group

# C_cf = 2.38
# alpha = 1.6
# mu = 15.5  
# v = 36.8   
# theta = 0.143  #theta_SE = 0.01807

# delta_mb = np.zeros((150,1))
# arr1 = np.zeros((150,1))
# arr2 = np.zeros((150,1))
# mb1 = np.zeros((150,1))
# mb2 = np.zeros((150,1))

# for city in range(150):
#     conpm1 = con1[city,2]
#     conpm2 = con2[city,2] 
    
#     popcity = pop[city,21]

#     I0 = mr_NCDLRI[12,1]
      
#     rr1 = calRR_GEMM(conpm1, C_cf, theta, alpha, mu, v)
#     arr1[city,0] = (rr1-1)/rr1
    
#     rr2 = calRR_GEMM(conpm2, C_cf, theta, alpha, mu, v)
#     arr2[city,0] = (rr2-1)/rr2
    
#     mb1[city,0] = ((rr1-1)/rr1)*I0*popcity
#     mb2[city,0] = ((rr2-1)/rr2)*I0*popcity
    
#     delta_mb[city,0] = mb2[city,0]-mb1[city,0]
#     dratio = delta_mb/mb2
    
#     ret = np.hstack((mb1,mb2, delta_mb ))
    
        
        
