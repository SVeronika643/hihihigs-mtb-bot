from aiogram import types, Router, F
import logging
from aiogram.types import CallbackQuery
from sqlalchemy import insert
from db import async_session, User
import string
from random import choices

router = Router()

@router.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer('пример текста')
    logging.info(f"user {callback.from_user.id} gets random value ")

@router.callback_query(F.data == "button_tutor")
async def callback_start_tutor(callback: CallbackQuery):
    async with async_session() as session:
        chars = string.ascii_letters + string.digits + string.punctuation
        new_user = {
            "user_id": callback.from_user.id,
            "username": callback.from_user.username,
            "tutorcode": "".join(choices(chars, k=6))
        }
        insert_query = insert(User).values(new_user)
        await session.execute(insert_query)
        await session.commit()
        await callback.message.answer("Пользователь добавлен!")
        logging.info(f"Пользователь {callback.from_user.username} добавлен в базу данных с ролью преподаватель!")

@router.callback_query(F.data == "button_student")
async def callback_insert_tutorcode(callback: CallbackQuery):
    await callback.message.answer("Введите код преподавателя (в формате tutorcode-CODE):")
