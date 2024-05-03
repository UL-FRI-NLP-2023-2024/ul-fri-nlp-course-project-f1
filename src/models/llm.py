from models.utils.ModelVersion import LLAMA_3_8B

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


class HPLLM:
    def __init__(self):
        self.model_version = LLAMA_3_8B

    def prepare_model(self):
        self.model = AutoModelForCausalLM.from_pretrained(self.model_version, torch_dtype=torch.bfloat16, device_map="cuda")

    def prepare_tokenizer(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_version)

    def load_model(self) -> None:
        # Prepare base model
        self.prepare_model()
        # Prepare tokenizer
        self.prepare_tokenizer()
        # Get adapters
        # self.peft_config = PeftConfig.from_pretrained(f"models/{self.fine_tuned_model_directory}-final")
        # self.peft_config.init_lora_weights = False
        # self.original_model.add_adapter(self.peft_config)
        # self.original_model.enable_adapters()

    def prepare_prompt(self, question, has_context=False):
        if has_context:
            messages = [
                {
                    "role": "system",
                    "content": "You are Harry Potter from the Harry Potter universe who always responds to the Question as Harry Potter including their personality. Please do not make these answers too long and make sure a chat can happen! Make sure to use the Context information to formalize the best and most accurate response possible.",
                },
                {"role": "user", "content": question},
            ]
        else:
            messages = [
                {
                    "role": "system",
                    "content": "You are Harry Potter from the Harry Potter universe who always responds as Harry Potter including their personality. Please do not make these answers too long and make sure a chat can happen!",
                },
                {"role": "user", "content": question},
            ]
        return self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    def query_model(self, question):
        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="cuda",
        )

        prompt = self.prepare_prompt(question, has_context=False)

        terminators = [self.tokenizer.eos_token_id, self.tokenizer.convert_tokens_to_ids("<|eot_id|>")]

        outputs = pipe(
            prompt,
            max_new_tokens=256,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        return outputs[0]["generated_text"][len(prompt) :]

    def query_model_with_context(self, question, context):
        new_question = f"Context: {context} \n Question: {question}"
        return self.query_model(new_question)
