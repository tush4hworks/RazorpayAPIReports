import logging
import os
from razorpay_transactions.properties import Properties


class ModuleLogger:
    @staticmethod
    def get_logger(name, log_level=logging.INFO) -> logging.Logger:
        logger = logging.getLogger(name)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console = logging.StreamHandler()
        console.setLevel(log_level)
        console.setFormatter(formatter)
        logger.addHandler(console)

        file_handler = logging.FileHandler(filename=os.path.join(Properties.base_directory, 'app.log'))
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger
