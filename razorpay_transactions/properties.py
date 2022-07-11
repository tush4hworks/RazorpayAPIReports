import os
from collections import namedtuple
from datetime import datetime, date, timedelta
razorpay_auth = namedtuple("auth", ["key_id", "key_secret"])


class Properties:
    base_directory = os.path.expanduser('~')
    polling_interval = None
    columns_in_summary = None
    filters = None
    today_date = None
    today_start_epoch = None
    razorpay_api_credentials = None

    @classmethod
    def initialize(cls,  polling_interval, columns_in_summary, filters=None):
        cls.polling_interval = polling_interval
        cls.columns_in_summary = columns_in_summary
        cls.filters = filters
        cls.razorpay_api_credentials = razorpay_auth(os.environ["RAZORPAY_KEY_ID"], os.environ["RAZORPAY_KEY_SECRET"])
        # TODO uncomment
        today_date = date.today() - timedelta(days=10)
        cls.today_date = today_date.strftime('%Y-%m-%d')
        cls.today_start_epoch = int(datetime.combine(today_date, datetime.min.time()).timestamp())
