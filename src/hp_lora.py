from models.lora import HPLora

if __name__ == "__main__":
    hp_lora = HPLora(fine_tuned_model_directory="peft")
    hp_lora.fine_tune_model(verbose=True)
