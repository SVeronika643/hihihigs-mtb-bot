import requests
from bs4 import BeautifulSoup

def parse_codewars_profile(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print("Ошибка запроса:", e)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Ищем все названия решённых задач
    # Они обычно находятся в таблице Completed Kata (когда заходишь на /users/USERNAME/completed)
    completed_url = url + "/completed"

    try:
        response = requests.get(completed_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print("Ошибка загрузки completed:", e)
        return []

    task_elements = soup.select(".item-title a")  # Выбираем задачи

    tasks = [task.text.strip() for task in task_elements]
    return list(set(tasks))  # Убираем повторы