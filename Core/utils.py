# core/utils.py
import pandas as pd
from datetime import datetime
from .models import Loan, CashFlow


def convert_date_format(original_date, input_format="%d/%m/%Y", output_format="%Y-%m-%d"):
    try:
        parsed_date = datetime.strptime(original_date, input_format)
        formatted_date = parsed_date.strftime(output_format)
        return formatted_date
    except ValueError as e:
        raise ValueError(f'Invalid date format: {e}')


def clean_up_percentage(value):
    if value.isnumeric():
        return float(value)
    elif value.endswith("%"):
        return float(value[:-1]) / 100


def clean_up_amount(amount):
    if amount.isnumeric():
        return amount
    else:
        return float(amount)


def convert_to_float(value):
    try:
        float_value = float(value.replace(',', ''))
        return float_value
    except ValueError as e:
        raise ValueError(f'Error converting to float: {e}')


def load_loans_in_database(file):
    loans = pd.read_excel(file)
    for _, loan_data in loans.iterrows():
        loan = Loan(
            loan_id=loan_data['loan_id'],
            investment_date=convert_date_format(loan_data['investment_date']),
            maturity_date=convert_date_format(loan_data['maturity_date']),
            interest_rate=clean_up_percentage(loan_data['interest_rate'])
        )
        loan.save()


def load_cashflows_in_database(file):
    cashflows = pd.read_excel(file)
    for _, cashflow_data in cashflows.iterrows():
        loan_id = cashflow_data['loan_id']
        loan = Loan.objects.get(loan_id=loan_id)
        cashflow = CashFlow(cashflow_id=cashflow_data['cashflow_id'],
            loan=loan,
            cashflow_date=convert_date_format(cashflow_data['cashflow_date']),
            cashflow_currency=cashflow_data['cashflow_currency'],
            cashflow_type=cashflow_data['cashflow_type'],
            amount=convert_to_float(cashflow_data['amount'])
        )
        cashflow.save()

