# api/urls.py
from django.urls import path
from .views import (
    LoanListCreateView,
    CashFlowListCreateView,
    RealizedAmountView,
    FileUploadView,
    RemainingInvestedAmountView,
    GrossExpectedAmountView,
    ClosingDateView
)

urlpatterns = [
    path('loans/', LoanListCreateView.as_view(), name='loan-list-create'),
    path('cashflows/', CashFlowListCreateView.as_view(), name='cashflow-list-create'),
    path('realized-amount/<str:trade_id>/<str:reference_date>/', RealizedAmountView.as_view(), name='realized-amount'),
    path('file-upload/', FileUploadView.as_view(), name='file-upload'),
    path('remaining-invested-amount/<str:trade_id>/<str:reference_date>/', RemainingInvestedAmountView.as_view(), name='remaining-invested-amount'),
    path('gross-expected-amount/<str:trade_id>/<str:reference_date>/', GrossExpectedAmountView.as_view(), name='gross-expected-amount'),
    path('closing-date/<str:trade_id>/', ClosingDateView.as_view(), name='closing-date'),
    # Add other endpoints here
]
