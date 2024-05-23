from models.rag import LukecRAG
from models.llm import LukecInteractiveLLM

if __name__ == "__main__":
    print(f"Lukec in njegov škorec pogovorni bot")
    # Retrieval Augmented Generation
    print("[RAG] Initializing...")
    lukec_rag = LukecRAG(use_ensemble_retriever=True, verbose=False, device="cuda:0")
    print("[RAG] Initialization successful!")
    # Large Language Model
    print("[LLM] Initializing...")
    lukec_llm = LukecInteractiveLLM()
    print("[LLM] Preparing the model...")
    lukec_llm.prepare_model(device="cuda:1")
    print("[LLM] Model preparation successful!")
    print("[LLM] Preparing the tokenizer...")
    lukec_llm.prepare_tokenizer()
    print("[LLM] Tokenizer preparation successful!")
    lukec_llm.start_llm(device="cuda:1")
    lukec_llm.start_chain()
    while True:
        # Get question from the user
        question = input("Q: ")
        # Get context with RAG
        context = lukec_rag.execute_query(question)
        # print(f"C: {context}")
        response = lukec_llm.query_model_with_context(question, context)
        print(f"A: {response}")
