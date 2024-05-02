import torch
import logging
from transformers import GPTNeoXForCausalLM, GPTNeoXTokenizerFast, GPTNeoForCausalLM, GPT2Tokenizer

logging.basicConfig(level=logging.INFO)
GPT_NEO = "EleutherAI/gpt-neo-1.3B"

class GPTNeoClient:
    def __init__(self, model_name: str = GPT_NEO) -> None:
        """
        Initializes the GPTNeo client with the specified model.
        """
        logging.info("Intializing he model...")
        self.model = GPTNeoForCausalLM.from_pretrained(model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        if torch.cuda.is_available():
            self.model.to("cuda")
        logging.info("Successfully initialised!")

    def generate_text(
        self, prompt: str, max_length: int = 100, temperature: float = 0.9, do_sample: bool = True
    ) -> str:
        """
        Generates text based on the provided prompt.
        """
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        if torch.cuda.is_available():
            input_ids = input_ids.to("cuda")

        gen_tokens = self.model.generate(
            input_ids, do_sample=do_sample, temperature=temperature, max_length=max_length
        )

        return self.tokenizer.batch_decode(gen_tokens)[0]

if __name__ == "__main__":
    client = GPTNeoClient()
    prompt = "Hello, world! How are you today?"
    logging.info("Promting the model...")
    generated_text = client.generate_text(prompt)
    print(f"Response from the model: {generated_text}")

