#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=gpu
#SBATCH --gpus=1
#SBATCH --time=00:30:00
#SBATCH --output=logs/hp_dialog_dataset.out
#SBATCH --error=logs/hp_dialog_dataset.err
#SBATCH --job-name="HP DD"

srun singularity exec --nv containers/container-lora.sif python src/data/hp_dialog_dataset.py