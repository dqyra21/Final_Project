# core/admin.py
from django.contrib import admin
from .models import Loan, CashFlow

class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'investment_date', 'maturity_date', 'interest_rate')
    search_fields = ('loan_id',)

class CashFlowAdmin(admin.ModelAdmin):
    list_display = ('cashflow_id', 'loan', 'cashflow_date', 'cashflow_currency', 'cashflow_type', 'amount')
    list_filter = ('cashflow_currency', 'cashflow_type')
    search_fields = ('cashflow_id', 'loan__loan_id')

admin.site.register(Loan, LoanAdmin)
admin.site.register(CashFlow, CashFlowAdmin)
