#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=gpu
#SBATCH --gpus=1
#SBATCH --time=00:30:00
#SBATCH --output=logs/gpt_neo.out
#SBATCH --error=logs/gpt_neo.err
#SBATCH --job-name="GPTNeoXClient"

srun singularity exec --nv containers/container-rag.sif python src/models/GPTNeoClient.py