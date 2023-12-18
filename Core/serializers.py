# api/serializers.py
from rest_framework import serializers
from .models import Loan, CashFlow

class FileUploadSerializer(serializers.Serializer):
    trades_file = serializers.FileField()
    cash_flows_file = serializers.FileField()


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class CashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = '__all__'
