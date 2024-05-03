# Natural language processing course 2023/24: `Conversations with Characters in Stories for Literacy`

## About

This is **Project 7** of the Natural Language Processing course in year 2023/2024 where we aim to tackle the problem of decreasing literacy skills of younger generations via quick and customized **Persona** bots from novels.

## Team

* Žan Kogovšek
* Žiga Drab
* Vid Cesar

## Repository structure

```
├── containers         <- Singularity containers
│
├── data
│   ├── external       <- Data from third party sources.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── logs               <- Output and Error logs from HPC
│
├── models             <- Trained and serialized models
│
├── notebooks          <- Jupyter notebooks.
│
├── references         <- Conducted tests with our models and existing solutions
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── fig            <- Generated graphics and figures to be used in reporting
│   └── code           <- Code snippets to be used in reporting
│   └── report.tex     <- LaTex source file for the report
│   └── ds_report.cls  <- LaTex document style source file for the report
│   └── report.bib     <- BibLaTex file with references used in the report
│   └── report.pdf     <- Compiled PDF LaTex source file
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment
│
├── src                <- Source code for use in this project.
│   │
│   ├── data           <- Scripts for processing data
│   │
│   ├── models         <- Scripts to train models and then use trained models to make predictions
│   │   │
│   │   ├── data       <- Helper scripts for training our models dealing with data
│   │   │
│   │   ├── utils      <- Helper scripts for training our models dealing with prompts, vector stores, ...
│   │
│   ├── scripts        <- Scripts to train models on HPC
│
│
├── .gitignore         <- Standard .gitignore file
│
├── LICENSE            <- Standard license file
├── Makefile           <- Makefile with model and data related commands
└── README.md          <- The top-level README for developers using this project.
```

## Retrieval Augmented Generation (RAG)

Details of how to use our RAG model.

### Setup

Before running our models we must make sure all the pre-requisites are met.

#### Dataset

For the Retrieval Augmented Generation (RAG) model we need PDFs of all the Harry Potter books and place them under `data/raw`.

The data we used is available to download from Kaggle: https://www.kaggle.com/datasets/icecubical/harry-potter-book-set?resource=download. We uploaded it to a shared Google drive folder for easier download. It can be downloaded using Makefile.

```bash
make download_data
```

The books should be named `harry_potter_book-N.pdf` where N is the number of the book (i.e. harry_potter_book-1.pdf for Harry Potter and the Philosopher's Stone).

#### Singularity Container

The RAG model requires `containers/container-rag.sif` singularity container.

This singularity container can be constructed using the Makefile.

```bash
make rag_container
```
This command will construct a singularity container based on the PyTorch docker container and install all the necessary libraries like langchain, transformers, ...

### Execute

Example of using `HPRag` our Harry Potter RAG model is shown in `src/hp_rag.py`.

#### Initialization

The first step is initializing our RAG model, which is achieved by the following command:
```python
from models.rag import HPRag
hp_rag = HPRag(
    use_ensemble_retriever=True
    verbose=True
)
```

Documentation:

```python
use_ensemble_retriever: bool -> RAG models supports Hybrid Search, which utilized both FAISS (Facebook AI Similarity Search) and BM25 Sparse Embedding Retriever. If this is set to False only FAISS is used.

verbose: bool -> boolean value denoting whether to print debug statements or not
```

Notes:

The first run will take a while around 30 minutes as FAISS and embeddings have to be calculated from scratch. These values get cached and next runs are much faster.

Hybrid Search is slower than FAISS only as BM25 does not supporting caching and therefore the embeddings need to be calculated every time.

#### Querying

Once the RAG is initialized we can start the querying process. Example:
```python
question = "Do you remember what spell Ron mocked Hermione over?"
response = hp_rag.execute_query(question)
print(f"Response: {response}")
```

The response to this specific question from our RAG model is:
```
Response: As Harry Potter, I remember that Ron mocked Hermione over the spell "Wingardium Leviosa". This is the spell that Hermione used to lift Ron's robes while they were playing with Fred and George Weasley's joke spell.
```

We have prepared a script for testing our Harry Potter RAG model in `src/hp_rag.py`.

This script should be executed using the previosly created Singularity Container `containers/container-rag.sif`

Example of running the query script is present in `src/scripts/hp_rag.sh`:
```bash
make hp_rag
```

## RAG + Llama 3 8B Instruct Harry Potter Chatbot

### Setup

RAG is required for this chatbot to function properly so make sure to follow the guide in the previous section - Retrieval Augmented Generation to setup everything properly.

#### Singularity Container

The RAG model requires `containers/container-rag.sif` singularity container, which should already exist by following the `Setup` section in the previous section - Retrieval Augmented Generation.

### Execute

The first step is initializing our LLM, which is achieved by the following command:
```python
from models.llm import HPLLM
hp_llm = HPLLM()
```
To initialize RAG please look at section - Retrieval Augmented Generation.
#### Querying

Once the LLM is initialized we can start the querying process. Example:
```python
question = "Do you remember what spell Ron mocked Hermione over?"
response = hp_llm.query_model(question)
print(f"Response: {response}")
```
This is querying without using the RAG.

Querying with RAG + Llama 3 is displayed below:
```python
    # Question
    question = "Do you remember what spell Ron mocked Hermione over?"
    # Retrieval Augmented Generation
    hp_rag = HPRag(use_ensemble_retriever=True, verbose=True)
    # Get the context
    context = hp_rag.execute_query(question)
    print(f"Context: {context}")
    # Free up memory on GPU (depends on the GPU - might be unnecessary)
    del hp_rag
    # Large Language Model
    hp_llm = HPLLM()
    # Load the model
    hp_llm.prepare_model()
    # Load the tokenizer
    hp_llm.prepare_tokenizer()
    # Get the response
    response = hp_llm.query_model_with_context(question, context)
    print(f"Question: {question}")
    print(f"Response: {response}")
```

We have prepared a script for testing our Harry Potter RAG model in `src/hp_llm.py`.

This script should be executed using the previosly created Singularity Container `containers/container-rag.sif`

Example of running the query script is present in `src/scripts/hp_llm.sh`:
```bash
make hp_llm
```

## LoRA: Low Rank Adaptation

### Setup

Before running our models we must make sure all the pre-requisites are met.

#### Dataset

For fine-tuning we require the Harry Potter dialogue dataset.

The data is already provided in `data/external`, but can also be downloaded from:
- [Train] https://hkustgz-my.sharepoint.com/personal/nchen022_connect_hkust-gz_edu_cn/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fnchen022%5Fconnect%5Fhkust%2Dgz%5Fedu%5Fcn%2FDocuments%2F202307%5FHPD%2Fen%5Ftrain%5Fset%2Ejson&parent=%2Fpersonal%2Fnchen022%5Fconnect%5Fhkust%2Dgz%5Fedu%5Fcn%2FDocuments%2F202307%5FHPD&ga=1
- [Test] https://hkustgz-my.sharepoint.com/personal/nchen022_connect_hkust-gz_edu_cn/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fnchen022%5Fconnect%5Fhkust%2Dgz%5Fedu%5Fcn%2FDocuments%2F202307%5FHPD%2Fen%5Ftest%5Fset%2Ejson&parent=%2Fpersonal%2Fnchen022%5Fconnect%5Fhkust%2Dgz%5Fedu%5Fcn%2FDocuments%2F202307%5FHPD&ga=1

#### Singularity container

The LoRA fine-tuning process requires `containers/container-lora.sif` singularity container.

This singularity container can be constructed using the Makefile.

```bash
make lora_container
```
This command will construct a singularity container based on the PyTorch docker container and install all the necessary libraries like pytorch, transformers, json, ...

### Execute

#### Data preparation
The previously downloaded data is not yet suitable for fine-tuning the large language models.

Utilize the script `src/data/hp_dialog_dataset.py` to prepare data that is suitable for fine-tuning.

This script can be run with the following command:

```bash
make hp_dialog_dataset
```

#### Initialization

The first step is initializing our LoRA trainer, which is achieved by the following command:
```python
from models.lora import HPLora
hp_lora = HPLora(
    fine_tuned_model_directory="lora-tuned-model"
)
```

Documentation:

```python
fine_tuned_model_directory: string -> name of the folder inside `models` folder where the fine-tuned adapter checkpoints are saved. The final adapters are saved in the folder `fine_tuned_model_directory-final`.
```

### Fine-Tuning

Once the LoRA trainer is initialized we can begin the fine-tuning process by calling:

```python
hp_lora.fine_tune_model(verbose=True)
```

We have prepared a script for fine-tuning in `src/hp_lora.py`.

This script should be executed using the previosly created Singularity Container `containers/container-lora.sif`

Example of running the fine-tuning script is present in `src/scripts/hp_lora.sh`:

```bash
make hp_lora
```