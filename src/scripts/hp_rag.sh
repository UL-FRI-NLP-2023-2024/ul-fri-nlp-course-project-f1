#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=gpu
#SBATCH --gpus=1
#SBATCH --time=02:00:00
#SBATCH --output=logs/hp_rag.out
#SBATCH --error=logs/hp_rag.err
#SBATCH --job-name="HP RAG"

srun singularity exec --nv containers/container-rag.sif python src/hp_rag.py