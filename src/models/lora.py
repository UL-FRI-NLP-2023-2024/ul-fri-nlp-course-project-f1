from models.utils.ModelVersion import LLAMA_3_8B

from datasets import load_dataset
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, pipeline
from trl import SFTTrainer
from peft import LoraConfig, get_peft_model, PeftModel
import os
import torch
from functools import partial


class HPLora:
    def __init__(self, fine_tuned_model_directory):
        os.environ["WANDB_DISABLED"] = "true"
        self.model_version = LLAMA_3_8B
        self.seed = 42
        self.fine_tuned_model_directory = fine_tuned_model_directory

    def get_max_length(self, verbose=False):
        if self.original_model:
            self.max_length = None
            for length_setting in ["n_positions", "max_position_embeddings", "seq_length"]:
                self.max_length = getattr(self.original_model.config, length_setting, None)
                if self.max_length:
                    if verbose:
                        print(f"Found max lenth: {self.max_length}")
                    break
            if not self.max_length:
                self.max_length = 1024
                if verbose:
                    print(f"Using default max length: {self.max_length}")
        else:
            raise RuntimeError("Model does not exist!")

    def preprocess_batch(self, batch):
        """
        Tokenizing a batch
        """
        if self.tokenizer:
            return self.tokenizer(
                batch["text"],
                max_length=self.max_length,
                truncation=True,
            )
        else:
            raise RuntimeError("Tokenizer does not exist!")

    def preprocess_dataset(self, dataset, verbose=False):
        if self.max_length is None or self.tokenizer is None:
            raise RuntimeError("Max Lenght or Tokenizer does not exist!")
        # Add prompt to each sample
        if verbose:
            print("Preprocessing dataset...")
        dataset = dataset.map(self.create_prompt)  # , batched=True)

        # Apply preprocessing to each batch of the dataset & and remove 'instruction', 'context', 'response', 'category' fields
        _preprocessing_function = partial(self.preprocess_batch)
        dataset = dataset.map(
            _preprocessing_function,
            batched=True,
            remove_columns=["id", "scene", "dialogue", "harry_response"],
        )

        # Filter out samples that have input_ids exceeding max_length
        dataset = dataset.filter(lambda sample: len(sample["input_ids"]) < self.max_length)

        # Shuffle dataset
        dataset = dataset.shuffle(seed=self.seed)

        return dataset

    def create_prompt(self, sample):

        formatted_prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are Harry Potter from the Harry Potter universe who always responds as Harry Potter including their personality. Please do not make these answers too long and make sure a chat can happen!<|eot_id|><|start_header_id|>user<|end_header_id|>
        Context: {sample['scene']}
        Question: {sample['dialogue']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
        {sample['harry_response']}<|eot_id|><|end_of_text|>
        """
        sample["text"] = formatted_prompt

        return sample

    def read_dataset(self, verbose=False):
        if verbose:
            print(f"Reading the datasets...")
        self.json_dataset = load_dataset(
            "json", data_files={"train": "data/processed/train_harry_dataset.json", "validation": "data/processed/eval_harry_dataset.json"}
        )
        if verbose:
            print(f"Train Example: {self.json_dataset['train'][0]}")
            print(f"Eval Example: {self.json_dataset['validation'][0]}")

    def prepare_original_model(self, verbose=False):
        if verbose:
            print("Preparing the original model...")
        self.original_model = AutoModelForCausalLM.from_pretrained(
            self.model_version,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        if verbose:
            print("Finished preparing the origina model.")

    def prepare_tokenizer(self, verbose=False):
        if verbose:
            print("Preparing the tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_version, trust_remote_code=True)
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        if verbose:
            print("Finished preparing the tokenizer.")

    def prepare_lora_config(self):
        self.config = LoraConfig(
            r=16,  # Rank
            lora_alpha=8,
            target_modules=["q_proj", "k_proj", "v_proj", "dense"],
            bias="none",
            lora_dropout=0.05,  # Conventional
            task_type="CAUSAL_LM",
        )

    def prepare_training_arguments(self):
        self.peft_training_args = TrainingArguments(
            output_dir=f"models/{self.fine_tuned_model_directory}",
            warmup_steps=1,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=1,
            max_steps=1000,
            learning_rate=2e-4,
            logging_steps=25,
            logging_dir=f"logs/{self.fine_tuned_model_directory}",
            save_strategy="steps",
            save_steps=25,
            evaluation_strategy="steps",
            eval_steps=25,
            do_eval=True,
            gradient_checkpointing=True,
            report_to="none",
            overwrite_output_dir="True",
            group_by_length=True,
        )

    def prepare_trainer(self):
        self.peft_trainer = SFTTrainer(
            model=self.peft_model,
            args=self.peft_training_args,
            train_dataset=self.train_dataset,
            eval_dataset=self.eval_dataset,
            dataset_text_field="text",
            tokenizer=self.tokenizer,
            packing=False,
            peft_config=self.config,
            max_seq_length=self.max_length,
        )

    def fine_tune_model(self, verbose=False):
        # Read the train and eval dataset
        self.read_dataset(verbose)
        # Prepare model
        self.prepare_original_model(verbose)
        # Prepare tokenizer
        self.prepare_tokenizer(verbose)
        # Read the max length
        self.get_max_length(verbose)
        # Preprocess datasets
        self.train_dataset = self.preprocess_dataset(self.json_dataset["train"], verbose)
        self.eval_dataset = self.preprocess_dataset(self.json_dataset["validation"], verbose)
        # Prepare config for LoRA
        self.prepare_lora_config()
        # Enable gradient checkpointing - reduces memory load
        self.original_model.gradient_checkpointing_enable()
        # Create PEFT model
        self.peft_model = get_peft_model(self.original_model, self.config)
        del self.original_model
        if verbose:
            self.peft_model.print_trainable_parameters()
        # Prepare training arguments for LoRA
        self.prepare_training_arguments()
        # Do not use cache
        self.peft_model.config.use_cache = False
        # Prepare trainer
        self.prepare_trainer()
        # Start the training
        self.peft_trainer.train()
        # Save the model
        self.peft_model.save_pretrained(f"models/{self.fine_tuned_model_directory}-final")

class HPLoraLLM:
    def __init__(self, peft_path):
        self.original_model = LLAMA_3_8B
        self.peft_model = peft_path

    def prepare_model(self, original_device="cuda", peft_device="cuda"):
        self.base_model = AutoModelForCausalLM.from_pretrained(self.original_model, device_map=original_device)
        self.merged_model = PeftModel.from_pretrained(self.base_model, self.peft_model, device_map=peft_device)

    def prepare_tokenizer(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.original_model, padding_side="left")
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

    def load_model(self, original_device="cuda", peft_device="cuda"):
        self.prepare_model(original_device=original_device, peft_device=peft_device)
        self.prepare_tokenizer()

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
            model=self.merged_model,
            tokenizer=self.tokenizer,
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