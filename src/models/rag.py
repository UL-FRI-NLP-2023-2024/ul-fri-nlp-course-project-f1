from models.data.DataParser import DataParser
from models.data.TextSplitter import TextSplitter
from models.utils.VectorStore import VectorStore
from models.utils.SparseEmbedding import SparseEmbedding
from models.utils.ModelVersion import MISTRAL_LITE, MISTRAL_ORCA, FAISS_PATH
from models.utils.PromptBuilder import PromptBuilder

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
import langchain
from langchain_core.prompts import PromptTemplate
from langchain_community.cache import InMemoryCache
from langchain_core.callbacks.stdout import StdOutCallbackHandler
from langchain.chains.retrieval_qa.base import RetrievalQA

import os


class HPRag:
    def __init__(self, use_ensemble_retriever=True, verbose=False):
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
        self.start_llm()
        self.construct_custom_prompt()
        self.start_qa_chain()

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
        self.vs.create_vector_store(None, self.verbose)
        self.faiss_retriever = self.vs.get_faiss_retriever(k=5)

    def start_sparse_embedder(self):
        # Sparse embedder
        self.se = SparseEmbedding(self.split_hp_docs, self.verbose)
        self.se.set_k(k=5)
        self.ensemble_retriever = self.se.get_ensemble_retriever(faiss_retriever=self.faiss_retriever)

    def start_llm(self):
        # LLM Model
        self.model_version = MISTRAL_ORCA
        self.model = AutoModelForCausalLM.from_pretrained(self.model_version, device_map="cuda")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_version)
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
            """You are an expert concerning everything Harry Potter. You are an expert in the Harry Potter franchise and remember every event that happened.
        With the information being provided try to provide as much context and important information surrounding the question.
        If you can't answer the question based on the information either say you can't find an answer or unable to find an answer.
        So try to understand in depth about the context and answer only based on the information provided. Don't generate irrelevant answers.

        Context: {context}
        Question: {question}

        Do provide only helpful answers, but don't limit yourself to only short answers. Try to provide as much context to the answer as possible.

        Helpful answer:
        """
        )
        self.prompt_builder.add_end()
        self.input_variables = ["context", "question"]
        self.custom_prompt = PromptTemplate(template=self.prompt_builder.get_prompt(), input_variables=self.input_variables)

    def start_qa_chain(self):
        # Retrieval QA
        self.handler = StdOutCallbackHandler()

        self.qa_with_sources_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.ensemble_retriever if self.use_ensemble_retriever else self.faiss_retriever,
            callbacks=[self.handler],
            chain_type_kwargs={"prompt": self.custom_prompt},
            return_source_documents=True,
        )

    def execute_query(self, question):
        new_question = f"{question}. This question is for Harry Potter."
        response = self.qa_with_sources_chain.invoke({"query": new_question})
        return response["result"]
