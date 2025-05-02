from aiogram.types import CallbackQuery
import random
import logging
from aiogram import F,Router

router = Router()

@router.callback_query(F.data == "button")
async def send_random_value(callback_query: CallbackQuery):

    # Генерируем случайное число
    random_number = random.randint(1, 100)

    # Отправляем сообщение с результатом
    await callback_query.message.answer(f"Случайное значение: {random_number}")

    logging.info(f"user {callback_query.from_user.id} generates random int")
