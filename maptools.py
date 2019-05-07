import numpy as np
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

def make_map(projection=ccrs.PlateCarree()):
    '''
    Return axis object for cartopy map with labeled gridlines.
    
    Input: Cartopy projection, default = cartopy.crs.PlateCarree()
    Output: Cartopy axis object
    
    Based on blog post by Filipe Fernandes:
    https://ocefpaf.github.io/python4oceanographers/blog/2015/06/22/osm/
    License: Creative Commons Attribution-ShareAlike 4.0
    https://creativecommons.org/licenses/by-sa/4.0/
    
    Example code:
    
    import cartopy.crs as ccrs
    plt.figure()
    ax = make_map(projection=ccrs.Mercator())
    ax.coastlines()
    '''
    ax = plt.axes(projection=projection)
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return ax

def load_crm_asc(data_file):
    '''
    Load bathymetry data from NOAA Coastal Relief model data set.
    For data in ascii format generated at:
    http://maps.ngdc.noaa.gov/viewers/wcs-client/
    
    Returns:
    z: m x n array of elevation values (negative for depth in ocean, positive on land)
    lon: array of n longitude values
    lat: array of m latitude values
    
    Tom Connolly, MLML (3/2016)
    '''

    # read information from header lines
    f = open(data_file)
    lines = f.readlines()
    ncols = int(lines[0][10:])
    nrows = int(lines[1][10:])
    xllcorner = float(lines[2][10:])
    yllcorner = float(lines[3][10:])
    cellsize = float(lines[4][10:])
    # create latitude and longitude arrays from info in header
    lon = np.empty(ncols)
    lat = np.empty(nrows)
    for ii in range(ncols):
        lon[ii] = xllcorner+cellsize*ii
    for jj in range(nrows):
        lat[jj] = yllcorner+cellsize*jj
    lat = lat[::-1] # flip latitude array so first row (top) is highest latitude
    
    # read elevation data
    z = np.genfromtxt(data_file,skip_header=5,delimiter=' ')
    return z, lon, lat