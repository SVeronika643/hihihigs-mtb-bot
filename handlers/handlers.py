from aiogram import types, Router
from aiogram.filters import Command, CommandStart
from .keyboard import keyboard  # Импорт клавиатуры
from aiogram.types import Message
import logging
from aiogram import types, Router, filters, F
from sqlalchemy import select
from db import async_session, User
from .keyboard import keyboard_start
from sqlalchemy import insert
from utils.parser import parse_codewars_profile
import re

# информация о статусе
status_string: str = """
UserId: {}
UserName: {}
"""
# Создаём экземпляр Router
router = Router()

@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    async with async_session() as session:
        query = select(User).where(message.from_user.id == User.user_id)
        result = await session.execute(query)
        if result.scalars().all():
            info = "Чтобы продолжить, вызовите команду /status"
            await message.answer(info)
        else:
            await  message.answer("Выберите роль", reply_markup=keyboard_start)
    logging.info(f"user {message.from_user.id} starts bot ")

@router.message(Command("status")) # /status
async def command_status_handler(message: Message) -> None:
    async with async_session() as session:
        query = select(User).where(message.from_user.id == User.user_id)
        result = await session.execute(query)
        user = result.scalar()
        if user.tutorcode:
            info = status_string + "Код преподавателя: {}"
            info = info.format(user.user_id, user.username, user.tutorcode)
        if user.subscribe:
            code = str(user.subscribe)
            info = status_string + "Преподаватель: {}"
            query = select(User).where(code == User.tutorcode)
            result = await session.execute(query)
            tutor = result.scalar()
            try:
                info = info.format(user.user_id, user.username, tutor.username)
            except:
                info = info.format(user.user_id, user.username)
        await message.answer(info)
    logging.info(f"user {message.from_user.id} gets status ")

    @router.message(F.text.startswith("tutorcode-"))
    async def start_student(message):
        async with async_session() as session:
            new_user = {
                "user_id": message.from_user.id,
                "username": message.from_user.username,
                "subscribe": str(message.text.split("-")[1])
            }
            insert_query = insert(User).values(new_user)
            await session.execute(insert_query)
            await session.commit()
            await message.answer("Пользователь добавлен!")
            logging.info(f"Пользователь {message.from_user.username} добавлен в базу данных с ролью слушатель!")

codewars_pattern = re.compile(r'^https?://(www\.)?codewars\.com/users/[^\s]+/?$')

@router.message(Command("load"))
async def load_profiles_handler(message: Message):
    text = message.text.strip()

    # Разделим по пробелу, чтобы отделить команду от аргументов
    parts = text.split(" ", 1)
    if len(parts) < 2:
        await message.answer("Пожалуйста, отправьте ссылку(-и) после команды /load через запятую.")
        return

    links_raw = parts[1].strip()
    links = [link.strip() for link in links_raw.split(",") if codewars_pattern.match(link.strip())]

    if not links:
        await message.answer("Пришли ссылку в формате https://www.codewars.com/users/...")
        logging.info(f"user {message.from_user.id} прислал невалидные ссылки: {links_raw}")
        return

    results = []

    for link in links:
        tasks = parse_codewars_profile(link)
        if tasks:
            results.append("Задачи загружены для " + link + ":\n" + "\n".join(tasks))
        else:
            results.append(f"Не удалось получить задачи по ссылке: {link}")

    await message.answer("\n\n".join(results))
    logging.info(f"user {message.from_user.id} загрузил ссылки: {links}")

from utils.parser import parse_codewars_profile  # если функция парсинга лежит в отдельном модуле
from sqlalchemy import select
from db import async_session, User
@router.message(Command("getres"))
async def get_results_handler(message: Message):
     all_tasks = set()

     async with async_session() as session:
         # Получаем преподавателя
         query = select(User).where(User.user_id == message.from_user.id)
         result = await session.execute(query)
         tutor = result.scalar()

         if not tutor or not tutor.tutorcode:
             await message.answer("Вы не являетесь преподавателем.")
             return

         # Получаем всех студентов, подписанных на этого преподавателя
         query = select(User).where(User.subscribe == str(tutor.tutorcode))
         result = await session.execute(query)
         students = result.scalars().all()

         if not students:
             await message.answer("У вас пока нет студентов.")
             return

         for student in students:
             if not student.username:
                 continue
             # Собираем ссылку на профиль студента
             profile_url = f"https://www.codewars.com/users/{student.username.replace(' ', '%20')}"
             tasks = parse_codewars_profile(profile_url)
             all_tasks.update(tasks)

         if all_tasks:
             sorted_tasks = sorted(all_tasks)
             await message.answer("Пройденные задачи:\n\n" + "\n".join(sorted_tasks))
         else:
            await message.answer("Не удалось получить задачи студентов.")


@router.message(Command("checked"))
async def notify_students_handler(message: Message):
    async with async_session() as session:
        # Получаем преподавателя по user_id
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        tutor = result.scalar()

        if not tutor or not tutor.tutorcode:
            await message.answer("Вы не являетесь преподавателем.")
            return

        # Получаем студентов, подписанных на tutorcode преподавателя
        query = select(User).where(User.subscribe == str(tutor.tutorcode))
        result = await session.execute(query)
        students = result.scalars().all()

        if not students:
            await message.answer("У вас пока нет студентов.")
            return

        count = 0
        for student in students:
            try:
                await message.bot.send_message(student.user_id, "Ваши задачи проверены преподавателем.")
                count += 1
            except Exception as e:
                logging.warning(f"Не удалось отправить сообщение студенту {student.user_id}: {e}")

        await message.answer(f"Отправлено уведомлений: {count}")
        logging.info(f"Преподаватель {message.from_user.id} отправил уведомления {count} студентам")

@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Список доступных команд:\n/start — запустить бота\n/status — проверить статус\n/help — помощь\n/menu — открыть меню")

@router.message(Command("menu"))
async def menu_command(message: types.Message):
    await message.answer("Выберите пункт меню:", reply_markup=keyboard())

@router.message()
async def echo_handler(message: Message) -> None:

    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
        logging.info(f"user {message.from_user.id} leaves unhandled message")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
        logging.info(f"user {message.from_user.id} leaves unhandled message unsuccessfully")
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
        logging.info(f"user {message.from_user.id} leaves unhandled message unsuccessfully")

