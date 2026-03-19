
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from matplotlib.patches import Polygon
import pandas as pd

# READ annual variation rate file

pollstr = 'PM25'
# pollstr = 'NO2'
# pollstr = 'CO'
# pollstr = 'PM10'
# pollstr = 'O3'

filename = 'Annual_variation_rate_for_different_cities_'+pollstr+'_fillnan_forest.xlsx'
excel_file = pd.ExcelFile(filename)
df1 = pd.read_excel(excel_file)
data1 = df1.to_numpy()
data1 = data1[:,1:]


cityshppath ='merged_output_150cities.shp'

fig = plt.figure(figsize=(8,6),dpi=300)
# fig = plt.figure(figsize=(12,6),dpi=300)
ax = fig.add_subplot(111)  

lons = 73
lone = 136
lats = 17
late = 55

m = Basemap(llcrnrlat = lats, urcrnrlat = late, llcrnrlon = lons, urcrnrlon = lone)

shpfile = r'D:\China_map\utf-8\Export_Output_2'
m.readshapefile(shpfile, 'states', drawbounds=True, linewidth=0.4)

m.readshapefile(cityshppath[:-4], 'cities',  linewidth=0.2)
cityinfo = m.cities_info 

colors = {}
cmap = plt.cm.PiYG_r

diff = data1[:,9]-data1[:,1]   # forest-road
diff_max = max([abs(min(diff)),abs(max(diff))])
diff_min = -1*diff_max

if pollstr == 'CO':
    diff_min = -0.06
    diff_max = 0.06
    
if pollstr == 'PM25':
    diff_min = -3
    diff_max = 3
    
if pollstr == 'NO2':
    diff_min = -1.5
    diff_max = 1.5
    
if pollstr == 'PM10':
    diff_min = -6
    diff_max = 6

if pollstr == 'O3':
    diff_min = -2.5
    diff_max = 2.5
        
for each_city in cityinfo:

    city_num = each_city['City_Numbe']
    
    slope = data1[city_num-1,8]    
    diff0 = diff[city_num-1]
    
    colors[city_num-1] = cmap((diff0 - diff_min) / (diff_max - diff_min))[:3] 
     
for info, shape in zip(m.cities_info, m.cities):
    cnum = info['City_Numbe']
  
    color = colors[cnum-1] 
    poly = Polygon(shape, facecolor=color) 
 
    ax.add_patch(poly)


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
  
  
    color = colors[cnum-1]
    poly = Polygon(shape2, facecolor=color) 
    axins.add_patch(poly)
    

mark_inset(ax, axins, loc1=2, loc2=2, fc = "none", ec = "none")


 # add colorbar
norm = cm.colors.Normalize(vmin=diff_min, vmax=diff_max)
cb = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
cb.set_array([])
colorbar = plt.colorbar(cb, orientation='horizontal', pad=0.01,  ax=ax, extend = 'both')  

# cb.set_ticks(np.arange(slope_min, slope_max))
# cbar.set_ticks(ll2)
colorbar.ax.tick_params(labelsize=20)
if pollstr != 'CO':
    colorbar.set_label(r'Difference ($\mu$g/${m^3}$/y)', fontsize=20)  
if pollstr == 'CO':
    colorbar.set_label(r'Difference (mg/${m^3}$/y)', fontsize=20)  

plt.show()