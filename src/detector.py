from google import genai
from PIL import Image
import os
import time
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

@retry(
    wait=wait_exponential(multiplier=2, min=5, max=60),
    stop=stop_after_attempt(5),
    before_sleep=lambda retry_state: print(f"[*] Rate limited (Detection). Retrying in {retry_state.next_action.sleep} seconds...")
)
def detect_bank(image_path: str) -> str:
    """
    Identifies the bank from the first page of the statement.
    Supported: HDFC, ICICI, SBI.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
        
    client = genai.Client(api_key=api_key)
    
    img = Image.open(image_path)
    
    prompt = """
    Analyze the following bank statement image and identify which bank it belongs to.
    Current supported banks are: HDFC, ICICI, SBI.
    
    Look for logos, header text, or addresses that mention the bank name.
    
    Return ONLY the bank name in uppercase (e.g., 'HDFC', 'ICICI', 'SBI').
    If the bank is not one of the supported ones, return the name of the bank you see anyway.
    If you cannot find any bank name, return 'UNKNOWN'.
    """
    
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=[prompt, img]
    )
    detected_text = response.text.strip().upper()
    
    # Flexible matching
    valid_banks = {
        "HDFC": ["HDFC", "HOUSING DEVELOPMENT FINANCE"],
        "ICICI": ["ICICI"],
        "SBI": ["SBI", "STATE BANK OF INDIA"],
        "AXIS": ["AXIS"]
    }
    
    for standard_name, aliases in valid_banks.items():
        if any(alias in detected_text for alias in aliases):
            return standard_name
            
    return detected_text if detected_text else "UNKNOWN"
