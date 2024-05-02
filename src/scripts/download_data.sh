#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=gpu
#SBATCH --time=00:05:00
#SBATCH --output=logs/download_data.out
#SBATCH --error=logs/download_data.err
#SBATCH --job-name="download_data"

srun singularity exec --nv containers/container-rag.sif python src/models/data/DataDownloadUtility.py