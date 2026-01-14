from src.parsers.base import BaseParser
from src.models import BankStatement

class ICICIParser(BaseParser):
    def __init__(self):
        super().__init__(bank_name="ICICI")

    def parse(self, raw_text: str) -> BankStatement:
        schema_prompt = """
        ICICI statements typically include 'Value Date', 'Transaction Date', 'Description', 'Withdrawal (DR)', 'Deposit (CR)', 'Balance'.
        Map 'Withdrawal (DR)' to 'debit' and 'Deposit (CR)' to 'credit'.
        Ensure 'account_holder' and 'account_number' are extracted from the header.
        """
        return self._ai_parse(raw_text, schema_prompt)
