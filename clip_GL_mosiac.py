#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:49:44 2023

@author: laserglaciers
"""
import sys
import os
from multiprocessing import Pool, cpu_count

sys.path.append('/usr/share/qgis/python/')

extent = [-271816.463800000,-69365.382000000,-2324947.243600000,-2071116.531200000] # rectangle around 4 west greenland glaciers


gl_mosiac_path = '/media/laserglaciers/upernavik/kevin_vels/measures_0731_vx_vy_files/'
gl_mosiacs = [mosiac for mosiac in os.listdir(gl_mosiac_path)]

os.chdir(gl_mosiac_path)
def gdal_extent_clip(gl_mosiac):
    print(f'processing {gl_mosiac}')
    op = '/media/laserglaciers/upernavik/kevin_vels/0731_clip/'
    dst = f'{op}{gl_mosiac[:-4]}-clip.tif'
    processing.run("gdal:cliprasterbyextent", 
                   {'INPUT':f'{gl_mosiac}',
                    'PROJWIN':f'{extent[0]}, {extent[1]}, {extent[2]}, {extent[3]} [EPSG:3413]',
                    'OVERCRS':False,'NODATA':None,'OPTIONS':'',
                    'DATA_TYPE':0,'EXTRA':'',
                    'OUTPUT':f'{dst}'})

    return

for mosiac in gl_mosiacs:
    gdal_extent_clip(mosiac)