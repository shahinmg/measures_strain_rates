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

opt_path = './measures_0646_vx_vy_files'
opt_vx_data = [opt for opt in os.listdir(opt_path) if opt.endswith('vx_v03.1.tif') or opt.endswith('vx_v03.0.tif')]
opt_vy_data = [opt for opt in os.listdir(opt_path) if opt.endswith('vy_v03.1.tif') or opt.endswith('vy_v03.0.tif')]

op = '../opt_strain_rates/' #out path

# get matching velocity pairs
matched_vels = []
for x_vel in opt_vx_data:
    
    prefix = x_vel[:19]
    for y_vel in opt_vy_data:
        if y_vel.startswith(prefix):
            matched_vels.append((x_vel,y_vel))

os.chdir(opt_path)
for u_vel_path, v_vel_path in matched_vels[:2]:
    print(f'computing {u_vel_path} & {v_vel_path} strain rates')
    
    u_vel_src = rasterio.open(u_vel_path)
    v_vel_src = rasterio.open(v_vel_path)
    
    u_vel = u_vel_src.read(1) # read first band of x comp vel
    v_vel = v_vel_src.read(1) # read first band of v comp vel
    
    #compute strain rates and rotate to flow direction
    strain_dict, stress_dict = ice.compute_stress_strain(u_vel, v_vel,rotate=True)
    
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
    
    out_file = f'{op}{u_vel_path[:19]}-strain-rates.tif'
    with rasterio.open(out_file,mode='w',**meta) as dst:
        for band_num, band in enumerate(strain_rate_bands, start=1):
            dst.write(band,band_num)
            dst.set_band_description(band_num, band_names[band_num-1])
    
    
    
    u_vel_src.close()
    v_vel_src.close()