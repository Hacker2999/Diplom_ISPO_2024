import logging
import datetime
import os

# логгер
logger = logging.getLogger('aiogram_logger')

# Установка уровня логгирования
logger.setLevel(logging.DEBUG)

# форматтер для логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# путь к директории скрипта
script_dir = os.path.dirname(__file__)

# имя файла логов с текущим временем
log_dir = os.path.join(script_dir, 'logs')
log_file_name = os.path.join(log_dir, f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# файловый хендлер для логов
file_handler = logging.FileHandler(log_file_name)
file_handler.setFormatter(formatter)

# хендлер к логгеру
logger.addHandler(file_handler)
