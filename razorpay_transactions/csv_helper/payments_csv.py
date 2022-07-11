import os

from dataclass_csv import DataclassReader, DataclassWriter
from typing import List
from razorpay_transactions.properties import Properties
from razorpay_transactions.payment_dataclasses.razorpay_payments import PaymentSummaryDataclassHelper, Payment
from razorpay_transactions.utils.log import ModuleLogger

logger = ModuleLogger.get_logger(__name__)


class CSVOperations:

    def __init__(self):
        self.csv_path = os.path.join(Properties.base_directory, f'{Properties.today_date}.csv')
        PaymentSummaryDataclassHelper.initialize_payment_summary_data_class(Properties.columns_in_summary)

    def read_payment_summary_csv(self):
        payment_summaries = []

        if not os.path.isfile(self.csv_path):
            logger.warning("File not found!.")
            return payment_summaries

        with open(self.csv_path, 'r') as payment_csv:
            reader = DataclassReader(payment_csv, PaymentSummaryDataclassHelper.PaymentSummary)
            for row in reader:
                payment_summaries.append(row)
        return payment_summaries

    def write_payment_summary_csv(self, payments: List[Payment] = None):
        """
        Theoretically one could look at the last added timestamp in the csv file and fetch new records from thereon
        However it could lead to few records being missed if they come between opening the file and subsequently
        fetching data and writing it
        Therefore we need to compare it with existing records for de-duplication and write missing entries
        Or we could just overwrite entire file
        :param payments:
        :return:
        """
        if not payments:
            payments = []
        # Select fields to write
        payment_summaries = [PaymentSummaryDataclassHelper.map_attributes(payment) for payment in payments]

        # De-duplicate
        # existing_rows = self.read_payment_summary_csv()
        # payment_summaries = [payment for payment in payment_summaries if payment not in existing_rows]

        with open(self.csv_path, 'w') as f:
            w = DataclassWriter(f, payment_summaries, PaymentSummaryDataclassHelper.PaymentSummary)
            w.write()
