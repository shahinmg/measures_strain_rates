#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 12:46:49 2023

@author: laserglaciers
"""

import iceutils as ice
import os
import numpy as np
import rasterio
from multiprocessing import Pool, cpu_count

vel_path = './0731_velocity_clip_filled_example/'
vel_vx_data = [opt for opt in os.listdir(vel_path) if opt.endswith('vx_v03.0-clip-filled.tif') or opt.endswith('vx_v03.1-clip-filled.tif.0.tif')]
vel_vy_data = [opt for opt in os.listdir(vel_path) if opt.endswith('vy_v03.0-clip-filled.tif') or opt.endswith('vy_v03.1-clip-filled.tif')]

op = '../0731_strain_rates_example/' #out path

# get matching velocity pairs
matched_vels = []
for x_vel in vel_vx_data:
    
    prefix = x_vel[:37]
    for y_vel in vel_vy_data:
        if y_vel.startswith(prefix):
            matched_vels.append((x_vel,y_vel))


os.chdir(vel_path)
def strain_rate_calc_worker(u_vel_path,v_vel_path):
    # print(f'computing {u_vel_path} & {v_vel_path} strain rates')
    
    u_vel_src = rasterio.open(u_vel_path)
    v_vel_src = rasterio.open(v_vel_path)
    
    #get dx and dy
    dx, dy = u_vel_src.transform[0], u_vel_src.transform[4]
    
    u_vel = u_vel_src.read(1) # read first band of x comp vel
    v_vel = v_vel_src.read(1) # read first band of v comp vel
    
    #compute strain rates and rotate to flow direction
    strain_dict, stress_dict = ice.compute_stress_strain(u_vel, v_vel, dx=dx, dy=dy,
                                                         rotate=True)
    
    # pull out strain rate components from strain_dict 
    e_xx = strain_dict['e_xx']
    e_yy = strain_dict['e_yy']
    e_xy = strain_dict['e_xy']
    dilatation = strain_dict['dilatation']
    effective = strain_dict['effective']
    
    
    strain_rate_bands = [e_xx, e_yy, e_xy, dilatation, effective]
    band_names = ['e_xx', 'e_yy', 'e_xy', 'dilatation', 'effective']
    
    meta = u_vel_src.meta.copy()
    meta['count'] = len(strain_rate_bands)
    
    # out_file = f'{op}{u_vel_path[:19]}-strain-rates.tif'
    out_file = f'{op}{u_vel_path[:37]}-strain-rates.tif'
    print(f'saving {out_file}')
    with rasterio.open(out_file,mode='w',**meta) as dst:
        for band_num, band in enumerate(strain_rate_bands, start=1):
            dst.write(band,band_num)
            dst.set_band_description(band_num, band_names[band_num-1])
    
    
    
    u_vel_src.close()
    v_vel_src.close()
    
    
    return
    
if __name__ == "__main__":
    with Pool(processes=cpu_count()-5) as pool:
          results = pool.starmap(strain_rate_calc_worker, matched_vels)
        
        