from google import genai
from google.genai import types
import os
from PIL import Image
from typing import List, Dict, Any
from tenacity import retry, wait_exponential, stop_after_attempt
import json

@retry(
    wait=wait_exponential(multiplier=2, min=5, max=60),
    stop=stop_after_attempt(10),
    before_sleep=lambda retry_state: print(f"[*] Rate limited (Extraction). Retrying in {retry_state.next_action.sleep} seconds...")
)
def extract_batch(image_paths: List[str], bank_name: str) -> Dict[str, Any]:
    """
    Extracts structured data from a batch of images.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    images = [Image.open(path) for path in image_paths]
    
    prompt = f"""
    Extract data from these {bank_name} statement pages into JSON:
    {{
      "account_holder": "string",
      "account_number": "string",
      "ifsc": "string",
      "transactions": [
        {{
          "date": "string",
          "description": "string",
          "debit": float,
          "credit": float,
          "balance": float
        }}
      ]
    }}
    Include all transactions found across these pages.
    """
    
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=[prompt] + images,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        )
    )
    
    try:
        return json.loads(response.text)
    except Exception as e:
        print(f"[!] Failed to parse JSON: {e}")
        return {"transactions": []}

def extract_all_pages(image_paths: List[str], bank_name: str) -> Dict[str, Any]:
    """
    Processes images in batches and aggregates the results.
    """
    aggregated_data = {
        "bank_name": bank_name,
        "account_holder": "UNKNOWN",
        "account_number": "UNKNOWN",
        "ifsc": "UNKNOWN",
        "transactions": []
    }
    
    batch_size = 3
    for i in range(0, len(image_paths), batch_size):
        batch_paths = image_paths[i:i + batch_size]
        print(f"[*] Processing batch {i//batch_size + 1}/{(len(image_paths)-1)//batch_size + 1} ({len(batch_paths)} pages)...")
        
        batch_data = extract_batch(batch_paths, bank_name)
        
        # Update header info if found and not yet set
        for key in ["account_holder", "account_number", "ifsc"]:
            if batch_data.get(key) and batch_data[key] != "string" and aggregated_data[key] == "UNKNOWN":
                aggregated_data[key] = batch_data[key]
            
        # Append transactions
        if "transactions" in batch_data:
            aggregated_data["transactions"].extend(batch_data["transactions"])
            
    return aggregated_data
