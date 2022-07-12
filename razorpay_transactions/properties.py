import os
from collections import namedtuple
from enum import Enum

razorpay_auth = namedtuple("auth", ["key_id", "key_secret"])


class Mode(Enum):
    quick_run = "quick_run"
    backlog = "backlog"
    schedule = "schedule"


class Properties:
    base_directory = os.path.expanduser('~')
    columns_in_summary = None
    razorpay_api_credentials = None
    mode = None

    @classmethod
    def initialize(cls, mode: Mode, columns_in_summary: list):
        cls.mode = mode
        cls.columns_in_summary = columns_in_summary
        cls.razorpay_api_credentials = razorpay_auth(os.environ["RAZORPAY_KEY_ID"], os.environ["RAZORPAY_KEY_SECRET"])


class RunProperties:
    days_preceding = None
    polling_interval = None
    filters = None

    @classmethod
    def initialize(cls, days_preceding, polling_interval, filters):
        cls.days_preceding = days_preceding
        cls.polling_interval = polling_interval
        cls.filters = filters
