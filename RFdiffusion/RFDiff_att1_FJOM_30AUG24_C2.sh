#!/bin/bash

# SLURM Directives for Resource Allocation (Common to both parts)
#SBATCH --nodes=1           # number of nodes
#SBATCH --ntasks=1          # number of tasks
#SBATCH --cpus-per-task=10  # 10 CPUs for each job
#SBATCH --gres=gpu:1        # 1 GPU
#SBATCH --mem=64G           # 64G CPU memory
#SBATCH --mail-type=ALL
#SBATCH --mail-user=phr361@ku.dk
#SBATCH --nice
#SBATCH --time=7-00:00:00   # time limit: 7 days
#SBATCH --partition=a100    # specify the partition if submitting on cprome cluster

# Job details
#SBATCH --job-name=RFdiff
#SBATCH --output=slurm-RFdiff-%j.log

set -o errexit # job exit on errors

# Load conda environment for RFdiffusion
ml miniconda3/23.5.2
conda activate /projects/cpr_software/apps/condaenvs/23.5.2/SE3nv

# Define input and working directory
WORKDIR=/projects/cpr_sbmm/people/phr361/PDcomp
INPUT_PDB=${WORKDIR}/CD20/structures/6vja_AB_relaxed.pdb
RFdiff_path=/projects/cpr_software/apps/software-src/RFdiffusion/scripts/run_inference.py
RFdiff_beta_model_path=/projects/cpr_software/apps/software-src/RFdiffusion/models/Complex_beta_ckpt.pt
mkdir -p ${WORKDIR}/RF_diff/
mkdir -p ${WORKDIR}/RF_diff/att1/
mkdir -p ${WORKDIR}/RF_diff/att1/C2

# Part 1: Protein Backbone Generation


RESULTS_DIR=${WORKDIR}/RF_diff/att1/C2/
cd ${RESULTS_DIR}
"${RFdiff_path}" --config-name=symmetry inference.symmetry="C2" 'potentials.guiding_potentials=["type:olig_contacts,weight_intra:1,weight_inter:0.1"]' \
    potentials.olig_intra_all=True potentials.olig_inter_all=True \
    inference.output_prefix="${RESULTS_DIR}" inference.input_pdb="${INPUT_PDB}" \
    'contigmap.contigs=[C140-190/0  80-80]' \
    'ppi.hotspot_res=[C161,C171,C172,C173,C174,C175]' \
    inference.num_designs=50 denoiser.noise_scale_ca=0 denoiser.noise_scale_frame=0 \
    
