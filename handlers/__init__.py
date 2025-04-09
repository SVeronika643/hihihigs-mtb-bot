# Файл __init__.py.py позволяет обращаться к папке как к модулю
# и импортировать из него содержимое


from .handlers import router
from .callbacks import send_random_value

__all__ = ['router', 'send_random_value']