from models.rag import HPRag
from models.llm import HPInteractiveLLM

if __name__ == "__main__":
    print(f"Welcome to the Harry Potter Chatbot")
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
        response = hp_llm.query_model(question)
        print(f"A: {response}")
