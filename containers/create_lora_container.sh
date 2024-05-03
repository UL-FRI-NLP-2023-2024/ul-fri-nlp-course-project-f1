singularity build containers/container-lora.sif docker://pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime
singularity exec containers/container-lora.sif pip install install torch torchvision torchaudio
singularity exec containers/container-lora.sif pip install install json
singularity exec containers/container-lora.sif pip install install transformers
singularity exec containers/container-lora.sif pip install install peft
singularity exec containers/container-lora.sif pip install install datasets
singularity exec containers/container-lora.sif pip install install trl