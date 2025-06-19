from .db import async_session
import requests
from bs4 import BeautifulSoup

class CodewarsLogic:
    def __init__(self):
        pass

    def __str__(self):
        return "CodewarsLogic"

    async def parse_and_store(self, profile_url: str):
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(profile_url + "/completed", headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        tasks = [a.text.strip() for a in soup.select(".item-title a")]

        async with async_session() as session:
            # Пример: сохраняем задачи в вашу таблицу tasks в БД
            # session.add(YourModel(profile=profile_url, tasks=','.join(tasks)))
            await session.commit()

        return tasks

    async def notify_students(self, tutor_id: int, send_fn):
        from sqlalchemy import select
        from .db import async_session
        from handlers.handlers import User  # или импорт вашей модели

        async with async_session() as session:
            result = await session.execute(select(User).where(User.tutorcode == tutor_id))
            students = result.scalars().all()

        for student in students:
            await send_fn(student.user_id, "Ваши задачи проверены преподавателем.")