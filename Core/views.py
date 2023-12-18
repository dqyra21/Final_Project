# api/views.py
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import FileUploadSerializer
from core.utils import load_loans_in_database, load_cashflows_in_database

class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = FileUploadSerializer(data=request.data)

        if file_serializer.is_valid():
            trades_file = file_serializer.validated_data['trades_file']
            cash_flows_file = file_serializer.validated_data['cash_flows_file']

            # Process the uploaded files (parse and save the data to models)
            load_loans_in_database(trades_file)
            load_cashflows_in_database(cash_flows_file)

            return Response({'message': 'Files uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Loan, CashFlow
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from django.db.models import Sum

class RealizedAmountView(APIView):
    def get(self, request, trade_id, reference_date, format=None):
        loan = get_object_or_404(Loan, loan_id=trade_id)
        cashflows = loan.cashflow_set.filter(cashflow_date__lte=reference_date, amount__gt=0)
        realized_amount = cashflows.aggregate(realized_amount=Sum('amount'))['realized_amount'] or 0

        return Response({'realized_amount': realized_amount})

class RemainingInvestedAmountView(APIView):
    def get(self, request, trade_id, reference_date, format=None):
        loan = get_object_or_404(Loan, loan_id=trade_id)
        cashflows = loan.cashflow_set.filter(cashflow_date__lte=reference_date)
        invested_amount = cashflows.aggregate(invested_amount=Sum('amount'))['invested_amount'] or 0
        realized_amount = cashflows.filter(amount__gt=0).aggregate(realized_amount=Sum('amount'))['realized_amount'] or 0
        remaining_invested_amount = invested_amount - realized_amount

        return Response({'remaining_invested_amount': remaining_invested_amount})

class GrossExpectedAmountView(APIView):
    def get(self, request, trade_id, reference_date, format=None):
        loan = get_object_or_404(Loan, loan_id=trade_id)
        cashflows = loan.cashflow_set.filter(cashflow_date__lte=reference_date)
        invested_amount = cashflows.aggregate(invested_amount=Sum('amount'))['invested_amount'] or 0
        daily_interest_rate = loan.interest_rate / 365
        passed_days = (reference_date - loan.investment_date).days
        gross_expected_interest_amount = invested_amount * daily_interest_rate * passed_days
        gross_expected_amount = invested_amount + gross_expected_interest_amount

        return Response({'gross_expected_amount': gross_expected_amount})

class ClosingDateView(APIView):
    def get(self, request, trade_id, format=None):
        loan = get_object_or_404(Loan, loan_id=trade_id)
        closing_date = loan.maturity_date

        return Response({'closing_date': closing_date})
