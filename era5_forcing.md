## Documentation for the generation of ROMS forcing file with ERA5

### ERA5-ROMS & Tips
GitHub repo used to download ERA5 data and pre-process for ROMS. This is not perfect and I made an additional post-processing script to modify the output. See https://github.com/dylanschlichting/ERA5-ROMS. In that repo, see ```save_forcing_new.py``` for relevant modifications. 

### Description of TXLA model specifics
We are using the ```BULK_FLUXES``` parameterization. From our activated list of CPP options in ```txla.h```, the relevant ones for atmospheric forcing are:

```
 Activated C-preprocessing Options:

 TXLA                     TXLA
 BULK_FLUXES              Surface bulk fluxes parameterization
 EMINUSP                  Compute Salt Flux using E-P
 LONGWAVE_OUT             Compute outgoing longwave radiation internally
 SOLAR_SOURCE             Solar Radiation Source Term
 VISC_GRID                Horizontal viscosity coefficient scaled by grid size
 WTYPE_GRID               Spatially varying Jerlov water type index
 ```
 Since we are providing the downwelling component of the longwave flux, we need to provide the following options:
 ```
Surface U-wind component [wind].
Surface V-wind component [wind].
Surface air temperature [celcius].
Surface air pressure [millibar].
Surface air relative humidity [or specific humidity in g/kg].
Rain fall rate [[kg m2/s].
Shortwave radiation flux [w/m^2].
```

When we generate the forcing file, we have to make sure the attributes match what ROMS expects from ```ROMS/External/varinfo.dat```. Below contains all relevant variables:
```
!------------------------------------------------------------------------------
!  Atmospheric forcing variables.
!------------------------------------------------------------------------------
!

'Pair'                                             ! Input
  'surface air pressure'
  'millibar'                                       ! [millibar]
  'Pair, scalar, series'
  'pair_time'
  'idPair'
  'r2dvar'
  1.0d0

'Tair'                                             ! Input
  'surface air temperature'
  'Celsius'                                        ! [Kelvin]
  'Tair, scalar, series'
  'tair_time'
  'idTair'
  'r2dvar'
  1.0d0

'Qair'                                             ! Input
  'surface air relative humidity'                  !  relative    or  specific
  'percentage'                                     ! [percentage  or  g/kg    ]
  'Qair, scalar, series'
  'qair_time'
  'idQair'
  'r2dvar'                                         ! relative        specific
  0.01d0                                           ! 1/100      or   1.0

'cloud'                                            ! Input
  'cloud fraction'
  'nondimensional'                                 ! [nondimensional]
  'cloud, scalar, series'
  'cloud_time'
  'idCfra'
  'r2dvar'
  1.0d0

'swrad'                                            ! Input/Output
  'solar shortwave radiation flux'
  'watt meter-2'                                   ! Input:  [Watt/m2]
  'shortwave radiation, scalar, series'            ! [Celsius m/s]
  'srf_time'                                       ! Output: [Watt/m2]
  'idSrad'
  'r2dvar'
  1.0d0

'lwrad_down'                                       ! Input
  'downwelling longwave radiation flux'
  'watt meter-2'                                   ! Input:  [Watt/m2]
  'downwelling longwave radiation, scalar, series' ! [Celsius m/s]
  'lrf_time'
  'idLdwn'
  'r2dvar'
  1.0d0

'lwrad'                                            ! Input/Output
  'net longwave radiation flux'
  'watt meter-2'                                   ! Input:  [Watt/m2]
  'longwave radiation, scalar, series'             ! [Celsius m/s]
  'lrf_time'                                       ! Output: [Watt/m2]
  'idLrad'
  'r2dvar'
  1.0d0

'rain'                                             ! Input
  'rain fall rate'
  'kilogram meter-2 second-1'                      ! [kg m2/s]
  'rain, scalar, series'
  'rain_time'
  'idrain'
  'r2dvar'
  1.0d0                                            ! 1/rhow (0.001 m3/kg) if m/s

'snow'                                             ! Input
  'snow fall rate'
  'kilogram meter-2 second-1'                      ! [kg m2/s]
  'snow, scalar, series'
  'snow_time'
  'idsnow'
  'r2dvar'
  1.0d0                                            ! 1/rhow (0.001 m3/kg) if m/s

'evaporation'                                      ! Input
  'evaporation rate'
  'kilogram meter-2 second-1'                      ! [kg m2/s]
  'evaporation, scalar, series'
  'evap_time'
  'idevap'
  'r2dvar'
  1.0d0                                            ! 1/rhow (0.001 m3/kg) if m/s

'Uwind'                                            ! Input
  'surface u-wind component'
  'meter second-1'                                 ! [m/s]
  'u-wind, scalar, series'
  'wind_time'
  'idUair'
  'r2dvar'
  1.0d0

'Vwind'                                            ! Input
  'surface v-wind component'
  'meter second-1'                                 ! [m/s]
  'v-wind, scalar, series'
  'wind_time'
  'idVair'
  'r2dvar'
  1.0d0
```
In previous versions of the TXLA model, ```Qair``` was provided via relative humidity and the longwave radiation was computed internally. We make two changes because they are more physically realistic. First, ```Qair``` is given as specific humidity. This is coded unelegantly into the source code in ```ROMS/Nonlinear/bulk_flux.F```: 
```
!  Compute specific humidity, Q (kg/kg).
!
          IF (RH.lt.2.0_r8) THEN                       !RH fraction
            cff=cff*RH                                 !Vapor pres (mb)
            Q(i)=0.62197_r8*                                            &
     &           (cff/(PairM-0.378_r8*cff+eps))        !Spec hum (kg/kg)
          ELSE          !RH input was actually specific humidity in g/kg
            Q(i)=RH/1000.0_r8                          !Spec Hum (kg/kg)
          END IF
```
ERA5 provides specific humidity in kg/kg already, so we have to purposely change the units just so it can be reconverted. There really should be an option to have the user input specific humidity, but our goal is not to fix the code. In ```varinfo.dat```: we change the following and make sure we multiply Qair by 1000 in the actual forcing file:
```
'Qair'                                             ! Input
  'surface air specific humidity'                  !  relative    or  specific
  'g/kg'                                           ! [percentage  or  g/kg    ]
  'Qair, scalar, series'
  'qair_time'
  'idQair'
  'r2dvar'                                         ! relative        specific
  1.0d0                                            ! 1/100      or   1.0
```
The second change is to provide the downwelling component of the longwave radiation and have ROMS compute the the outgoing component based on the model SST. While we don't test the differences, this should be more physically realistic since only outward component is paramaterized. If we used ```LONGWAVE```, we would need to provide the cloud fraction to the model too:
```
# if defined LONGWAVE
!
!  Use Berliand (1952) formula to calculate net longwave radiation.
!  The equation for saturation vapor pressure is from Gill (Atmosphere-
!  Ocean Dynamics, pp 606). Here the coefficient in the cloud term
!  is assumed constant, but it is a function of latitude varying from
!  1.0 at poles to 0.5 at the Equator).
!
          cff=(0.7859_r8+0.03477_r8*TairC(i))/                          &
     &        (1.0_r8+0.00412_r8*TairC(i))
          e_sat=10.0_r8**cff   ! saturation vapor pressure (hPa or mbar)
          vap_p=e_sat*RH       ! water vapor pressure (hPa or mbar)
          cff2=TairK(i)*TairK(i)*TairK(i)
          cff1=cff2*TairK(i)
          LRad(i,j)=-emmiss*StefBo*                                     &
     &              (cff1*(0.39_r8-0.05_r8*SQRT(vap_p))*                &
     &                    (1.0_r8-0.6823_r8*cloud(i,j)*cloud(i,j))+     &
     &               cff2*4.0_r8*(TseaK(i)-TairK(i)))
```
Thankfully, this is not required for ```LONGWAVE_OUT```, as shown below. In adition, there does not appear to be a correction to specific humidity in ```LONGWAVE```? If this is correct, inputting specific humidity would result in a major source of error for longwave. 
```
# elif defined LONGWAVE_OUT
!
!  Treat input longwave data as downwelling radiation only and add
!  outgoing IR from model sea surface temperature.
!
          LRad(i,j)=lrflx(i,j)*Hscale-                                  &
     &              emmiss*StefBo*TseaK(i)*TseaK(i)*TseaK(i)*TseaK(i)

# else
```
The third change, which is done for convenience, is that we allow ROMS to interpolate the atmoshperic forcing to the TXLA grid internally. In previous versions of the model, the forcing was interpolated before runtime, but I was unable to find example code. Didn't want to introduce another potential error source and the ROMS interpolation has been used by many researchers. 

### Background on heat fluxes
A local heat budget can be written as: $Q_{net}=Q_{sw}+Q_{lw}+Q_{sen}+Q_{lat}$
where 
> - $Q_{sw}=$ shortwave  [w/m^2]
> - $Q_{lw}=$ longwave  [w/m^2]
> - $Q_{sen}=$ sensible [w/m^2]
> - $Q_{lat}=$ latent [w/m^2]


> - Shortwave: Portion of the EM spectrum with wavelengths shorter than visible light, up to UV and includes some IR. It penetrates into the water column and can be affected by turbidity.
> - Longwave: Earth absorbs SW, then re-emits energy in the form of LW. This should be based on the model SST and is more physically consistent than having the model calculate the net longwave from cloudiness, humidity, etc. 
> - Sensible: Conductive flux from the surface to the atmosphere. 
> - Latent: Energy transfer from the atmosphere/ocean due to phase changes, i.e., precipitation and evaporation. 
