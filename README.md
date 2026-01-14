# Bank Statement AI Parser - Implementation Plan

## Overview
An AI-powered pipeline to convert bank statement PDFs into structured JSON data using Gemini's Vision and Language capabilities.

## Tech Stack
- **Language**: Python 3.10+
- **PDF Processing**: `pdf2image` (requires `poppler`)
- **AI Engine**: Google Gemini (via `google-generativeai`)
- **Data Validation**: `pydantic`

## Project Structure
```
.
├── src/
│   ├── __init__.py
│   ├── main.py          # Entry point and pipeline orchestration
│   ├── converter.py     # PDF to Image conversion
│   ├── detector.py      # Bank detection logic (Gemini Vision)
│   ├── extractor.py     # Text extraction logic (Gemini Vision)
│   ├── models.py        # Pydantic schemas for structured output
│   └── parsers/         # Bank-specific parsing logic
│       ├── __init__.py
│       ├── base.py      # Base class for parsers
│       ├── hdfc.py
│       ├── icici.py
│       └── sbi.py
├── data/                # Input PDFs and temp storage
├── tests/               # Unit and integration tests
├── requirements.txt
└── .env
```

## Workflow
1. **PDF to Image**: Convert all pages of the input PDF to high-quality images.
2. **Bank Detection**: Send the first page to Gemini Vision to identify the bank (HDFC, ICICI, SBI).
3. **Full Text Extraction**: Send all images to Gemini Vision to extract raw text (markdown/structured).
4. **Parsing**: route raw text to the detected bank's parser to map it to the standard Pydantic schema.
5. **Output**: Return the final JSON.
