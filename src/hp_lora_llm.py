from models.lora import HPLoraLLM

if __name__ == "__main__":
    # Question
    question = "Hey Harry my name is Zan and I wonder what would you say is your favorite sport?"
    # Large Language Model
    hp_lora_llm = HPLoraLLM(peft_path="models/peft-final")
    # Load the model
    hp_lora_llm.load_model(original_device="cuda:0", peft_device="cuda:1")
    # Get the response
    response = hp_lora_llm.query_model(question)
    # response = hp_llm.query_model(question)
    print(f"Question: {question}")
    print(f"Response: {response}")
