# txla_model
```txla_model``` is a metarepository for the Texas-Louisiana shelf hydrodynamic ROMS model configured as part of COAWST (Warner et al., 2010 *O.M.*). The information required to run the model can be found here. The bulk of the input generation and output postprocessing/analysis is done in Python. Output analysis is based on modern packages such as ```xroms```, which is built on ```xarray``` and ```xgcm```. It contains a panolpy of useful tools for working with ROMS output. Runs conducted for SUNRISE by Daijiro Kobashi during 2021 - Aug. 2023 are configured with COAWST ver. 3.7.  This includes the 2010, 2021, and 2022 simulations disucssed in this repository, although future runs will be on ver 3.8.
## First steps: Create a conda environment
If you work in Python, we recommend creating a custom conda environment so package version control can be managed easily. To run the notebooks in this repository, an environment can be installed by running 

        conda install --file txla_model_req.txt
    
## Running the model (work in progress):
Example files will be provided or linked to run the model (if file size is an issue) as listed below. One example is given for the native parent and one for the nested iteration. Slurm job scripts for running on an HPRC cluster are also provided.
> - grid generation (future work)
> - forcing generation (future work)
> - .in files (see inputs)
> - hprc job scripts with slurm (see inputs)
> - nested setup (see inputs)
## Working with model output (work in progress):
```txla_model``` has many tools for dealing with model output, including:
> - A condensed ```xroms``` tutorial:
> > - Open model output from a url path (e.g., Hafen for the TXLA model) with ```xroms```.
> > - Make plan and section view of model variables with ```cartopy```.
> > - Interpolating model variables (future work)
> > - Calculating derivatives and integrals of model variables (future work)
> - Commonly calculated variables, properties, or processes
> > - Rotate $u$ and $v$ velocities from their native grid to east-west and north-south components.
> > - Calculate quantities from the velocity gradient tensor (relative vorticity, divergence, strain; future work)
> > - Calculate total kinetic energy dissipation $\epsilon$ from Generic Length Scale turbulence closure schemes following Warner et al. (2005).
> > - Calculate the two-dimensional frontogenesis function of some property $q$ following Hetland and Qu (in prep).
> - More sophisticated analyses
> > - Compute on- and offline volume-integrated temperature budgets using average (offline) and diagnostic (online) files.
> > - Compute volume-integrated salinity variance budgets (future work; see https://github.com/dylanschlichting/numerical_mixing for more information.)
> > - Compute relative-divergence histograms to study diurnal convergence at fronts.
## Key publications and descriptions (ordered by time):
Publications that contain major changes to model setup are listed here:
> - **Schlichting, D.**, Qu, L., Kobashi, D., & Hetland, R. (2023). Quantification of physical and numerical mixing in a coastal ocean model using salinity variance budgets. Journal of Advances in Modeling Earth Systems, 15, e2022MS003380. https://doi.org/10.1029/2022MS003380. *Detailed two-way nested model setup, analysis of on- and offline physical/numerical mixing.*
> - Qu, L., Thomas, L. N., Wienkers, A. F., Hetland, R. D., Kobashi, D., Taylor, J. R., et al. (2022). Rapid vertical exchange at fronts in the northern Gulf of Mexico. *Nature Communications*, 13(1), 1–11. https://doi.org/10.1038/s41467-022-33251-7. *Detailed triple-nested setup with Croco.*
> - Kobashi, D., & Hetland, R. (2020). Reproducibility and variability of submesoscale frontal eddies on a broad, low-energy shelf of freshwater influence. *Ocean Dynamics*, 70(11), 1377–1395. Updated skill assessment of model salinity for native parent model. https://doi.org/10.1007/s10236-020-01401-4. *Native parent model. Concluded model is capable of statistically reproducing submesoscale eddy characteristics.*
> - Zhang, X., Marta-Almeida, M., & Hetland, R. D. (2012). A high-resolution pre-operational forecast model of circulation on the Texas-Louisiana continental shelf and slope. *Journal of Operational Oceanography*, 5(1), 19–34. https://doi.org/10.1080/1755876X.2012.11020129. *One of the first TXLA model publications where the domain is similar to the modern version. Depracated!*
## Model documentation
The most comprehensive description of the (nested) model setup is currently found in *Schlichting et al. (2023)*. A draft of an in-depth description authored by Daijiro Kobashi of the nested model setup is attached in ROMS_nested_app.pdf. Key points of the model setup are documented for reference:
> - Standard output frequency: 1 hour
> - 670 x 189 x 30 grid points for native (non-nested) parent
> > - 677 X 602 X 30 for 2010 nested simulation, 402 X 377 X 30 for the 2021 nested simulation, and 452 X 552 X 30 for the 2022 nested simulation. Note indices may be off by one or two grid points. 
> - ```Vtransform=2,Vstretching=4```, ```\theta_s = 5.0, \theta_b = 0.4```
> - Online timestep ```dt= 75-80 s```, nesting is 5X finer due to the CFL criteria. At least for 2010, 2021, and 2022 simulations.
> - MPDATA for momentum and tracer advection
> - ERA interim reanalysis for 2010 atmospheric forcing, ERA5 reanalysis for 2021/2022 simulations.
> - River forcing: USGS streamflow data for 2010 simulations, national water model for future runs (work in progress, add to docs). 
> - Vertical mixing (turbulence closure) schemes: $\kappa-\omega$ for 2010 simulations. $\kappa-\epsilon$ for 2021 ver 1.0 and 2022.
> - Lateral mixing schemes: Laplacian diffusivity and viscosity that are scaled to the grid size. Mixing along geopotential surfaces, i.e., completely horizontal in our model.
> > - For 2010 nested simulations, these values are scaled incorrectly! They should be rescaled to account for the smaller area in the child model, but are left the same as the parent values. See *Schlichting et al. (2023)* Section 3 and the response to reviewers for more information.
