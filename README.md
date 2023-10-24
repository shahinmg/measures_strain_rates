## measures_strain_rates

`measures_strain_rates` uses [`iceutils`](https://github.com/bryanvriel/iceutils) to calculate strain rates from NASA's MEaSUREs velocity products ([0646 optical](https://nsidc.org/data/nsidc-0646/versions/3) and [0731 sar and landsat](https://nsidc.org/data/nsidc-0731/versions/3)). To use this, you will need to install `iceutils` and `rasterio`

## Installation

`iceutils` depends on these packages 

```
numpy
scipy
matplotlib
gdal
h5py
pyproj
scikit-image
tqdm
rasterio
opencv
scikit-learn
pint
cvxopt
```
Below is a slightly modified version of how to install `iceutils`
```
# Install requirements
conda install -c conda-forge --file=requirements.txt
```

To install `iceutils`, you may clone a read-only version of the repository:

```
git clone https://github.com/bryanvriel/iceutils.git
```
Or, if you are developer, you may clone with SSH:

```
git clone git@github.com:bryanvriel/iceutils.git
```
Then, simply run `pip install .` in the main repository directory to install.

In the cloned directory, you'll find several Python source files, each containing various functions and classes. While the naming of the source files gives a hint about what they contain, all functions are classes are imported into a common namespace. For example, the file `stress.py` contains a function `compute_stress_strain()`. This function would be called as follows:

```python
import iceutils as ice

stress_strain = ice.compute_stress_strain(vx, vy)
```
## Python file descriptions

### calc_strain_rates.py
`calc_strain_rates.py` calculates inputed component velocities and saves a strain rate tiff with the following bands
```
band 1: e_xx (units yr$^{-1}$)
band 2: e_yy (units yr$^{-1}$)
band 3: e_xy (units yr$^{-1}$)
band 4: dilatation (units yr$^{-1}$)
band 5: effective strain rate (units yr$^{-1}$)
band 6: effective_tensile strain rate (units yr$^{-1}$)
band 7: von_Mises_Stress (units Mpa)
```

### calc_strain_rates_parallel_0646.py & calc_strain_rates_parallel_0731
`calc_strain_rates_parallel_0646.py` and `calc_strain_rates_parallel_0731.py` calculates inputed component velocities and saves a strain rate tiff with the following bands in parallel using python's multiprocessing package
```
band 1: e_xx (units yr$^{-1}$)
band 2: e_yy (units yr$^{-1}$)
band 3: e_xy (units yr$^{-1}$)
band 4: dilatation (units yr$^{-1}$)
band 5: effective strain rate (units yr$^{-1}$)
band 6: effective_tensile strain rate (units yr$^{-1}$)
band 7: von_Mises_Stress (units Mpa)
```
the von Mises stress output in band 7 is calculated using the equations from [Morlighem et al (2016)](https://agupubs.onlinelibrary.wiley.com/doi/10.1002/2016GL067695). Effective tensile strain rate (band 6) comes from Morlighem et al (2016) equation 6
**von Mises equations**
$\tilde{\dot{\varepsilon}}_{e}^{2} = \frac{1}{2}(\max(0,\dot{\varepsilon}_{1})^{2} + (\max(0,\dot{\varepsilon}_{1})^{2})$
and the tensile von Mises stress as 
$$\tilde{\sigma} = \sqrt{3} B \tilde{\dot{\varepsilon}}_{e}^\frac{1}{n}$$


### clip_GL_mosiac.py
`clip_GL_mosiac.py` clips the 0731 velocity mosiacs to a specifc extent. This was done using QGIS' `gdal:cliprasterbyextent` tool with QGIS' python interpreter 

### gdal_fill_na.py
`gdal_fill_na.py` fills in missing data in the velocity raster. This was only used for the 0731 velocity data.


