import os
from dotenv import load_dotenv

def load_config():
    # Загрузка переменных окружения
    load_dotenv()
    # Получение токена из окружения
    TOKEN = os.environ.get('TOKEN')
    return TOKEN

