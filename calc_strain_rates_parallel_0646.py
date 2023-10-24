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

vel_path = './measures_0646_vx_vy_files/'
vel_vx_data = [opt for opt in os.listdir(vel_path) if opt.endswith('vx_v03.0.tif') or opt.endswith('vx_v03.1.tif')]
vel_vy_data = [opt for opt in os.listdir(vel_path) if opt.endswith('vy_v03.0.tif') or opt.endswith('vy_v03.1.tif')]

op = '../0646_strain_rates/' #out path

# get matching velocity pairs
matched_vels = []
for x_vel in vel_vx_data:
    
    prefix = x_vel[:19]
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
    
    
    # Morlighem effective tensile strain rate equation 6  DOI: 10.1002/2016GL067695
    
    # find principal  strain rates or "eigenvalues" of the strain rate tensor
    # using equation found here https://www.continuummechanics.org/principalstrain.html#:~:text=The%20principal%20orientation%20is%20tan(2%CE%B8P)%20%3D%202%20%E2%88%97,%2B%20(0.30)2%20%CF%B5max%2C%20%CF%B5min%20%3D%200.611%2C%20%E2%88%92%200.311
    first_term = (e_xx + e_yy)/2
    radicand = np.square(((e_xx - e_yy)/2)) + np.square((e_xy/2))
    second_term = np.sqrt(radicand)
    
    # get e1 and e2; The first and second principal strain rates or "eigenvalues"
    e1 = first_term + second_term
    e2 = first_term - second_term
    

    e1_eff = np.where(e1<0,0,e1)
    e2_eff = np.where(e2<0,0,e2)
    effective_tensile_sq = 0.5 * (np.square(e1_eff) + np.square(e2_eff))
    effective_tensile = np.sqrt(effective_tensile_sq) # this is what should be input in equation 7
    
    
    # using table 3.4 of creep parameter A values from cuffey and patteson pg 75 and 
    # an assumed ice temperature of -5 from Morlighem et al., 2016
    A = 9.3 * 10**-25 #s^-1 Pa^-3
    # need to convert from per second to per year to match computed strain rate units
    # and MPa to match the Morlighem text
    n = 3
    sec_in_yr = 86400 * 365
    An = A * sec_in_yr * 10**18 #yr^-1 MPa^-3
    # convert A to B using eq 2.13 in Kees' book
    B = An ** (-1/n) # MPa yr^1/3
    # B = 600 * 1e3
    # now compute the tensile von Mises stress from equation 7 in Morlighem et al., 2016
    vm_stress = np.sqrt(3) * B * np.power(effective_tensile,1/n) #MPa
    
    strain_rate_bands = [e_xx, e_yy, e_xy, dilatation, effective, effective_tensile, vm_stress]
    band_names = ['e_xx', 'e_yy', 'e_xy', 'dilatation', 'effective', 'effective_tensile', 'von_Mises_Stress']
    
    meta = u_vel_src.meta.copy()
    meta['count'] = len(strain_rate_bands)
    
    out_file = f'{op}{u_vel_path[:19]}-strain-rates.tif'
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
        
        