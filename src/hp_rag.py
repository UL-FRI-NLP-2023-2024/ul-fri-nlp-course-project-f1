from models.rag import HPRag


if __name__ == "__main__":
    hp_rag = HPRag(use_ensemble_retriever=False, verbose=True)
    question = "Do you remember what spell Ron mocked Hermione over?"
    response = hp_rag.execute_query(question)
    print(f"Response: {response}")
