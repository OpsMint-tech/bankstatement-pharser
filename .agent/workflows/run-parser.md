---
description: How to run the Bank Statement AI Parser
---

## Prerequisites
1. **Google Gemini API Key**: Get one from [Google AI Studio](https://aistudio.google.com/).
2. **Poppler**: Required for `pdf2image`. On Mac, run `brew install poppler`.

## Setup
1. Create a `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```
2. Add your `GEMINI_API_KEY` to the `.env` file.

## Running the Parser
// turbo
1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Run the parser on a PDF file:
   ```bash
   python3 -m src.main Account_stmt-inforvio.pdf 
   ```

## Output
- The structured JSON will be displayed in the terminal.
- A file named `output.json` will be created in the root directory.
