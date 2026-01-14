import os
import shutil
import uuid
from datetime import datetime
from dotenv import load_dotenv
from src.converter import convert_pdf_to_images
from src.detector import detect_bank
from src.extractor import extract_all_pages
from src.analyzer import analyze_statement
from src.models import BankStatement

load_dotenv()

class StatementProcessor:
    def __init__(self):
        pass

    def process_statement(self, pdf_path: str, job_id: str = None) -> BankStatement:
        if not job_id:
            job_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            
        print(f"[*] Processing: {pdf_path} (Job ID: {job_id})")
        
        # Create a unique temp directory for this job's images
        temp_dir = os.path.join("temp_images", job_id)
        
        try:
            # 1. PDF to Image
            print(f"[*] Converting PDF to images in {temp_dir}...")
            image_paths = convert_pdf_to_images(pdf_path, output_dir=temp_dir)
            
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
            statement = BankStatement(**structured_data)
            
            # 5. Analysis (ABB, etc.)
            print("[*] Calculating ABB and analyzing transactions...")
            return analyze_statement(statement)
            
        finally:
            # Cleanup: Remove the temporary images directory
            if os.path.exists(temp_dir):
                print(f"[*] Cleaning up temporary images in {temp_dir}...")
                shutil.rmtree(temp_dir)

if __name__ == "__main__":
    import sys
    import json
    import traceback
    import uuid
    from datetime import datetime
    
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <path_to_pdf>")
        sys.exit(1)
        
    pdf_input = sys.argv[1]
    
    # Generate Unique ID for this run
    job_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    print(f"[*] Starting Job ID: {job_id}")
    
    processor = StatementProcessor()
    
    try:
        result = processor.process_statement(pdf_input, job_id=job_id)
        print("\n--- Final Structured Output ---")
        # Print a snippet to console to avoid cluttering terminal
        print(f"[+] Extracted {len(result.transactions)} transactions.")
        
        # Save to unique output file
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, f"result_{job_id}.json")
        with open(output_file, "w") as f:
            f.write(result.model_dump_json(indent=2))
            
        print(f"\n[+] Results saved uniquely to: {output_file}")
        
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        traceback.print_exc()
