#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 09:34:12 2023

@author: laserglaciers
"""

import os
import pathlib
import shutil

measures_0646_dir = 'measures_0646_vx_vy_files'
measures_0731_dir = 'measures_0731_vx_vy_files'

rootdir = '/media/laserglaciers/upernavik/kevin_vels/'

measures_0646 = '/media/laserglaciers/upernavik/kevin_vels_moved/measures_0646_vx_vy_files/'
measures_0731 = '/media/laserglaciers/upernavik/kevin_vels_moved/measures_0731_vx_vy_files/'

for subdir, dirs, files in os.walk(rootdir):
    subdir_name = os.path.split(subdir)[-1]
    
    if subdir_name == measures_0646_dir:
        os.chdir(subdir)
        print(subdir_name)
        for file in files:
            dst = f'{measures_0646}{file}'
            shutil.copy2(file, dst)
        
        
    elif subdir_name == measures_0731_dir:
        os.chdir(subdir)
        print(subdir_name)
        for file in files:
            dst = f'{measures_0731}{file}'
            shutil.copy2(file, dst)
    
    # for file in files:
    #     print(os.path.join(subdir, file))