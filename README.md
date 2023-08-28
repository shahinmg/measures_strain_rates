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