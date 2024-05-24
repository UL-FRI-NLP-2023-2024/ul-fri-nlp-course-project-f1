#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --partition=gpu
#SBATCH --gpus=2
#SBATCH --time=04:00:00
#SBATCH --output=logs/hp_lora_llm.out
#SBATCH --error=logs/hp_lora_llm.err
#SBATCH --job-name="HP LoRA LLM"

srun singularity exec --nv containers/container-lora.sif python src/hp_lora_llm.py