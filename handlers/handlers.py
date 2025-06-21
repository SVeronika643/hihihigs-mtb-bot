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
import json
from sqlalchemy import update
from uuid import uuid4



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
        # Ищем пользователя в базе
        query = select(User).where(User.user_id == message.from_user.id)
        result = await session.execute(query)
        user = result.scalar()

        if user:
            if user.subscribe:
                await message.answer("Вы уже зарегистрированы и подписаны на преподавателя.\nМожете использовать команду /status.")
            else:
                await message.answer("Введите код преподавателя (в формате tutorcode-XXXXXX):")
        else:
            await message.answer("Выберите роль:", reply_markup=keyboard_start)

    (logging.info(f"user {message.from_user.id} starts bot")

@router.message(Command("status"))) # /status
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
async def start_student(message: Message):
    logging.info(f"Получено сообщение с кодом: {message.text}")
    try:
        code = message.text.split("-")[1].strip()

        async with async_session() as session:
            # Проверка кода преподавателя
            query = select(User).where(User.tutorcode == code)
            result = await session.execute(query)
            tutor = result.scalar()

            if not tutor:
                await message.answer("Преподаватель с таким кодом не найден.")
                return

            # Проверка, есть ли пользователь
            query = select(User).where(User.user_id == message.from_user.id)
            result = await session.execute(query)
            student = result.scalar()

            if student:
                student.subscribe = code
                await session.commit()
                await message.answer("Вы подписались на преподавателя!")
                logging.info(f"{message.from_user.username} подписался на преподавателя {tutor.username}")
            else:
                new_user = {
                    "user_id": message.from_user.id,
                    "username": message.from_user.username,
                    "subscribe": code
                }
                insert_query = insert(User).values(new_user)
                await session.execute(insert_query)
                await session.commit()
                await message.answer("Вы зарегистрированы как слушатель!")
                logging.info(
                    f"{message.from_user.username} зарегистрирован и подписался на преподавателя {tutor.username}")

    except Exception as e:
        logging.exception("Ошибка при регистрации студента")
        await message.answer("Произошла ошибка при обработке вашего кода. Попробуйте ещё раз.")

codewars_pattern = re.compile(r'^https?://(www\.)?codewars\.com/users/[^\s]+/?$')

@router.message(Command("load"))
async def load_profiles_handler(message: Message):
    import json

    text = message.text.strip()
    parts = text.split(" ", 1)
    if len(parts) < 2:
        await message.answer("Пожалуйста, отправьте ссылку(-и) после команды /load через запятую.")
        return

    links_raw = parts[1].strip()
    links = [link.strip() for link in links_raw.split(",") if codewars_pattern.match(link.strip())]

    if not links:
        await message.answer("Пришлите ссылки в формате https://www.codewars.com/users/...")
        return

    results = []

    async with async_session() as session:
        # Получаем пользователя из базы
        result = await session.execute(select(User).where(User.user_id == message.from_user.id))
        user = result.scalar()

        if user is None:
            await message.answer("Пользователь не найден в базе.")
            return

        # Считываем существующие логины из extra
        try:
            existing_extra = json.loads(user.extra) if user.extra else {}
            existing_usernames = set(existing_extra.get("codewars_usernames", []))
        except Exception:
            existing_usernames = set()

        for link in links:
            # Парсим задачи, чтобы проверить доступность профиля
            tasks = parse_codewars_profile(link)
            if tasks:
                username_from_url = link.split("/")[-1].replace('%20', ' ')
                existing_usernames.add(username_from_url)
                results.append(f"Задачи загружены для {link}:\n" + "\n".join(tasks))
            else:
                results.append(f"Не удалось получить задачи по ссылке: {link}")

        # Сохраняем обновленный список аккаунтов в extra
        new_extra = {"codewars_usernames": list(existing_usernames)}
        stmt = (
            update(User)
            .where(User.user_id == message.from_user.id)
            .values(extra=json.dumps(new_extra))
        )
        await session.execute(stmt)
        await session.commit()

    await message.answer("\n\n".join(results))

from utils.parser import parse_codewars_profile  # если функция парсинга лежит в отдельном модуле
from sqlalchemy import select
from db import async_session, User
@router.message(Command("getres"))
async def get_results_handler(message: Message):
    import json
    all_tasks = set()

    async with async_session() as session:
        # Получаем преподавателя
        result = await session.execute(select(User).where(User.user_id == message.from_user.id))
        tutor = result.scalar()

        if not tutor or not tutor.tutorcode:
            await message.answer("Вы не являетесь преподавателем.")
            return

        # Получаем всех студентов, подписанных на этого преподавателя
        result = await session.execute(select(User).where(User.subscribe == str(tutor.tutorcode)))
        students = result.scalars().all()

        if not students:
            await message.answer("У вас пока нет студентов.")
            return

        for student in students:
            print(f"[DEBUG] Студент: id={student.user_id}, telegram_username={student.username!r}")

            if not student.extra:
                print("[DEBUG] У студента нет поля extra.")
                continue

            try:
                extra_data = json.loads(student.extra)
            except Exception as e:
                print(f"[DEBUG] Ошибка разбора extra: {e}")
                continue

            # Получаем список логинов Codewars, если есть
            usernames = []
            if "codewars_usernames" in extra_data:
                usernames = extra_data["codewars_usernames"]
            elif "codewars_username" in extra_data:
                usernames = [extra_data["codewars_username"]]

            if not usernames:
                print("[DEBUG] Логины Codewars не найдены у студента.")
                continue

            for codewars_username in usernames:
                profile_url = f"https://www.codewars.com/users/{codewars_username.replace(' ', '%20')}"
                print(f"[DEBUG] Парсим: {profile_url}")
                tasks = parse_codewars_profile(profile_url)

                if not tasks:
                    print(f"[DEBUG] Не удалось получить задачи по ссылке: {profile_url}")
                    continue

                print(f"[DEBUG] Получено задач: {len(tasks)}")
                all_tasks.update(tasks)

        if all_tasks:
            sorted_tasks = sorted(all_tasks)
            await message.answer("Пройденные задачи студентами:\n\n" + "\n".join(sorted_tasks))
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



