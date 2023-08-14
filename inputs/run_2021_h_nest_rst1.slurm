#!/bin/bash
##ENVIRONMENT SETTINGS; CHANGE WITH CAUTION
#SBATCH --get-user-env=L     #Replicate login environment
  
##NECESSARY JOB SPECIFICATIONS
#SBATCH --job-name=txla2_nest_NM_kw_2021_rst1        #Set the job name to "JobExample1"
#SBATCH --time=20-00:00:00             #Set the wall clock limit to 1hr and 30min
#SBATCH --ntasks=120            #number of total CPU cores
#SBATCH --ntasks-per-node=20
#SBATCH --mem=32G                   #memory per node
#SBATCH --partition=xlong
#SBATCH --output=/scratch/user/d.kobashi/projects/hindcasts/projects/txla2/roms_logs/txla2_nest_NM_kw_2021_rst1.%j

module purge
# module load netCDF-Fortran/4.4.4-intel-2016a
#module load netCDF-Fortran/4.4.4-intel-2018b
#module load netCDF-Fortran/4.4.4-gompi-2017b
module load netCDF-Fortran/4.4.4-intel-2018b
# module load netCDF-Fortran/4.5.3-gompi-2020b

WORK_DIR=/scratch/user/d.kobashi/projects/hindcasts/projects/txla2
#MPIDIR=/software/easybuild/software/impi/5.0.3.048-iccifort-2015.3.187-GCC-4.8.4/bin64/mpiexec
cd $WORK_DIR

#mpiexec.hydra mpi_program
NPROCS=120
#OCEAN_IN=${WORK_DIR}/inputs/ocean_in/nest/ocean_txla2_2010_nest_spinup_v2.in
OCEAN_IN=${WORK_DIR}/inputs/ocean_in/nest/ocean_txla2_2021_nest_rst1.in
# OCEAN_IN=${WORK_DIR}/inputs/ocean_in/nest/ocean_txla2_2010_nest_v2_2.in
# OCEAN_IN=/scratch/user/d.kobashi/projects/hindcasts/projects/txla2/inputs/ocean_in/ocean_txla2_2010_nest_spinup.in
# ROMS_EXEC=coawstMv3p5_nest_flt
# ROMS_EXEC=coawstMv3p5_nest
# ROMS_EXEC=coawstM_nest_NM
ROMS_EXEC=coawstM_nest_NM_KanthaC
#ROMS_EXEC=coawstMv3p3
#mpiexec.hydra -f mpd.hosts -np $NPROCS ${WORK_DIR}/coawstM ${OCEAN_IN}
mpirun -np ${NPROCS} ${WORK_DIR}/${ROMS_EXEC} ${OCEAN_IN}
# mpirun ${WORK_DIR}/${ROMS_EXEC} ${OCEAN_IN}

