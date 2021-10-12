# Program to plot GOES-R True Color + IR imagery
#
# Joseph B. Zambon
# jbzambon@ncsu.edu
# 5 April 2019

import numpy as np
from datetime import datetime, timedelta
from pyproj import Proj
import xarray
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import sys
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mpl

# Sounding location
s_loc = np.array([35.407,-74.691])

file = sys.argv[-1]
print('Processing: ' + file)
M1 = xarray.open_dataset(file)

# Load the RGB arrays
R = M1['CMI_C02'][:].data
G = M1['CMI_C03'][:].data
B = M1['CMI_C01'][:].data
# High-Level Water Vapor (Channel 8)
WV08 = M1.variables['CMI_C08']
# Mid-Level Water Vapor (Channel 9)
WV09 = M1.variables['CMI_C09']
# Low-Level Water Vapor (Channel 10)
WV10 = M1.variables['CMI_C10']

# Turn empty values into nans
R[R==-1] = np.nan
G[G==-1] = np.nan
B[B==-1] = np.nan

# Apply range limits for each channel becuase RGB values must be between 0 and 1
R = np.maximum(R, 0)
R = np.minimum(R, 1)
G = np.maximum(G, 0)
G = np.minimum(G, 1)
B = np.maximum(B, 0)
B = np.minimum(B, 1)

# Apply the gamma correction
gamma = 0.4
R = np.power(R, gamma)
G = np.power(G, gamma)
B = np.power(B, gamma)

# Calculate the "True" Green
G_true = 0.48358168 * R + 0.45706946 * B + 0.06038137 * G
G_true = np.maximum(G_true, 0)
G_true = np.minimum(G_true, 1)

cleanIR = M1.variables['CMI_C13'][:].data
cleanIR[cleanIR==-1] = np.nan

# Apply range limits for clean IR channel
cleanIR = np.maximum(cleanIR, 90)
cleanIR = np.minimum(cleanIR, 313)

# Normalize the channel between a range
cleanIR = (cleanIR-90)/(313-90)

# Invert colors
cleanIR = 1 - cleanIR

# Lessen the brightness of the coldest clouds so they don't appear so bright near the day/night line
cleanIR = cleanIR/1.2

# The final RGB array :)
RGB = np.dstack([R, G_true, B])

# The final IR array
IR = np.dstack([cleanIR, cleanIR, cleanIR])

RGB_IR = np.dstack([np.maximum(R, cleanIR), np.maximum(G_true, cleanIR), np.maximum(B, cleanIR)])

# Scan's start time, converted to datetime object
scan_start = datetime.strptime(M1.time_coverage_start, '%Y-%m-%dT%H:%M:%S.%fZ')

# Satellite height
sat_h = M1['goes_imager_projection'].perspective_point_height

# Satellite longitude
sat_lon = M1['goes_imager_projection'].longitude_of_projection_origin

# Satellite sweep
sat_sweep = M1['goes_imager_projection'].sweep_angle_axis

# The projection x and y coordinates equals
# the scanning angle (in radians) multiplied by the satellite height (http://proj4.org/projections/geos.html)
x = M1['x'][:] * sat_h
y = M1['y'][:] * sat_h


parallels = np.arange(0.,90,2.)
meridians = np.arange(180.,360.,2.)

# map object with pyproj
p = Proj(proj='geos', h=sat_h, lon_0=sat_lon, sweep=sat_sweep)

# Convert map points to latitude and longitude with the magic provided by Pyproj
XX, YY = np.meshgrid(x, y)
lons, lats = p(XX, YY, inverse=True)

mH = Basemap(resolution='i', projection='merc', \
            lat_1=38.5, lat_2=38.5, \
            lat_0=38.5, lon_0=-97.5, \
            llcrnrlon=-81.3,llcrnrlat=28,
            urcrnrlon=-70.9,urcrnrlat=39.5)
x_loc,y_loc = mH(s_loc[1], s_loc[0])

xH, yH = mH(lons, lats)

# Create a color tuple for pcolormesh
rgb = RGB_IR[:,:-1,:] 
colorTuple = rgb.reshape((rgb.shape[0] * rgb.shape[1]), 3)
colorTuple = np.insert(colorTuple, 3, 1.0, axis=1)

# Now we can plot the GOES data on the HRRR map domain and projection
fig = plt.figure(figsize=[16, 20],dpi=100)

# Visible + IR
ax = fig.add_subplot(221)
newmap = mH.pcolormesh(xH, yH, R, color=colorTuple, linewidth=0)
newmap.set_array(None)

mH.plot(x_loc, y_loc, 'k*', markersize=16)   #Sounding location
mH.drawstates()
mH.drawcountries()
mH.drawcoastlines()
mH.drawparallels(parallels,labels=[1,0,0,0],fontsize=18)
mH.drawmeridians(meridians,labels=[0,0,0,1],fontsize=18)

plt.title('GOES-16 True Color + IR',fontweight='semibold', loc='left', fontsize=20)

# High Water Vapor
ax = fig.add_subplot(222)
cmap_WV = LinearSegmentedColormap.from_list('this', ['darkgreen', 'green', 'lightgreen', 'white', 'blue', 'yellow', 'red', 'k'])

newmap = mH.pcolormesh(xH, yH, WV08, cmap=cmap_WV, linewidth=0,vmax=280, vmin=180)
mH.plot(x_loc, y_loc, 'k*', markersize=16)   #Sounding location
mH.drawstates()
mH.drawcountries()
mH.drawcoastlines()
mH.drawparallels(parallels,labels=[1,0,0,0],fontsize=18)
mH.drawmeridians(meridians,labels=[0,0,0,1],fontsize=18)

plt.title('GOES-16 High-Level Water Vapor',fontweight='semibold', loc='left', fontsize=20)

# Mid Water Vapor
ax = fig.add_subplot(223)
cmap_WV = LinearSegmentedColormap.from_list('this', ['darkgreen', 'green', 'lightgreen', 'white', 'blue', 'yellow', 'red', 'k'])

newmap = mH.pcolormesh(xH, yH, WV09, cmap=cmap_WV, linewidth=0,vmax=280, vmin=180)
mH.plot(x_loc, y_loc, 'k*', markersize=16)   #Sounding location
mH.drawstates()
mH.drawcountries()
mH.drawcoastlines()
mH.drawparallels(parallels,labels=[1,0,0,0],fontsize=18)
mH.drawmeridians(meridians,labels=[0,0,0,1],fontsize=18)

plt.title('GOES-16 Mid-Level Water Vapor',fontweight='semibold', loc='left', fontsize=20)

# Low Water Vapor
ax = fig.add_subplot(224)
cmap_WV = LinearSegmentedColormap.from_list('this', ['darkgreen', 'green', 'lightgreen', 'white', 'blue', 'yellow', 'red', 'k'])

newmap = mH.pcolormesh(xH, yH, WV10, cmap=cmap_WV, linewidth=0,vmax=280, vmin=180)
mH.plot(x_loc, y_loc, 'k*', markersize=16)   #Sounding location
mH.drawstates()
mH.drawcountries()
mH.drawcoastlines()
mH.drawparallels(parallels,labels=[1,0,0,0],fontsize=18)
mH.drawmeridians(meridians,labels=[0,0,0,1],fontsize=18)

plt.title('GOES-16 Low-Level Water Vapor',fontweight='semibold', loc='left', fontsize=20)

ax = fig.add_axes([0.15, 0.045, 0.7, 0.02])
norm = mpl.colors.Normalize(vmin=180, vmax=280)
cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap_WV,
                                norm=norm,
                                orientation='horizontal')
cb1.set_label('Brightness Temperature (K)',fontsize=22)
cb1.ax.tick_params(labelsize=18)

fig.suptitle('%s' % scan_start.strftime('%H:%M UTC %d %B %Y'), fontsize=36)

plt.savefig(file[:-3] + ".png")
print('Saved: ' + file[:-3] + ".png")

