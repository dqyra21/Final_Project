from datetime import datetime
from datetime import date
from django.db.models import Sum
import pandas as pd
from core.models import Loan, CashFlow



def convert_date_format(original_date, input_format="%d/%m/%Y", output_format="%Y-%m-%d"):
    try:
        # Parse the original date with the input format
        parsed_date = datetime.strptime(original_date, input_format)
        # Convert the date to the desired output format
        formatted_date = parsed_date.strftime(output_format)
        return formatted_date
    except ValueError as e:
        # Handle the case where the input date is not in the expected format
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
        # Replace commas with an empty string and convert to float
        float_value = float(value.replace(',', ''))
        return float_value
    except ValueError as e:
        # Handle the case where the conversion fails
        raise ValueError(f'Error converting to float: {e}')


def load_loans_in_database():
    loans = pd.read_excel('data/trades.xlsx')
    for _, loan_data in loans.iterrows():
        loan = Loan(
            loan_id=loan_data['loan_id'],
            investment_date=convert_date_format(loan_data['investment_date']),
            maturity_date=convert_date_format(loan_data['maturity_date']),
            interest_rate=clean_up_percentage(loan_data['interest_rate'])
        )
        loan.save()


def load_cashflows_in_database():
    cashflows = pd.read_excel('data/cash_flows.xlsx')
    for _, cashflow_data in cashflows.iterrows():
        cashflow = CashFlow(
            cashflow_id=cashflow_data['cashflow_id'],
            loan_id=cashflow_data['loan_id'],
            cashflow_date=convert_date_format(cashflow_data['cashflow_date']),
            cashflow_currency=cashflow_data['cashflow_currency'],
            cashflow_type=cashflow_data['cashflow_type'],
            amount=convert_to_float(cashflow_data['amount'])
        )
        cashflow.save()


def calculate_statistics(reference_date, loan_id):
    # Get the Loan object
    loan = Loan.objects.get(loan_id=loan_id)

    # Access related CashFlow objects through the ForeignKey
    cashflows = loan.cashflow_set.filter(cashflow_date__lte=reference_date)

    # Calculate the invested amount at reference date
    invested_amount = cashflows.aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate daily interest rate
    daily_interest_rate = loan.interest_rate / 365

    # Calculate daily interest amount
    daily_interest_amount = invested_amount * daily_interest_rate

    # Calculate passed days
    passed_days = (reference_date - loan.investment_date).days

    # Calculate gross expected interest amount
    gross_expected_interest_amount = daily_interest_amount * passed_days

    # Calculate gross expected amount
    gross_expected_amount = invested_amount + gross_expected_interest_amount

    # Get realized amount at reference date
    realized_amount = cashflows.filter(amount_gt=0, cashflow_datelte=reference_date).aggregate(Sum('amount'))['amount_sum'] or 0

    # Calculate remaining invested amount at reference date
    remaining_invested_amount = invested_amount - realized_amount

    return {
        'gross_expected_amount': gross_expected_amount,
        'realized_amount': realized_amount,
        'remaining_invested_amount': remaining_invested_amount,
    }

# Example usage
reference_date = date(2023, 9, 17)
loan_id = '10229_AA_2231658'

statistics = calculate_statistics(reference_date, loan_id)
print(statistics)