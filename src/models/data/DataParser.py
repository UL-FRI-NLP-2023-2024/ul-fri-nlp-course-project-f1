from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader


class DataParser:
    def __init__(self, directory):
        self.directory = directory

    def update_directory(self, new_directory):
        self.directory = new_directory

    def read_documents(self, verbose=False):
        if verbose:
            print("[DataParser] Reading the documents...")
        self.directory_loader = DirectoryLoader(
            self.directory, glob="harry_potter_book-*.pdf", loader_cls=PyPDFLoader, show_progress=True, use_multithreading=True
        )
        if verbose:
            print("[DataParser] Finished reading the documents.")

    def get_documents(self, verbose=False):
        if verbose:
            print("[DataParser] Loading the documents...")
        self.documents = self.directory_loader.load()
        if verbose:
            print(f"[DataParser] Finished loading the documents. Length of documents: {len(self.documents)}")
        return self.documents
