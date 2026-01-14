from src.parsers.base import BaseParser
from src.models import BankStatement

class AxisParser(BaseParser):
    def __init__(self):
        super().__init__(bank_name="AXIS")

    def parse(self, raw_text: str) -> BankStatement:
        schema_prompt = """
        Axis Bank statements usually have columns: Date, Particulars, Chq/Ref No, Withdrawal (Dr), Deposit (Cr), Balance.
        Map 'Withdrawal (Dr)' to 'debit' and 'Deposit (Cr)' to 'credit'.
        Extract the account number and holder name from the top section.
        """
        return self._ai_parse(raw_text, schema_prompt)
