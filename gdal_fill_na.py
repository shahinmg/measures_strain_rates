#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 17:40:31 2023

@author: laserglaciers
"""

import os
import subprocess
from multiprocessing import Pool, cpu_count


# gdal_fillnodata.py 
# /media/laserglaciers/upernavik/kevin_vels/0731_clip/GL_vel_mosaic_Monthly_01Apr15_30Apr15_vx_v03.0-clip.tif 
# /media/laserglaciers/upernavik/kevin_vels/0731_clip_filled/test.tif 
# -md 10 -b 1 -of GTiff


input_vels_path = './0731_clip/'

vel_list = [vel for vel in os.listdir(input_vels_path) if vel.endswith('.tif')]
os.chdir(input_vels_path)
op = '/media/laserglaciers/upernavik/kevin_vels/0731_clip_filled/'
args_list = []
md = 10 # max distance
si = 0
band = 1
for vel in vel_list:
    
    
    # args = f'gdal_fillnodata.py -mb {md}'
    
    args = ['gdal_fillnodata.py', 
            '-md', f'{md}', 
            '-si',f'{si}',
            '-b', f'{band}',
            f'{vel}',
            '-of', 'GTiff',
            f'{op}{vel[:-4]}-filled.tif']
    args_list.append(args)
    
def worker(cmd):
    proc = subprocess.Popen(cmd)
    proc.wait()
    
    
if __name__ == "__main__":
    with Pool(processes=cpu_count()-2) as pool:
          results = pool.map(worker, args_list)
          