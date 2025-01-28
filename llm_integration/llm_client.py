from abc import ABC, abstractmethod
from openai import OpenAI
import time
import threading


class BaseLLMClient(ABC):
    @abstractmethod
    def generate_response(self, system_prompt: str, user_input: str) -> str:
        pass


class DeepSeekClient(BaseLLMClient):
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com"):
        print("[INFO] Initializing DeepSeekClient...")
        self.api_key = api_key
        self.base_url = base_url
        try:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            print(f"[INFO] DeepSeekClient initialized successfully with base_url: {base_url}")
        except Exception as e:
            print(f"[ERROR] Failed to initialize DeepSeekClient: {e}")
            raise

    def generate_response(self, system_prompt: str, user_input: str) -> str:
        print(f"[INFO] Generating response from DeepSeekClient...")
        print(f"[DEBUG] System Prompt: {system_prompt}")
        print(f"[DEBUG] User Input: {user_input}")

        start_time = time.time()
        progress_thread = threading.Thread(target=self._log_progress, args=(start_time,))
        progress_thread.daemon = True  # Allows the program to exit even if thread is running
        progress_thread.start()

        try:
            response = self.client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
                stream=False,
                max_tokens=8000
            )
            end_time = time.time()
            print(f"[INFO] Response generated successfully in {end_time - start_time:.2f} seconds.")
            print(f"[DEBUG] Full Response: {response}")
            return response.choices[0].message.content
        except Exception as e:
            end_time = time.time()
            print(f"[ERROR] Failed to generate response: {e}")
            print(f"[INFO] Time taken before failure: {end_time - start_time:.2f} seconds")
            raise
        finally:
            # Allow the thread to gracefully exit
            self._stop_progress = True
            progress_thread.join()

    def _log_progress(self, start_time):
        """
        Logs the elapsed time every 2 seconds until the process completes.
        """
        self._stop_progress = False
        while not self._stop_progress:
            elapsed_time = time.time() - start_time
            print(f"[INFO] Time elapsed for the LLM ro respond: {elapsed_time:.2f} seconds...", end="\r", flush=True)
            time.sleep(0.01)  # Update every 2 seconds
