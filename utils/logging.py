import os
import logging


def setup_logger(fname: str):
    # Создание папки logs
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.FileHandler(f"logs/{fname}.log", mode="w"),
            logging.StreamHandler()
        ]
    )