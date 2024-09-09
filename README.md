```txla_model``` is a metarepository for the Texas-Louisiana shelf hydrodynamic ROMS model configured as part of COAWST (Warner et al., 2010 *O.M.*). The information required to run the model can be found here. Most input generation and output postprocessing/analysis is done in Python. Output analysis is based on ```xroms```. To run the notebooks in this repository, an environment can be installed by running

        conda install --file txla_model_req.txt

### Run history
> - Seahorce (2024 onwards): COAWST v3.8 by Dylan Schlichting. 
> > - Hindcast model run with ERA5 re-analysis, USGS streamflow, GoM HYCOM. Used for MPAS-O comparison. 
> - SUNRISE (2020-2023): COAWST v3.7 by Daijiro Kobashi. 
> > - Nested model with numerical salinity mixing work. Mix of ERA-Interim / ERA5 reanalysis, USGS streamflow, Global HYCOM. 
> - Forecaset model (indefinite, still active as of 2024): COAWST v.3.5 by Yun Liu. 
> > - Different river & atmospheric forcing & BBL model. 
## Running the model:
Example files will be provided or linked to run the model (if file size is an issue) as listed below. One example is given for the native parent and one for the nested iteration. Slurm job scripts for running on an HPRC cluster are also provided.
> - grid generation (future work)
> - forcing generation (future work)
> - .in files (see inputs)
> - hprc job scripts with slurm (see inputs)
> - nested setup (see inputs)
## Working with model output
> - A condensed ```xroms``` tutorial:
> > - Open model output from a url path (e.g., Hafen for the TXLA model) with ```xroms```.
> > - Make plan and section view of model variables with ```cartopy```.
> > - Calculating derivatives and integrals of model variables.
> > > - Surface derivatives can be calculated with a ```grid.derivative()```
> > > - Depth dependent derivatives should be calculated with a Jacobian to account for the time-dependent sea surface height oscillations. Use ```xroms.hgrad()``` for this.
> > - Interpolating model variables.
> - An extensive ```xhistogram``` tutorial with various applications (future work):
> > - Salinity coordinates, total exchange flow (MacCready, 2011 *J.P.O.*), and mixing. TEF is a transported weighted histogram of salinity.
> > - Two-dimensional weighted histograms
> > - How to construct PDFs and CDFs offline discreetly from a histogram
> - Commonly calculated variables, properties, or processes:
> > - Rotate $u$ and $v$ velocities from their native grid to east-west and north-south components.
> > - Calculate normalized quantities from the velocity gradient tensor:
> > > - Relative vorticity $`\zeta/f = (\partial_x v - \partial_y u)/f`$.
> > > - Divergence $`(\partial_x u + \partial_y v)/f`$.
> > > - Total strain rate $`\sqrt{(\partial_x u - \partial_y v)^2+(\partial_x v + \partial_y u)^2}/f`$.
> > - Calculate total kinetic energy dissipation $\epsilon$ from Generic Length Scale turbulence closure schemes following Warner et al. (2005).
> > - Calculate the two-dimensional frontogenesis function of some property $q$ following Hetland and Qu (in prep).
> > > - Code to compute histograms of the 2D normalized frontogenesis function may be found under ```/output_scripts/```
> - More sophisticated analyses
> > - Compute on- and offline volume-integrated temperature budgets using average (offline) and diagnostic (online) files.
> > - Compute volume-integrated salinity variance budgets (arhived in a separate repository; https://github.com/dylanschlichting/numerical_mixing.)
> > - Compute relative-divergence histograms to study diurnal convergence at fronts.
## Key publications:
Publications that contain major changes to model setup are listed here:
> - **Schlichting, D.**, Qu, L., Kobashi, D., & Hetland, R. (2023). Quantification of physical and numerical mixing in a coastal ocean model using salinity variance budgets. Journal of Advances in Modeling Earth Systems, 15, e2022MS003380. https://doi.org/10.1029/2022MS003380. *Detailed two-way nested model setup, analysis of on- and offline physical/numerical mixing.*
> - Qu, L., Thomas, L. N., Wienkers, A. F., Hetland, R. D., Kobashi, D., Taylor, J. R., et al. (2022). Rapid vertical exchange at fronts in the northern Gulf of Mexico. *Nature Communications*, 13(1), 1–11. https://doi.org/10.1038/s41467-022-33251-7. *Detailed triple-nested setup with Croco.*
> - Kobashi, D., & Hetland, R. (2020). Reproducibility and variability of submesoscale frontal eddies on a broad, low-energy shelf of freshwater influence. *Ocean Dynamics*, 70(11), 1377–1395. Updated skill assessment of model salinity for native parent model. https://doi.org/10.1007/s10236-020-01401-4. *Native parent model. Concluded model is capable of statistically reproducing submesoscale eddy characteristics.*
> - Zhang, X., Marta-Almeida, M., & Hetland, R. D. (2012). A high-resolution pre-operational forecast model of circulation on the Texas-Louisiana continental shelf and slope. *Journal of Operational Oceanography*, 5(1), 19–34. https://doi.org/10.1080/1755876X.2012.11020129. *One of the first TXLA model publications where the domain is similar to the modern version. Depracated!*
## Model documentation
The most comprehensive description of the (nested) model setup is currently found in *Schlichting et al. (2023)*. A draft of an in-depth description authored by Daijiro Kobashi of the nested model setup is attached in ROMS_nested_app.pdf. Key points of the model setup are documented for reference:
> - Standard output frequency: 1 hour
> - 2 year spinup for the shelf if starting from a fresh initial condition file. 
> - 670 x 189 x 30 grid points for native (non-nested) parent
> > - 677 X 602 X 30 for 2010 nested simulation, 402 X 377 X 30 for the 2021 nested simulation, and 452 X 552 X 30 for the 2022 nested simulation. Note indices may be off by one or two grid points.
> - ```Vtransform=2,Vstretching=4```, ```\theta_s = 5.0, \theta_b = 0.4```
> - Online timestep ```dt= 75-80 s```, nesting is 5X finer due to the CFL criteria. At least for 2010, 2021, and 2022 simulations.
> - ```MPDATA``` for momentum and tracer advection
> - Vertical mixing schemes: $\kappa-\omega$ for 2010 simulations. $\kappa-\epsilon$ for 2021 ver 1.0 and 2022.
> > - This can be confirmed with variables ```m```, ```n```, and ```p```. See Warner et al. (2005) *O.M.*.
> - Lateral mixing schemes: Laplacian constant diffusivity (1.0 m$`^2`$ s$`^{-1}`$) and viscosity (5.0 m$`^2`$ s$`^{-1}`$) that are scaled to the grid size.
> > - Momentum rotated along s surfaces, diffusivity along geopotential surfaces
> > - For 2010 nested simulations, these values are scaled incorrectly! They should be rescaled to account for the smaller area in the child model, but are left the same as the parent values. See *Schlichting et al. (2023)* Section 3 and the response to reviewers for more information.
