import openai
import logging
from secrets import CHATGPT_API_KEY

logging.basicConfig(level=logging.INFO)

class ChatGPTClient:
    def __init__(self):
        openai.api_key = CHATGPT_API_KEY

    def send_prompt(self, prompt_text: str, max_tokens: int = 500, model: str = "gpt-4") -> str:
        """Sends a prompt to the ChatGPT and returns the response."""
        try:
            response = openai.Completion.create(
                model=model,
                prompt=prompt_text,
                max_tokens=max_tokens
            )
            return response.choices[0].text
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

if __name__ == '__main__':
    client = ChatGPTClient()
    test_prompt = "Hello, world! How are you today?"
    logging.info("Sending test prompt...")
    result = client.send_prompt(test_prompt)
    logging.info(f"Response from ChatGPT: {result}")
