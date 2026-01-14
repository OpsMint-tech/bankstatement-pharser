import os
from dotenv import load_dotenv
from src.converter import convert_pdf_to_images
from src.detector import detect_bank
from src.extractor import extract_all_pages
from src.models import BankStatement

load_dotenv()

class StatementProcessor:
    def __init__(self):
        pass

    def process_statement(self, pdf_path: str) -> BankStatement:
        print(f"[*] Processing: {pdf_path}")
        
        # 1. PDF to Image
        print("[*] Converting PDF to images...")
        image_paths = convert_pdf_to_images(pdf_path)
        
        # 2. Bank Detection (First page)
        print("[*] Detecting bank...")
        bank_name = detect_bank(image_paths[0])
        print(f"[+] Detected Bank: {bank_name}")
        
        if bank_name == "UNKNOWN":
            print("[!] Warning: Bank could not be automatically detected. Proceeding with generic parsing.")
            bank_name = "Generic Bank"
        
        # 3. Chunked Extraction (Page by Page)
        print("[*] Starting chunked extraction...")
        structured_data = extract_all_pages(image_paths, bank_name)
        
        # 4. Final Validation/Model Casting
        print("[*] Finalizing structured output...")
        return BankStatement(**structured_data)

if __name__ == "__main__":
    import sys
    import json
    import traceback
    
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <path_to_pdf>")
        sys.exit(1)
        
    pdf_input = sys.argv[1]
    processor = StatementProcessor()
    
    try:
        result = processor.process_statement(pdf_input)
        print("\n--- Final Structured Output ---")
        print(result.model_dump_json(indent=2))
        
        # Save to output file
        output_file = "output.json"
        with open(output_file, "w") as f:
            f.write(result.model_dump_json(indent=2))
        print(f"\n[+] Results saved to {output_file}")
        
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        traceback.print_exc()
