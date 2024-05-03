.PHONY: hello rag_container lora_container hp_rag hp_dialog_dataset hp_llm, hp_lora

hello:
	echo "Hello from Makefile"

rag_container:
	./containers/create_rag_container.sh

download_data:
	sbatch src/scripts/download_data.sh

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