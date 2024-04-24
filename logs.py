import logging
import sys


def setup_logging(log_level=logging.INFO, log_file=None):
    """
    Настройка параметров логирования.

    Args:
        log_level (int, optional): Уровень логирования. По умолчанию logging.INFO.
        log_file (str, optional): Путь к файлу логов. Если None, логи будут выводиться в консоль.
    """
    # Создание логгера
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Создание форматтера
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Создание обработчика для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Создание обработчика для файла, если указан log_file
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


# Пример использования:
if __name__ == "__main__":
    setup_logging(log_level=logging.DEBUG, log_file="bot.log")
