from models.utils.ModelVersion import MISTRAL_LITE, MISTRAL_8x22, MISTRAL_ORCA


class PromptBuilder:
    def __init__(self, model_version):
        self.model_version = model_version
        self.prompt = ""

    def update(self, model_version):
        self.model_version = model_version
        self.prompt = ""

    def reset_(self):
        self.prompt = ""

    def add_start(self):
        if self.model_version == MISTRAL_LITE:
            self.prompt += "<|prompter|>"
        elif self.model_version == MISTRAL_8x22:
            self.prompt += ""
        elif self.model_version == MISTRAL_ORCA:
            self.prompt += "<|im_start|>"
        else:
            raise RuntimeError(f"Model version: {self.model_version} is not supported!")

    def add_prompt(self, prompt):
        self.prompt += prompt

    def add_end(self):
        if self.model_version == MISTRAL_LITE:
            self.prompt += "</s><|assistant|>"
        elif self.model_version == MISTRAL_8x22:
            self.prompt += ""
        elif self.model_version == MISTRAL_ORCA:
            self.prompt += "<|im_end|>"
        else:
            raise RuntimeError(f"Model version: {self.model_version} is not supported!")

    def get_prompt(self):
        return self.prompt
