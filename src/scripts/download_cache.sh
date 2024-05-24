#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=gpu
#SBATCH --time=00:05:00
#SBATCH --output=logs/download_cache.out
#SBATCH --error=logs/download_cache.err
#SBATCH --job-name="download_cache"

srun src/models/data/download_cache.sh