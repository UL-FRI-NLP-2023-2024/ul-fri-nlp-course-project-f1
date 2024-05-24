# Natural language processing course 2023/24: `Conversations with Characters in Stories for Literacy`

# Table of Contents
1. [About](#about)
2. [Team](#team)
3. [Repository Structure](#repository-structure)
4. [High Performance Computing](#high-performance-computing)
5. [Singularity Containers](#singularity-containers)
6. [How To Run Scripts](#how-to-run-scripts)
7. [Retrieval Augmented Generation (RAG)](#retrieval-augmented-generation-rag)
8. [Harry Potter Question Answering Model](#harry-potter-question-answering-model)
9. [Harry Potter Interactive Chatbot](#harry-potter-interactive-chatbot)
10. [Lukec in njegov škorec Interactive Chatbot](#lukec-in-njegov-škorec-interactive-chatbot)
11. [LoRA LLM Fine-Tuning](#lora-llm-fine-tuning)

## About

This is **Project 7** of the Natural Language Processing course in year 2023/2024 where we aim to tackle the problem of decreasing literacy skills of younger generations via quick and customized **Persona** bots from novels.

## Team

* Žan Kogovšek
* Žiga Drab
* Vid Cesar

## Repository Structure

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
## High Performance Computing

This project was made for high performance computing SLURM systems. We created and tested this project on ARNES cluster and for ease of use we recommend you do the same.

## Singularity Containers

All scripts require a Singularity Container, which has all the dependencies installed for us.

There are 2 different Singularity Containers for this project:
- RAG Container (container-rag.sif): this model is used for running RAGs, LLMs and Interactive Chatbots. Build it with `make rag_container`.
- LoRA Container (container-lora.sif): this model is used for fine-tuning the LLM. Build it with `make lora_container`.


## How To Run Scripts?

There are two ways of running scripts:
- Directly via `make` command (Example: `make hp_rag`). To view all supported commands please continue reading this README or check `Makefile`
- Initialize an interactive session by running `make interactive` and then running an interactive script inside Singularity Container while inside and interactive session(Example: `singularity exec --nv containers/container-rag.sif python src/hp_interactive_chatbot.py`)
- Download cache data which we uploaded to external drive for quicker Peer Reviews by running `make download_cachw`. You can skip this step, but the first run will take noticably longer.

Remember to run Makefile scripts from the root directory.

## Peer Review

This section provides a **step-by-step example** on running the Harry Potter chatbot in interactive mode. **Detailed descriptions, more usages and how to chat with Lukec character are shown in the following sections!**

#### 1. **Download Cached Data**

To save about an hour of setup time, pre-download cached data by running following command in the root directory:

```bash
make download_cache
```

You can check the status of the job with the following command. Usually, it takes about 40 seconds.

```bash
squeue --me
```

#### 2. **Build the Singularity Container**

Build the necessary Singularity container:

```bash
make rag_container
```

#### 3. **Start an Interactive SLURM Session**

Allocate resources and start an interactive session:

```bash
make interactive
```
Wait for the resources to be allocated, and then proceed when you see a prompt like [user@computing-node]$.

#### 4. **Run the Harry Potter Chatbot**

Choose and run one of the interactive chatbot scripts:

* LLM Only Chatbot (Setup time 2 minutes):

```bash
singularity exec --nv containers/container-rag.sif python src/hp_interactive_chatbot.py
```

* RAG Assisted LLM Chatbot (Setup time 6 minutes):

```bash
singularity exec --nv containers/container-rag.sif python src/hp_interactive_rag_chatbot.py
```

#### 5. **Interact with the Chatbot**

After initialization, you'll be prompted to input your questions. Interact as follows:
```bash
Q: <your question here>
A: <model answer here>
```
Continue interacting as desired. Exit by closing the terminal or terminating the SLURM job when finished with:
```bash
exit
```


## Retrieval Augmented Generation (RAG)

Details of how our RAG model works and how to use it.

### Singularity Container

Requires `container-rag.sif`.

### How To Run

We have prepared a script for testing our Harry Potter RAG model in `src/hp_rag.py`.

This is not an interactive example, but only a single question to which the model will provide a single answer.

Make sure to set the question to the one you want to pose.

The response will be the context surrounding the question.

Run the script with:
```bash
make hp_rag
```

Output will be in logs/hp_rag.out

### Implementation Details

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

## Harry Potter Question Answering Model

Details of how our Question Answering Harry Potter Model combining RAG + Llama 3 8B Instruct works and how to use it.

### Singularity Container

Requires `container-rag.sif`.

### How To Run

We have prepared a script for testing our Harry Potter Question Answering Model in `src/hp_llm.py`.

This is not an interactive example, but only a single question to which the model will provide a single answer.

Make sure to set the question to the one you want to pose.

The model will first pose the question to the RAG model to obtain the context.

The question and the obtained context from the RAG will then be given to the LLM (Llama 3 8B Instruct).

The response will be the answer to the question as the character Harry Potter.

Run the script with:
```bash
make hp_llm
```

Output will be in logs/hp_llm.out

### Implementation Detials

The first step is initializing our LLM, which is achieved by the following command:
```python
from models.llm import HPLLM
hp_llm = HPLLM()
```
To initialize RAG please look at section - Retrieval Augmented Generation (RAG).

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

## Harry Potter Interactive Chatbot

### Singularity Container

Requires `container-rag.sif`.

### How To Run

First create an interactive SLURM job. This can be achieved by running:
```bash
make interactive
```

Wait for the resources to be allocated (computing-node is something like wn220 or any other node):
```bash
srun: job 10256812 queued and waiting for resources
srun: job 10256812 has been allocated resources
[user@computing-node]$
```

Now you can start the interactive chatbot script. You have two choices:
- LLM only interactive chatbot. This means you will only be chatting with the Llama 3 LLM with no extra context being provided.
    ```bash
    [user@computing-node]$ singularity exec --nv containers/container-rag.sif python src/hp_interactive_chatbot.py
    ```
- RAG assisted LLM interactive chatbot. This means your question will first be presented to the RAG and then passed onto the LLM along with the context from the RAG.
    ```bash
    [user@computing-node]$ singularity exec --nv containers/container-rag.sif python src/hp_interactive_rag_chatbot.py
    ```

The LLM and the RAG (depends on the version) will first be initialized after which point you will be presented with the input to start interacting with the chatbot.

```bash
[RAG] Initialzing...
.
.
.
[LLM] Finished initialization!
Q: <your question here>
A:

<model answer here>
Q: <your next question here>

A:

<model next answer here>
.
.
.
```

## Lukec in njegov škorec Interactive Chatbot

### Singularity Container

Requires `container-rag.sif`.

### How To Run

First create an interactive SLURM job. This can be achieved by running:
```bash
make interactive
```

Wait for the resources to be allocated (computing-node is something like wn220 or any other node):
```bash
srun: job 10256812 queued and waiting for resources
srun: job 10256812 has been allocated resources
[user@computing-node]$
```

Now you can start the interactive chatbot script. You have two choices:
- LLM only interactive chatbot. This means you will only be chatting with the Llama 3 LLM with no extra context being provided.
    ```bash
    [user@computing-node]$ singularity exec --nv containers/container-rag.sif python src/lukec_interactive_chatbot.py
    ```
- RAG assisted LLM interactive chatbot. This means your question will first be presented to the RAG and then passed onto the LLM along with the context from the RAG.
    ```bash
    [user@computing-node]$ singularity exec --nv containers/container-rag.sif python src/lukec_interactive_rag_chatbot.py
    ```

The LLM and the RAG (depends on the version) will first be initialized after which point you will be presented with the input to start interacting with the chatbot.

```bash
[RAG] Initialzing...
.
.
.
[LLM] Finished initialization!
Q: <your question here>
A:

<model answer here>
Q: <your next question here>

A:

<model next answer here>
.
.
.
```

## LoRA LLM Fine-Tuning

### Singularity Container

Requires `container-lora.sif`.

### Dataset

For fine-tuning we require the Harry Potter dialogue dataset.

The data is already provided in `data/external`, but can also be downloaded from:
- [Train] https://hkustgz-my.sharepoint.com/personal/nchen022_connect_hkust-gz_edu_cn/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fnchen022%5Fconnect%5Fhkust%2Dgz%5Fedu%5Fcn%2FDocuments%2F202307%5FHPD%2Fen%5Ftrain%5Fset%2Ejson&parent=%2Fpersonal%2Fnchen022%5Fconnect%5Fhkust%2Dgz%5Fedu%5Fcn%2FDocuments%2F202307%5FHPD&ga=1
- [Test] https://hkustgz-my.sharepoint.com/personal/nchen022_connect_hkust-gz_edu_cn/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fnchen022%5Fconnect%5Fhkust%2Dgz%5Fedu%5Fcn%2FDocuments%2F202307%5FHPD%2Fen%5Ftest%5Fset%2Ejson&parent=%2Fpersonal%2Fnchen022%5Fconnect%5Fhkust%2Dgz%5Fedu%5Fcn%2FDocuments%2F202307%5FHPD&ga=1

### How To Run

#### Data preparation

The previously downloaded data is not yet suitable for fine-tuning the large language models.

Utilize the script `src/data/hp_dialog_dataset.py` to prepare data that is suitable for fine-tuning.

This script can be run with the following command:
```bash
make hp_dialog_dataset
```

#### Fine-Tuning

We have prepared a script for fine-tuning in `src/hp_lora.py`.

This script can be run with the following command:
```bash
make hp_lora
```

#### Fine-Tuned LLM

We have prepared a script for running the fine-tuned LLM in `src/hp_lora_llm.py`.

This script can be run with the following command:
```bash
make hp_lora_llm
```

### Implementation Details

The first step is initializing our LoRA trainer, which is achieved by the following command:
```python
from models.lora import HPLora
hp_lora = HPLora(
    fine_tuned_model_directory="peft"
)
```

Documentation:

```python
fine_tuned_model_directory: string -> name of the folder inside `models` folder where the fine-tuned adapter checkpoints are saved. The final adapters are saved in the folder `peft-final`.
```

Once the LoRA trainer is initialized we can begin the fine-tuning process by calling:

```python
hp_lora.fine_tune_model(verbose=True)
```

After the training is complete we can initialize the LoRA fine-tuned LLM, which is achieved by the following code:
```python
hp_lora_llm = HPLoraLLM(peft_path="models/peft-final")
```

We then load the models with:
```python
hp_lora_llm.load_model(original_device="cuda:0", peft_device="cuda:1")
```

And finally we can query the model with:
```python
response = hp_lora_llm.query_model(question)
```

Documentation:
```python
peft_path: string -> name of the folder inside `models` where the final fine-tuned adapters are saved.
original_device: string -> device map for where to load the original model
peft_device: string -> device map for where to lead the fine-tuned model
```