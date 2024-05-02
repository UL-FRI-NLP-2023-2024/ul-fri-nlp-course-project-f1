.PHONY: hello rag_container hp_rag

hello:
	echo "Hello from Makefile"

rag_container:
	./containers/create_rag_container.sh

download_data:
	sbatch src/scripts/download_data.sh

hp_rag:
	sbatch src/scripts/hp_rag.sh