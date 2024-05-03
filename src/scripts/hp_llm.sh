#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --partition=gpu
#SBATCH --gpus=1
#SBATCH --time=04:00:00
#SBATCH --output=logs/hp_llm.out
#SBATCH --error=logs/hp_llm.err
#SBATCH --job-name="HP LLM"

srun singularity exec --nv containers/container-rag.sif python src/hp_llm.py