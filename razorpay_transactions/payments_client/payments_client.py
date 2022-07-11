import razorpay
from typing import List
from razorpay_transactions.properties import razorpay_auth
from razorpay_transactions.errors.exceptions import PaymentReportBaseException
from razorpay_transactions.utils.log import ModuleLogger
from razorpay_transactions.payment_dataclasses.rpay_payments import Payment

logger = ModuleLogger.get_logger(__name__)


class PaymentsClient:
    def __init__(self, credentials: razorpay_auth):
        self.client = razorpay.Client(auth=(credentials.key_id, credentials.key_secret))

    def __all_payments(self, option: dict = None) -> List[dict]:
        """
        Raw dict response from API
        :param option:
        :return:
        """
        if not option:
            option = {}
        option["count"] = 100

        payments = []

        batch = self.client.payment.all(option)
        while batch["items"]:
            payments.extend(batch["items"])
            option["skip"] = len(payments)
            batch = self.client.payment.all(option)

        return payments

    def all_payments(self, option: dict = None) -> List[Payment]:
        """
        Dataclass mapped response
        :param option:
        :return:
        """
        try:
            payments = self.__all_payments(option=option)
            payments_list = [Payment(**payment) for payment in payments]
            payments_list.sort(key=lambda p: p.created_at_epoch, reverse=False)
            return payments_list
        except Exception as e:
            logger.error(e)
            raise PaymentReportBaseException(e)


if __name__ == "__main__":
    pass
