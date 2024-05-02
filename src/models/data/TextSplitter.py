from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextSplitter:
    def __init__(self, chunk_size, chunk_overlap):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def update(self, new_chunk_size, new_chunk_overlap):
        self.chunk_size = new_chunk_size
        self.chunk_overlap = new_chunk_overlap

    def init_splitter(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

    def split_documents(self, documents, verbose=False):
        if verbose:
            print("[TextSplitter] Splitting the documents...")
        self.split_docs = self.text_splitter.transform_documents(documents)
        if verbose:
            print(f"[TextSplitter] Finished splitting the documents. Number of chunks in documents: {len(self.split_docs)}")
        return self.split_docs
