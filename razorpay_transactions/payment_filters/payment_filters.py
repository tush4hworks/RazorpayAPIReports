import itertools
import copy
from collections import namedtuple

from typing import List, Dict
from razorpay_transactions.utils.log import ModuleLogger
from razorpay_transactions.payment_dataclasses.razorpay_payments import Payment
from razorpay_transactions.errors.exceptions import PaymentReportBaseException

logger = ModuleLogger.get_logger(__name__)

filter_spec = namedtuple("filter_spec", ["filter_type", "filter_column", "filter_value"])


class PaymentFilters:

    def __init__(self, filters: List[List[Dict]]):
        self.filter_blocks = [[filter_spec(**spec) for spec in item] for item in filters]

    @staticmethod
    def equals(filter_column, filter_value):
        return lambda x: getattr(x, filter_column) == filter_value

    @staticmethod
    def not_equals(filter_column, filter_value):
        return lambda x: getattr(x, filter_column) != filter_value

    @staticmethod
    def is_in(filter_column, filter_value):
        return lambda x: getattr(x, filter_column) in filter_value

    @staticmethod
    def is_not_in(filter_column, filter_value):
        return lambda x: getattr(x, filter_column) not in filter_value

    @staticmethod
    def greater_than(filter_column, filter_value):
        return lambda x: getattr(x, filter_column) > filter_value

    @staticmethod
    def less_than(filter_column, filter_value):
        return lambda x: getattr(x, filter_column) < filter_value

    def or_items(self, payments: List[Payment], conditions: List[filter_spec]):
        return list(set(itertools.chain.from_iterable(
            filter(getattr(self, condition.filter_type)(condition.filter_column, condition.filter_value), payments)
            for
            condition in conditions)))

    def filter_results(self, payments: List[Payment]):
        # Create copy so that original payments list is unmodified
        filtered_payments = copy.copy(payments)
        try:
            for filter_block in self.filter_blocks:
                filtered_payments = self.or_items(filtered_payments, filter_block)
            logger.info(filtered_payments)
            return filtered_payments
        except Exception as e:
            logger.error(e)
            raise PaymentReportBaseException(e)


if __name__ == "__main__":
    pf = PaymentFilters([
        [
            {
                "filter_type": "equals",
                "filter_column": "status",
                "filter_value": "failed"
            }
        ]
    ])
