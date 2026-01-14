from src.parsers.base import BaseParser
from src.models import BankStatement

class SBIParser(BaseParser):
    def __init__(self):
        super().__init__(bank_name="SBI")

    def parse(self, raw_text: str) -> BankStatement:
        schema_prompt = """
        SBI statements usually have 'Txn Date', 'Value Date', 'Description', 'Ref No./Cheque No.', 'Debit', 'Credit', 'Balance'.
        Ensure the 'branch' or 'ifsc' is captured from the top section.
        Transactions should be listed chronologically.
        """
        return self._ai_parse(raw_text, schema_prompt)
