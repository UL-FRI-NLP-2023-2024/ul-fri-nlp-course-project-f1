singularity build containers/container-rag.sif docker://pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime
singularity exec containers/container-rag.sif pip install install torch torchvision torchaudio
singularity exec containers/container-rag.sif pip install langchain
singularity exec containers/container-rag.sif pip install langchain-community
singularity exec containers/container-rag.sif pip install transformers
singularity exec containers/container-rag.sif pip install sentencepiece
singularity exec containers/container-rag.sif pip install protobuf
singularity exec containers/container-rag.sif pip install bitsandbytes
singularity exec containers/container-rag.sif pip install accelerate
singularity exec containers/container-rag.sif pip install pypdf
singularity exec containers/container-rag.sif pip install InstructorEmbedding
singularity exec containers/container-rag.sif pip install sentence-transformers
singularity exec containers/container-rag.sif pip install faiss-gpu
singularity exec containers/container-rag.sif pip install rank_bm25
singularity exec containers/container-rag.sif pip install openai