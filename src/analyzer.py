from datetime import datetime, timedelta
from typing import List, Dict, Any
from src.models import BankStatement, StatementSummary, Transaction, CategoryDetail, FinancialHealth

def parse_date(date_str: str) -> datetime:
    """Try various date formats commonly found in bank statements."""
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d %b %Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    # Fallback if no format matches, return a far future or past or current
    return datetime.now()

def calculate_abb(transactions: List[Transaction]) -> float:
    """
    Calculates the Average Bank Balance (ABB).
    ABB is the average of the closing balance of each day in the statement period.
    """
    if not transactions:
        return 0.0

    # Sort transactions by date
    try:
        sorted_txns = sorted(transactions, key=lambda tx: parse_date(tx.date))
    except Exception:
        return 0.0

    start_date = parse_date(sorted_txns[0].date)
    end_date = parse_date(sorted_txns[-1].date)
    
    daily_balances = {}
    last_balance = 0.0
    
    # Track the last balance seen for each day that has transactions
    for tx in sorted_txns:
        date_obj = parse_date(tx.date).date()
        daily_balances[date_obj] = tx.balance
        last_balance = tx.balance

    # Interpolate balances for days without transactions
    total_balance_sum = 0.0
    current_date = start_date.date()
    running_balance = sorted_txns[0].balance # Start with first txn balance
    
    num_days = (end_date.date() - start_date.date()).days + 1
    
    for i in range(num_days):
        check_date = current_date + timedelta(days=i)
        if check_date in daily_balances:
            running_balance = daily_balances[check_date]
        total_balance_sum += running_balance
        
    return total_balance_sum / num_days if num_days > 0 else 0.0

def calculate_category_metrics(transactions: List[Transaction]) -> Dict[str, CategoryDetail]:
    """Calculates Count, Total, and Average for each category."""
    metrics = {}
    temp_data = {} # category -> list of amounts

    for tx in transactions:
        cat = tx.category
        if cat not in temp_data:
            temp_data[cat] = []
        
        # Use credit if it's income, otherwise debit
        amount = tx.credit if tx.credit > 0 else tx.debit
        temp_data[cat].append(amount)

    for cat, amounts in temp_data.items():
        total = sum(amounts)
        count = len(amounts)
        metrics[cat] = CategoryDetail(
            count=count,
            total_amount=round(total, 2),
            average_amount=round(total / count, 2) if count > 0 else 0.0
        )
    return metrics

def calculate_financial_health(total_debits: float, total_credits: float, metrics: Dict[str, CategoryDetail]) -> FinancialHealth:
    """Calculates industry standard lending ratios."""
    income = metrics.get("Salary", CategoryDetail()).total_amount
    if income == 0: # Fallback to total credits if salary not tagged
        income = total_credits
        
    emis = metrics.get("Rent / EMI", CategoryDetail()).total_amount + metrics.get("Loan Repayment", CategoryDetail()).total_amount
    
    emi_to_income = (emis / income) if income > 0 else 0.0
    savings_ratio = ((total_credits - total_debits) / total_credits) if total_credits > 0 else 0.0
    
    return FinancialHealth(
        emi_to_income_ratio=round(emi_to_income, 2),
        savings_ratio=round(savings_ratio, 2),
        monthly_inflow=round(total_credits, 2),
        monthly_outflow=round(total_debits, 2)
    )

def analyze_statement(statement: BankStatement) -> BankStatement:
    """
    Complete financial analysis: ABB, Categories, and Health Ratios.
    """
    total_debits = sum(t.debit for t in statement.transactions)
    total_credits = sum(t.credit for t in statement.transactions)
    
    abb = calculate_abb(statement.transactions)
    category_metrics = calculate_category_metrics(statement.transactions)
    health = calculate_financial_health(total_debits, total_credits, category_metrics)
    
    statement.summary = StatementSummary(
        average_bank_balance=round(abb, 2),
        total_debits=round(total_debits, 2),
        total_credits=round(total_credits, 2),
        category_metrics=category_metrics,
        financial_health=health
    )
    
    return statement
