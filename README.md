# Final_Project

## API USAGE 

-List and Create Loans:

-GET /api/loans/

-POST /api/loans/

-List and Create Cash Flows:

-GET /api/cashflows/

-POST /api/cashflows/

-Upload Files (trades.xlsx, cash_flows.xlsx):

-POST /api/file-upload/

-Get Realized Amount for a Trade in Reference Date:

-GET /api/realized-amount/<str:trade_id>/<str:reference_date>/

-Get Remaining Invested Amount for a Trade in Reference Date:

-GET /api/remaining-invested-amount/<str:trade_id>/<str:reference_date>/

-Get Gross Expected Amount for a Trade in Reference Date:

-GET /api/gross-expected-amount/<str:trade_id>/<str:reference_date>/

-Get Closing Date for a Trade:

-GET /api/closing-date/<str:trade_id>/

