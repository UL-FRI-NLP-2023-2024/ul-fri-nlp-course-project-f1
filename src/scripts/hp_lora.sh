#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G
#SBATCH --partition=gpu
#SBATCH --gpus=1
#SBATCH --time=04:00:00
#SBATCH --output=logs/hp_lora.out
#SBATCH --error=logs/hp_lora.err
#SBATCH --job-name="HP LORA"

srun singularity exec --nv containers/container-lora.sif python src/hp_lora.py