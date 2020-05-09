import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker
import cartopy.crs as ccrs 
import cartopy.feature
import numpy as np
import os 

import argparse

from scipy.interpolate import griddata

from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
from lambertTicks import lambert_xticks, lambert_yticks
import getData
from addparser import getParser

def main(parser):
    args = parser.parse_args()
    infilename = args.input

    img_extent = (105, 175, 15, 57) 
    fig = plt.figure(figsize=(16.0,10.0)) 
    plt.subplots_adjust(left=0.08,right=0.97,bottom=0.08,top=0.94)
    
    ax = plt.axes(zorder=0, projection=ccrs.LambertConformal(central_longitude=145.0,central_latitude=35,standard_parallels=(30,60)))
    ax.coastlines(resolution='10m',lw=0.5)
    ax.set_extent(img_extent,ccrs.PlateCarree())
    xticks = np.arange(50,190,5).tolist()
    yticks = np.arange(0,90,5).tolist()
    xticks.append(-175)
    xticks.append(-170)
    xticks.append(-165)
    xticks.append(-160)
    #ax.stock_img()
    ax.gridlines(xlocs=xticks,
                 ylocs=yticks,
                 linestyle='dotted',
                 linewidth=0.5,
                 color='dimgray',
                 zorder=1,
                 draw_labels=False)

    fig.canvas.draw()

    ax.axes.tick_params(labelsize=12)
    ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
    ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)
    lambert_xticks(ax, xticks, 'bottom')
    lambert_yticks(ax, yticks, 'left')
    ax.add_feature(cartopy.feature.LAND)
    
    title, lat, lon, pre = getData.getData(infilename)
    ax.scatter(lon,lat,c=pre,transform=ccrs.PlateCarree(),s=5)

    X, Y, Z = grid(lon, lat, pre)
    levels = np.arange(960,1040,2)
    cont = ax.contour(X,Y,Z,transform=ccrs.PlateCarree(),linewidths=1,levels=levels)
    clevels = cont.levels
    cont.clabel(clevels[::2],fmt='%d',fontsize=10)

    fig.text(0.15,0.9,title)

    os.system('mkdir -p result')
    plt.savefig(f'result/{title}.pdf')
    plt.show()
    
def grid(x, y, z, resX=1000, resY=1000):
    "Convert 3 column data to matplotlib grid"
    #xi = np.linspace(min(x), max(x), resX)
    #yi = np.linspace(min(y), max(y), resY)
    xi = np.linspace(-180, 180, resX)
    yi = np.linspace(-90, 90, resY)
    Z = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')
    X, Y = np.meshgrid(xi, yi)
    return X, Y, Z 

if __name__ == "__main__":
    parser = getParser()
    main(parser)
