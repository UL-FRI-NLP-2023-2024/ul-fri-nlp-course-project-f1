import logging
from openai import OpenAI
from secrets import CHATGPT_API_KEY

logging.basicConfig(level=logging.INFO)

class ChatGPTClient:
    def __init__(self):
        self.client = OpenAI(api_key=CHATGPT_API_KEY)

    def send_prompt(self, prompt_text: str, max_tokens: int = 500, model: str = "gpt-3.5-turbo-0125") -> str:
        """Sends a prompt to the ChatGPT and returns the response."""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{ "role": "user", "content": prompt_text}],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

if __name__ == '__main__':
    client = ChatGPTClient()
    test_prompt = "Hello, world! How are you today?"
    logging.info("Sending test prompt...")
    result = client.send_prompt(test_prompt)
    logging.info(f"Response from ChatGPT: {result}")
