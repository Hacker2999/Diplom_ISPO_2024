import logging
import sys


def setup_logging(log_level=logging.INFO, log_file=None):
    """
    Configure logging settings.

    Args:
        log_level (int, optional): The logging level. Defaults to logging.INFO.
        log_file (str, optional): The path to the log file. If None, logs will be output to the console.
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler if log file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


# Example usage:
if __name__ == "__main__":
    setup_logging(log_level=logging.DEBUG, log_file="bot.log")
