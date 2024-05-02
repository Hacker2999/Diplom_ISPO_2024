import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Set the logger level to DEBUG

def setup_logging(log_level=logging.INFO, log_file=None):
    # Создание форматтера
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - '
                                  '%(message)s')

    # Создание обработчика для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)  # Set the console handler level to log_level
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Создание обработчика для файла, если указан log_file
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)  # Set the file handler level to log_level
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)