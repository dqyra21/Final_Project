from django.db import models


# Create your models here.

class Loan(models.Model):
    loan_id = models.CharField(primary_key=True, max_length=30)
    investment_date = models.DateField()
    maturity_date = models.DateField()
    interest_rate = models.FloatField()


class CashFlow(models.Model):
    cashflow_id = models.CharField(primary_key=True, max_length=30)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    cashflow_date = models.DateField()
    cashflow_currency = models.CharField(max_length=5)
    cashflow_type = models.CharField(max_length=20)
    amount = models.FloatField()
