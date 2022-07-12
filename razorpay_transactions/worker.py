import threading
import json
import time
from datetime import date, timedelta, datetime
from razorpay_transactions.payments_client.payments_client import PaymentsClient
from razorpay_transactions.csv_helper.payments_csv import CSVOperations
from razorpay_transactions.properties import Properties, RunProperties, Mode
from razorpay_transactions.payment_filters.payment_filters import PaymentFilters
from razorpay_transactions.utils.log import ModuleLogger
from razorpay_transactions.errors.exceptions import PaymentReportBaseException

logger = ModuleLogger.get_logger(__name__)


class Worker:
    def __init__(self, mode: Mode, columns_in_summary: list, days_preceding: int = 1,
                 polling_interval: int = 3600,
                 filters: str = None, input_json_path: str = None):
        """
        Init
        :param mode:
        :param columns_in_summary:
        :param days_preceding:
        :param polling_interval:
        :param filters:
        :param input_json_path:
        """
        Properties.initialize(mode=mode, columns_in_summary=columns_in_summary)
        self.payments_client = PaymentsClient(Properties.razorpay_api_credentials)
        self._days_preceding = days_preceding
        self._polling_interval = polling_interval
        if filters:
            self._filters = json.loads(filters)
        else:
            self._filters = []
        self._input_json_file = input_json_path

    def read_run_config_json(self):
        try:
            with open(self._input_json_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(e)
            raise PaymentReportBaseException(e)

    def init_run_config(self):
        """
        Init run config
        Config that is read from json file can be modified before next scheduled run and will be automatically picked up
        :return:
        """
        if self._input_json_file:
            run_config = self.read_run_config_json()
            RunProperties.initialize(days_preceding=run_config.get("days_preceding"),
                                     polling_interval=run_config.get("polling_interval"),
                                     filters=run_config.get("filters"),
                                     )
        else:
            RunProperties.initialize(days_preceding=self._days_preceding, polling_interval=self._polling_interval,
                                     filters=self._filters)

        logger.info("Starting Run with following properties.")
        logger.info(f"Mode: {Properties.mode.value}")
        logger.info(f"Columns_in_summary:{Properties.columns_in_summary}")
        logger.info(f"Polling interval:{RunProperties.polling_interval}")
        logger.info(f"Filters:{RunProperties.filters}")
        logger.info(f"Days preceding:{RunProperties.days_preceding}")

    def __call__(self):
        if Properties.mode == Mode.quick_run:
            self.quick_run()
        elif Properties.mode == Mode.backlog:
            self.backlog()
        elif Properties.mode == Mode.schedule:
            self.schedule()
        else:
            raise PaymentReportBaseException("Mode not supported")

    def unit_worker(self, from_date: date, to_date: date = None):
        """
        Unit worker which aggregates data for the given data
        :param from_date:  date object
        :param to_date: date object
        :return:
        """
        date_str = from_date.strftime('%Y-%m-%d')
        start_epoch = int(datetime.combine(from_date, datetime.min.time()).timestamp())
        option = {"from": start_epoch}
        if to_date:
            to_epoch = int(datetime.combine(to_date, datetime.min.time()).timestamp())
            option.update({"to": to_epoch})
        all_payments = self.payments_client.all_payments(option=option)
        filters = PaymentFilters(RunProperties.filters)
        filtered_payments = filters.filter_results(all_payments)
        csv_ops = CSVOperations(date_string=date_str)
        csv_ops.write_payment_summary_csv(filtered_payments)

    def quick_run(self):
        """
        Runs once for current date
        :return:
        """
        self.init_run_config()
        logger.info("Quick Run starting")
        today_date = date.today()
        self.unit_worker(from_date=today_date)

    def backlog(self):
        """
        Fills backlog from preceding days to yesterday
        :return:
        """
        self.init_run_config()
        logger.info("Backlog worker starting")
        for back_fill in range(RunProperties.days_preceding, 0, -1):
            from_date = date.today() - timedelta(days=back_fill)
            to_date = from_date + timedelta(days=1)
            logger.info(f"Filling backlog for {from_date}")
            self.unit_worker(from_date=from_date, to_date=to_date)

    def scheduler(self):
        """
        Threaded worker
        :return:
        """
        while True:
            self.init_run_config()
            logger.info("Scheduler worker starting")
            self.unit_worker(from_date=date.today())
            time.sleep(RunProperties.polling_interval)

    def schedule(self):
        """
        Updates csvs and sleeps for polling interval
        :return:
        """
        thread = threading.Thread(target=self.scheduler, args=(), daemon=True)
        thread.start()
        thread.join()


if __name__ == "__main__":
    w = Worker(mode=Mode.schedule,
               columns_in_summary=["id", "amount", "status", "method", "order_id", "created_at"],
               input_json_path="/tmp/conf.json"
               )
    w()
