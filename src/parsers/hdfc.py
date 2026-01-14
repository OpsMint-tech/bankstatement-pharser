from src.parsers.base import BaseParser
from src.models import BankStatement

class HDFCParser(BaseParser):
    def __init__(self):
        super().__init__(bank_name="HDFC")

    def parse(self, raw_text: str) -> BankStatement:
        schema_prompt = """
        HDFC statements often have columns like Date, Narration, Chq/Ref no, Value Date, Withdrawal Amt, Deposit Amt, Closing Balance.
        Map Withdrawal Amt to 'debit' and Deposit Amt to 'credit'.
        Mask the account number (e.g., XXXXXX1234).
        Include dates in YYYY-MM-DD format if possible, otherwise keep as is.
        """
        return self._ai_parse(raw_text, schema_prompt)
