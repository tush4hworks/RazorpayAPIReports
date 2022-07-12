import logging
import os
from razorpay_transactions.properties import Properties


class ModuleLogger:
    logger = None

    @staticmethod
    def get_logger(name) -> logging.Logger:
        if ModuleLogger.logger:
            return ModuleLogger.logger

        logger = logging.getLogger(name)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

        file_handler = logging.FileHandler(filename=os.path.join(Properties.base_directory, 'app.log'))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.setLevel(logging.INFO)

        ModuleLogger.logger = logger

        return logger
