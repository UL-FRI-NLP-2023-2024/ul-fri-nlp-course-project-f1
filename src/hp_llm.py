from models.llm import HPLLM
from models.rag import HPRag

if __name__ == "__main__":
    # Question
    question = "Hey Harry, I wonder what would you say is your favorite sport?"
    # Retrieval Augmented Generation
    hp_rag = HPRag(use_ensemble_retriever=True, verbose=True, device="cuda:0")
    # Get the context
    context = hp_rag.execute_query(question)
    # print(f"Context: {context}")
    # Free up memory on GPU
    # del hp_rag
    # Large Language Model
    hp_llm = HPLLM()
    # Load the model
    hp_llm.prepare_model(device="cuda:1")
    # Load the tokenizer
    hp_llm.prepare_tokenizer()
    # Get the response
    response = hp_llm.query_model_with_context(question, context)
    # response = hp_llm.query_model(question)
    print(f"Question: {question}")
    print(f"Response: {response}")
