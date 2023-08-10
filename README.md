# txla_model
## Code repository for the Texas-Louisiana shelf hydrodynamic ROMS model.

## First steps: Create a conda environment if working in Python
If you work in Python, we recommend creating a custom conda environment. I've included a minimal environment used for the examples in
  * txla_model_req.txt (updated Aug. 2023)
## Model inputs (future work):
> - grid generation
> - forcing generation
> - .in files
> - hprc scripts/resources
> - nested setup
## Post-processing and analysis examples:
> - open_output.ipynb: Open model output(s) on Hafen with xROMS.
> - make_plots.ipynb: Plot surface variables and cross sections with Cartopy.
> - rotate_velocities.ipynb: Rotate u and v velocities from their native grid to east-west and north-south components.
> - calc_dissipation.ipynb: Calculate total kinetic energy dissipation from Generic Length Scale turbulence closure schemes.
> - offline_temp_budget_valid.ipynb: Assesses accuracy of offline, volume-integrated temperature budget using average (offline) and diagnostic (online) files
> - diurnal_convergence.ipynb: Remakes relative vorticity-divergence Hovmoller diagrams for 2022 output. Remakes a subplot from Qu et al. (2022)
> - frontogenesis_function_2d.ipynb: Computes the two-dimensional frontogenesis function of some property q and makes a basic surface plot.
## Key publications and descriptions (ordered by time):
> -  **Schlichting, D.**, Qu, L., Kobashi, D., & Hetland, R. (2023). Quantification of physical and numerical mixing in a coastal ocean model using salinity variance budgets. Journal of Advances in Modeling Earth Systems, 15, e2022MS003380.https://doi.org/10.1029/2022MS003380. *Detailed nested model setup, analysis of on- and offline physical/numerical mixing.*
> - Qu, L., Thomas, L. N., Wienkers, A. F., Hetland, R. D., Kobashi, D., Taylor, J. R., et al. (2022). Rapid vertical exchange at fronts in the northern Gulf of Mexico. *Nature Communications*, 13(1), 1–11. https://doi.org/10.1038/s41467-022-33251-7. *Details triple-nested setup with Croco.*
> - Kobashi, D., & Hetland, R. (2020). Reproducibility and variability of submesoscale frontal eddies on a broad, low-energy shelf of freshwater influence. *Ocean Dynamics*, 70(11), 1377–1395. Updated skill assessment of model salinity for native parent model. https://doi.org/10.1007/s10236-020-01401-4. *Also concludes model is capable of statistically reproducing the eddy characteristics.*
> - Zhang, X., Marta-Almeida, M., & Hetland, R. D. (2012). A high-resolution pre-operational forecast model of circulation on the Texas-Louisiana continental shelf and slope. *Journal of Operational Oceanography*, 5(1), 19–34. https://doi.org/10.1080/1755876X.2012.11020129. *One of the first TXLA model publications where the domain is similar to the modern version. Depracated.*
