from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from models.utils.ModelVersion import BGE_SMALL, FAISS_PATH

import os


class VectorStore:
    def __init__(self):
        self.store = LocalFileStore("./cache/")
        self.embedding_model_version = BGE_SMALL

    def load_embeddings_model(self, verbose):
        if verbose:
            print("[VectorStore] Preparing Embeddings Model...")
        self.embedding_model = HuggingFaceEmbeddings(model_name=self.embedding_model_version)
        if verbose:
            print("[VectorStore] Finished preparing Embeddings Model.")
            print("[VectorStore] Preparing Cache Backed Embeddings Model...")
        self.embedder = CacheBackedEmbeddings.from_bytes_store(self.embedding_model, self.store, namespace=self.embedding_model_version)
        if verbose:
            print("[VectorStore] Finished preparing Cache Backed Embeddings Model.")

    def get_embedding_model(self):
        if self.embedding_model:
            return self.embedding_model
        else:
            raise RuntimeError("Embedding Model does not exist!")

    def create_vector_store(self, split_docs, verbose):
        if verbose:
            print("[VectorStore] Preparing FAISS Vector Store...")
        if os.path.exists(FAISS_PATH):
            self.vector_store = FAISS.load_local(FAISS_PATH, self.embedder, allow_dangerous_deserialization=True)
        else:
            self.vector_store = FAISS.from_documents(split_docs, self.embedder)
            self.vector_store.save_local(FAISS_PATH)
        if verbose:
            print("[VectorStore] Finished preparing FAISS Vector Store.")

    def get_vector_store(self):
        if self.vector_store:
            return self.vector_store
        else:
            raise RuntimeError("Vector Store does not exist!")

    def get_faiss_retriever(self, k):
        if self.vector_store:
            return self.vector_store.as_retriever(search_kwargs={"k": k})
