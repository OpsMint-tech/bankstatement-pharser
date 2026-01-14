from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Transaction(BaseModel):
    date: str = Field(..., description="Date of the transaction")
    description: str = Field(..., description="Description of the transaction")
    debit: float = Field(default=0.0, description="Amount debited")
    credit: float = Field(default=0.0, description="Amount credited")
    balance: float = Field(..., description="Balance after the transaction")
    category: str = Field("Others", description="Main category (Salary, Rent, etc.)")
    payment_mode: str = Field("Others", description="More specific type (P2M, P2P, EMI, RTGS, etc.)")

class CategoryDetail(BaseModel):
    count: int = 0
    total_amount: float = 0.0
    average_amount: float = 0.0

class FinancialHealth(BaseModel):
    emi_to_income_ratio: float = 0.0  # (Total EMIs / Total Income)
    savings_ratio: float = 0.0        # (Income - Expenses) / Income
    monthly_inflow: float = 0.0
    monthly_outflow: float = 0.0

class StatementSummary(BaseModel):
    average_bank_balance: float = Field(0.0, description="ABB")
    total_debits: float = 0.0
    total_credits: float = 0.0
    category_metrics: Dict[str, CategoryDetail] = Field(default_factory=dict)
    financial_health: Optional[FinancialHealth] = None

class BankStatement(BaseModel):
    bank_name: str = Field(..., description="Name of the bank")
    account_holder: str = Field(..., description="Name of the account holder")
    account_number: str = Field(..., description="Masked account number")
    ifsc: Optional[str] = Field(None, description="IFSC code or Branch info")
    transactions: List[Transaction] = Field(default_factory=list, description="List of transactions")
    summary: Optional[StatementSummary] = Field(None)
