import os
import logging


def setup_logger(fname: str):
<<<<<<< HEAD
    # Создание папки logs
=======
    # Создание папки logs, если её нет
>>>>>>> 3019c2d (handlers, keyboard, main)
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.FileHandler(f"logs/{fname}.log", mode="w"),
            logging.StreamHandler()
        ]
<<<<<<< HEAD
    )
=======
    )
>>>>>>> 3019c2d (handlers, keyboard, main)
