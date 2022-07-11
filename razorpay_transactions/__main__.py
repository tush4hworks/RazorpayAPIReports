from razorpay_transactions.payments_client.payments_client import PaymentsClient
from razorpay_transactions.csv_helper.payments_csv import CSVOperations
from razorpay_transactions.properties import Properties
from razorpay_transactions.properties import razorpay_auth

if __name__ == "__main__":
    Properties.initialize(polling_interval=60,
                          columns_in_summary=["id", "amount", "status", "method", "order_id", "created_at"],
                          filters=None)
    creds = Properties.razorpay_api_credentials
    c = PaymentsClient(creds)
    x = c.all_payments(option={"from": Properties.today_start_epoch})
    csvo = CSVOperations()
    csvo.write_payment_summary_csv(x)
