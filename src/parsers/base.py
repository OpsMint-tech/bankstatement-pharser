from abc import ABC, abstractmethod
from src.models import BankStatement
from google import genai
from google.genai import types
import os
import json
from tenacity import retry, wait_exponential, stop_after_attempt

class BaseParser(ABC):
    def __init__(self, bank_name: str):
        self.bank_name = bank_name
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")
        self.client = genai.Client(api_key=self.api_key)

    @abstractmethod
    def parse(self, raw_text: str) -> BankStatement:
        pass

    @retry(
        wait=wait_exponential(multiplier=2, min=5, max=60),
        stop=stop_after_attempt(10),
        before_sleep=lambda retry_state: print(f"[*] Rate limited. Retrying in {retry_state.next_action.sleep} seconds...")
    )
    def _ai_parse(self, raw_text: str, schema_prompt: str) -> BankStatement:
        prompt = f"""
        You are an expert financial data parser. 
        Convert the following raw text from a {self.bank_name} statement into a structured JSON.
        
        {schema_prompt}
        
        Raw Text:
        {raw_text}
        
        JSON Output:
        """
        
        response = self.client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        data = json.loads(response.text)
        return BankStatement(**data)
