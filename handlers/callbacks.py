from aiogram import types, Router, F
import logging
from aiogram.types import CallbackQuery
from sqlalchemy import insert, select
from db import async_session, User
import string
from random import choices

router = Router()

@router.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer('пример текста')
    logging.info(f"user {callback.from_user.id} gets random value ")

@router.callback_query(F.data == "button_tutor")
async def handle_tutor_role(callback: CallbackQuery):
    from db import async_session, User
    from sqlalchemy import insert

    async with async_session() as session:
        tutorcode = str(callback.from_user.id)[-6:]  # последние 6 цифр ID — как код
        new_user = {
            "user_id": callback.from_user.id,
            "username": callback.from_user.username,
            "tutorcode": tutorcode
        }
        insert_query = insert(User).values(new_user)
        await session.execute(insert_query)
        await session.commit()
        await callback.message.edit_text(f"Вы зарегистрированы как преподаватель.\nВаш код: `{tutorcode}`", parse_mode="Markdown")

@router.callback_query(F.data == "button_student")
async def callback_insert_tutorcode(callback: CallbackQuery):
    async with async_session() as session:
        # Проверяем, существует ли уже пользователь
        result = await session.execute(
            select(User).where(User.user_id == callback.from_user.id)
        )
        user = result.scalar()

        if not user:
            # Если не существует — добавляем
            new_user = {
                "user_id": callback.from_user.id,
                "username": callback.from_user.username,
            }
            insert_query = insert(User).values(new_user)
            await session.execute(insert_query)
            await session.commit()
            logging.info(f"Пользователь {callback.from_user.username} добавлен в базу как слушатель!")
        else:
            logging.info(f"Пользователь {callback.from_user.username} уже есть в базе.")

    # Запросим код преподавателя в любом случае
    await callback.message.answer(
        "Введите код преподавателя в формате:\n`tutorcode-XXXXXX`",
        parse_mode="Markdown"
    )
