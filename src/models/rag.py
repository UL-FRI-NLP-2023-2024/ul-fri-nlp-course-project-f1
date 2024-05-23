from models.data.DataParser import DataParser, LukecDataParser
from models.data.TextSplitter import TextSplitter
from models.utils.VectorStore import VectorStore, LukecVectorStore
from models.utils.SparseEmbedding import SparseEmbedding
from models.utils.ModelVersion import MISTRAL_LITE, MISTRAL_ORCA, FAISS_PATH, LUKEC_FAISS_PATH
from models.utils.PromptBuilder import PromptBuilder

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
import langchain
from langchain_core.prompts import PromptTemplate
from langchain_community.cache import InMemoryCache
from langchain_core.callbacks.stdout import StdOutCallbackHandler
from langchain.chains.retrieval_qa.base import RetrievalQA
from transformers.utils import logging
from langchain.memory import ConversationBufferMemory

import os


class HPRag:
    def __init__(self, use_ensemble_retriever=True, verbose=False, device="cuda"):
        logging.get_logger("transformers").setLevel(logging.ERROR)
        self.use_ensemble_retriever = use_ensemble_retriever
        self.read_documents = use_ensemble_retriever
        self.verbose = verbose
        if not os.path.exists(FAISS_PATH):
            # Must construct FAISS using existing documents
            self.read_documents = True
        if self.read_documents:
            self.start_directory_loader()
        self.start_vector_store()
        if self.read_documents:
            self.start_sparse_embedder()
        self.start_llm(device)
        self.construct_custom_prompt()
        self.start_qa_chain(verbose)

    def start_directory_loader(self):
        # Directory Loader
        directory_loader = DataParser(directory="data/raw/")
        directory_loader.read_documents(self.verbose)
        self.hp_docs = directory_loader.get_documents(self.verbose)
        # Text Splitter
        text_splitter = TextSplitter(chunk_size=1000, chunk_overlap=200)
        text_splitter.init_splitter()
        self.split_hp_docs = text_splitter.split_documents(self.hp_docs, self.verbose)

    def start_vector_store(self):
        # Vector Store
        self.vs = VectorStore()
        self.vs.load_embeddings_model(self.verbose)
        self.vs.create_vector_store(self.split_hp_docs, self.verbose)
        self.faiss_retriever = self.vs.get_faiss_retriever(k=5)

    def start_sparse_embedder(self):
        # Sparse embedder
        self.se = SparseEmbedding(self.split_hp_docs, self.verbose)
        self.se.set_k(k=5)
        self.ensemble_retriever = self.se.get_ensemble_retriever(faiss_retriever=self.faiss_retriever)

    def start_llm(self, device):
        # LLM Model
        self.model_version = MISTRAL_ORCA
        self.model = AutoModelForCausalLM.from_pretrained(self.model_version, device_map=device)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_version, padding_side="left")
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        self.tokenizer.padding_side = "left"
        # Pipeline
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.1,
            top_p=0.95,
            top_k=40,
            repetition_penalty=1.1,
            return_full_text=False,
        )
        # LLM
        self.llm = HuggingFacePipeline(pipeline=self.pipe)
        # Caching
        langchain.llm_cache = InMemoryCache()

    def construct_custom_prompt(self):
        # Prompt
        self.prompt_builder = PromptBuilder(self.model_version)
        self.prompt_builder.add_start()
        self.prompt_builder.add_prompt(
            """Context information is below.

        Context: {context}

        Chat history is below.

        Chat History: {history}

        Given the context and no prior knowledge, provide as much context surrounding the question as possible. There is no need to provide short answers.
        Remember to use the chat history to simplify and clarify the question, but do not provide an answer from chat history only the context provided.

        Question: {question}

        Answer:
        """
        )
        self.prompt_builder.add_end()
        self.input_variables = ["context", "history", "question"]
        self.custom_prompt = PromptTemplate(template=self.prompt_builder.get_prompt(), input_variables=self.input_variables)

    def start_qa_chain(self, verbose):
        # Retrieval QA
        # self.handler = StdOutCallbackHandler()

        self.qa_with_sources_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.ensemble_retriever if self.use_ensemble_retriever else self.faiss_retriever,
            # callbacks=[self.handler],
            chain_type_kwargs={
                "prompt": self.custom_prompt,
                "verbose": verbose,
                "memory": ConversationBufferMemory(memory_key="history", input_key="question"),
            },
            return_source_documents=True,
            verbose=verbose,
        )

    def execute_query(self, question):
        new_question = f"{question}. This question is for Harry Potter."
        response = self.qa_with_sources_chain.invoke({"query": new_question})
        return response["result"]


class LukecRAG:
    def __init__(self, use_ensemble_retriever=True, verbose=False, device="cuda"):
        logging.get_logger("transformers").setLevel(logging.ERROR)
        self.use_ensemble_retriever = use_ensemble_retriever
        self.read_documents = use_ensemble_retriever
        self.verbose = verbose
        if not os.path.exists(LUKEC_FAISS_PATH):
            # Must construct FAISS using existing documents
            self.read_documents = True
        if self.read_documents:
            self.start_directory_loader()
        self.start_vector_store()
        if self.read_documents:
            self.start_sparse_embedder()
        self.start_llm(device)
        self.construct_custom_prompt()
        self.start_qa_chain(verbose)

    def start_directory_loader(self):
        # Directory Loader
        directory_loader = LukecDataParser(directory="data/raw/")
        directory_loader.read_documents(self.verbose)
        self.lukec_docs = directory_loader.get_documents(self.verbose)
        # Text Splitter
        text_splitter = TextSplitter(chunk_size=1000, chunk_overlap=200)
        text_splitter.init_splitter()
        self.split_lukec_docs = text_splitter.split_documents(self.lukec_docs, self.verbose)

    def start_vector_store(self):
        # Vector Store
        self.vs = LukecVectorStore()
        self.vs.load_embeddings_model(self.verbose)
        self.vs.create_vector_store(self.split_lukec_docs, self.verbose)
        self.faiss_retriever = self.vs.get_faiss_retriever(k=5)

    def start_sparse_embedder(self):
        # Sparse embedder
        self.se = SparseEmbedding(self.split_lukec_docs, self.verbose)
        self.se.set_k(k=5)
        self.ensemble_retriever = self.se.get_ensemble_retriever(faiss_retriever=self.faiss_retriever)

    def start_llm(self, device):
        # LLM Model
        self.model_version = MISTRAL_ORCA
        self.model = AutoModelForCausalLM.from_pretrained(self.model_version, device_map=device)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_version, padding_side="left")
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        self.tokenizer.padding_side = "left"
        # Pipeline
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.1,
            top_p=0.95,
            top_k=40,
            repetition_penalty=1.1,
            return_full_text=False,
        )
        # LLM
        self.llm = HuggingFacePipeline(pipeline=self.pipe)
        # Caching
        langchain.llm_cache = InMemoryCache()

    def construct_custom_prompt(self):
        # Prompt
        self.prompt_builder = PromptBuilder(self.model_version)
        self.prompt_builder.add_start()
        self.prompt_builder.add_prompt(
            """Spodaj je podan kontekst.

        Kontekst: {context}

        Sledi zgodovina pogovora.

        Zgodovina pogovora: {history}

        S pomočjo konteksta in brez predhodnjega znanja odgovori na vprašanje, tako da odgovor vsebuje čim več konteksta o vprašanju.

        Vprašanje: {question}

        Odgovor:
        """
        )
        self.prompt_builder.add_end()
        self.input_variables = ["context", "history", "question"]
        self.custom_prompt = PromptTemplate(template=self.prompt_builder.get_prompt(), input_variables=self.input_variables)

    def start_qa_chain(self, verbose):
        # Retrieval QA
        # self.handler = StdOutCallbackHandler()

        self.qa_with_sources_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.ensemble_retriever if self.use_ensemble_retriever else self.faiss_retriever,
            # callbacks=[self.handler],
            chain_type_kwargs={
                "prompt": self.custom_prompt,
                "verbose": verbose,
                "memory": ConversationBufferMemory(memory_key="history", input_key="question"),
            },
            return_source_documents=True,
            verbose=verbose,
        )

    def execute_query(self, question):
        new_question = f"{question}"
        response = self.qa_with_sources_chain.invoke({"query": new_question})
        return response["result"]
