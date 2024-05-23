from models.rag import HPRag
from models.llm import HPInteractiveLLM

if __name__ == "__main__":
    print(f"Welcome to the Harry Potter Chatbot")
    # Retrieval Augmented Generation
    print("[RAG] Initializing...")
    hp_rag = HPRag(use_ensemble_retriever=True, verbose=False, device="cuda:0")
    print("[RAG] Initialization successful!")
    # Large Language Model
    print("[LLM] Initializing...")
    hp_llm = HPInteractiveLLM()
    print("[LLM] Preparing the model...")
    hp_llm.prepare_model(device="cuda:1")
    print("[LLM] Model preparation successful!")
    print("[LLM] Preparing the tokenizer...")
    hp_llm.prepare_tokenizer()
    print("[LLM] Tokenizer preparation successful!")
    hp_llm.start_llm(device="cuda:1")
    hp_llm.start_chain()
    while True:
        # Get question from the user
        question = input("Q: ")
        # Get context with RAG
        context = hp_rag.execute_query(question)
        # print(f"C: {context}")
        response = hp_llm.query_model_with_context(question, context)
        print(f"A: {response}")
