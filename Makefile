.PHONY: hello rag_container lora_container hp_rag hp_dialog_dataset hp_llm, hp_lora, hp_lora_llm, interactive

hello:
	echo "Hello from Makefile"

rag_container:
	./containers/create_rag_container.sh

download_cache:
	sbatch src/scripts/download_cache.sh

lora_container:
	./containers/create_lora_container.sh

hp_rag:
	sbatch src/scripts/hp_rag.sh

hp_dialog_dataset:
	sbatch src/scripts/hp_dialog_dataset.sh

hp_llm:
	sbatch src/scripts/hp_llm.sh

hp_lora:
	sbatch src/scripts/hp_lora.sh

hp_lora_llm:
	sbatch src/scripts/hp_lora_llm.sh

interactive:
	srun --nodes=1 --ntasks=1 --cpus-per-task=2 --partition=gpu --gpus=2 --time=03:00:00 --pty bash -i