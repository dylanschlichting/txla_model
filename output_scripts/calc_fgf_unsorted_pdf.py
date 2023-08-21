"""
Script to save probability density functions for TXLA parent and child model 
output of the normalized frontogenesis function  NOT sorted by 
relative vorticity>1, which indicates an active front is present.See
mnum_fgf_TXLA.ipynb for relevant theory and explanation of the functions.
"""
#Packages
import numpy as np
import xgcm
from xgcm import Grid
import xarray as xr
import xroms
from xhistogram.xarray import histogram
import glob

# Open model output
def open_roms(path):
    ds1 = xroms.open_mfnetcdf(path)
    ds1, grid1 = xroms.roms_dataset(ds1)
    return ds1, grid1

paths = [glob.glob('/d1/shared/TXLA_ROMS/numerical_mixing/non-nest/ver1/1hr/ocean_avg_0000*.nc'),
         glob.glob('/d1/shared/TXLA_ROMS/numerical_mixing/nest/ver1/ocean_avg_child_0000*.nc')]

ds = []
grid = []
for i in range(len(paths)):
    ds1, grid1 = open_roms(paths[i])
    ds.append(ds1)
    grid.append(grid1)

# Functions for FGF and rel. vort.
def norm_fgf(ds,grid, q):
    '''
    Code to calculate 2D normalized FGF. See mnum_fgf_TXLA.ipynb for details. 
    '''
    dqdx = xroms.to_rho(grid.derivative(q, 'X'),grid) # defined at rho-points
    dqdy = xroms.to_rho(grid.derivative(q, 'Y'),grid)

    us = ds.u.isel(s_rho = -1) # surface velocity field
    vs = ds.v.isel(s_rho = -1)

    dudx = grid.derivative(us, 'X', boundary='extend')
    dvdy = grid.derivative(vs, 'Y', boundary='extend')
    dudy = xroms.to_rho(grid.derivative(us, 'Y', boundary='extend'),grid)
    dvdx = xroms.to_rho(grid.derivative(vs, 'X', boundary='extend'),grid)

    Dgradq_i = - dudx*dqdx - dvdx*dqdy
    Dgradq_j = - dudy*dqdx - dvdy*dqdy

    # The frontogenesis function
    Ddelq2 = (dqdx*Dgradq_i + dqdy*Dgradq_j)
    Ddelq2.name = 'FGF'

    # Density gradients squared
    gradq2 = dqdx**2 + dqdy**2
    gradq2.name = r'$(\nabla q)^2$'

    # Normalized frontogenesis function
    nFGF = Ddelq2 / (gradq2 * ds.f)
    nFGF.name = r'nFGF'
    return nFGF
    
# Run the functions, sort by fronts (zeta>1), and save area for weighting
fgf = []
dA = []
for i in range(len(paths)):
    nfgf = norm_fgf(ds[i], grid[i], ds[i].salt.isel(s_rho = -1))
    dA1 = ds[i].dA
    fgf.append(nfgf)
    dA.append(dA1)

# Slices for analysis. Indices determined in 'numerical_mixing' repository
tslice = slice('06-10-2010','06-16-2010') # Take a week of model output
xislicep = slice(271,404)
etaslicep = slice(31,149)

xislicec = slice(8, 677-8)
etaslicec = slice(8, 602-8)

# Individually slice fgf and dA. Could have automated by it's unambiguous this way
Fp = fgf[0].isel(xi_rho=xislicep,eta_rho=etaslicep).sel(ocean_time = tslice) #Parent FGF
Fc = fgf[1].isel(xi_rho=xislicec,eta_rho=etaslicec).sel(ocean_time = tslice) #Child FGF

Ap = dA[0].isel(xi_rho=xislicep,eta_rho=etaslicep) #Parent area
Ac = dA[1].isel(xi_rho=xislicec,eta_rho=etaslicec) #Child area

# Compute histograms
fgf_bins = np.linspace(-5,7,151)
fp_pdf = histogram(Fp, bins=[fgf_bins], weights = Ap,
                   density = True)
fc_pdf = histogram(Fc, bins=[fgf_bins], block_size = len(ds[1].ocean_time), 
                   weights = Ac, density = True)
# Save
fp_pdf.to_netcdf('txla_nFGF_unsrt_pdf_par_june_10_16_2010.nc')
fc_pdf.to_netcdf('txla_nFGF_unsrt_pdf_chi_june_10_16_2010.nc')