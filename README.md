# txla_model
```txla_model``` is a metarepository for the Texas-Louisiana shelf hydrodynamic ROMS model. The information required to run the model can be found here. The bulk of the input generation and output postprocessing/analysis is done in Python. Output analysis is based on modern packages such as ```xroms```, which is built on ```xarray``` and ```xgcm```. It contains a panolpy of useful tools for working with ROMS output. 
## First steps: Create a conda environment
If you work in Python, we recommend creating a custom conda environment so package version control can be managed easily. To run the notebooks in this repository, an environment can be installed by running 
    conda install --file txla_model_req.txt
## Running the model - Inputs (future work)
> - grid generation
> - forcing generation
> - .in files
> - hprc scripts/resources
> - nested setup
## Working with model output (work in progress):
```txla_model``` has many tools for dealing with model output, including:
> - A condensed ```xroms``` tutorial:
> > - Open model output from a url path (e.g., Hafen for the TXLA model) with ```xroms```.
> > - Make plan and section view of model variables with ```cartopy```.
> > - Interpolating model variables (future work)
> > - Calculating derivatives and integrals (future work)
> - Commonly calculated variables, properties, or processes
> > - Rotate $u$ and $v$ velocities from their native grid to east-west and north-south components.
> > - Calculate total kinetic energy dissipation $\epsilon$ from Generic Length Scale turbulence closure schemes following Warner et al. (2005).
> > - Calculate the two-dimensional frontogenesis function of some property $q$ following Hetland and Qu (in prep).
> - More sophisticated analyses
> > - Compute on- and offline volume-integrated temperature budgets using average (offline) and diagnostic (online) files.
> > - Compute relative-divergence histograms to study diurnal convergence at fronts.

## Key publications and descriptions (ordered by time):
Publications that contain major changes to model setup are listed here:
> - **Schlichting, D.**, Qu, L., Kobashi, D., & Hetland, R. (2023). Quantification of physical and numerical mixing in a coastal ocean model using salinity variance budgets. Journal of Advances in Modeling Earth Systems, 15, e2022MS003380. https://doi.org/10.1029/2022MS003380. *Detailed two-way nested model setup, analysis of on- and offline physical/numerical mixing.*
> - Qu, L., Thomas, L. N., Wienkers, A. F., Hetland, R. D., Kobashi, D., Taylor, J. R., et al. (2022). Rapid vertical exchange at fronts in the northern Gulf of Mexico. *Nature Communications*, 13(1), 1–11. https://doi.org/10.1038/s41467-022-33251-7. *Detailed triple-nested setup with Croco.*
> - Kobashi, D., & Hetland, R. (2020). Reproducibility and variability of submesoscale frontal eddies on a broad, low-energy shelf of freshwater influence. *Ocean Dynamics*, 70(11), 1377–1395. Updated skill assessment of model salinity for native parent model. https://doi.org/10.1007/s10236-020-01401-4. *Native parent model. Concluded model is capable of statistically reproducing the eddy characteristics.*
> - Zhang, X., Marta-Almeida, M., & Hetland, R. D. (2012). A high-resolution pre-operational forecast model of circulation on the Texas-Louisiana continental shelf and slope. *Journal of Operational Oceanography*, 5(1), 19–34. https://doi.org/10.1080/1755876X.2012.11020129. *One of the first TXLA model publications where the domain is similar to the modern version. Depracated!*
