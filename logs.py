import logging
import datetime
import os

# Создаем логгер
logger = logging.getLogger('aiogram_logger')

# Установка уровня логгирования
logger.setLevel(logging.DEBUG)

# Создаем форматтер для логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Получаем путь к директории скрипта
script_dir = os.path.dirname(__file__)

# Создаем имя файла логов с текущим временем
log_dir = os.path.join(script_dir, 'logs')
log_file_name = os.path.join(log_dir, f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# Создаем файловый хендлер для логов
file_handler = logging.FileHandler(log_file_name)
file_handler.setFormatter(formatter)

# Добавляем хендлер к логгеру
logger.addHandler(file_handler)

# Теперь можно использовать логгер
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')