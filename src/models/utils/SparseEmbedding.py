from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever


class SparseEmbedding:
    def __init__(self, split_docs, verbose):
        if verbose:
            print("[SparseEmbedding] Preparing Sparse Embedding Model...")
        self.bm25_retriever = BM25Retriever.from_documents(split_docs)
        if verbose:
            print("[SparseEmbedding] Finished preparing Sparse Embedding Model...")

    def update_documents(self, new_split_docs):
        self.bm25_retriever = BM25Retriever.from_documents(new_split_docs)

    def set_k(self, k):
        self.bm25_retriever.k = k

    def get_sparse_embedding_retriever(self):
        return self.bm25_retriever

    def get_ensemble_retriever(self, faiss_retriever):
        self.ensemble_retriever = EnsembleRetriever(retrievers=[self.bm25_retriever, faiss_retriever], weights=[0.5, 0.5])
        return self.ensemble_retriever
