from sqlalchemy import create_engine  # Импортируем функцию для создания движка базы данных
from sqlalchemy.ext.declarative import declarative_base  # Импортируем базовый класс для моделей
from sqlalchemy.orm import sessionmaker  # Импортируем функцию для создания сессий
from sqlalchemy.pool import NullPool  # Импортируем класс для управления подключением
import os  # Импортируем модуль для работы с операционной системой
from dotenv import load_dotenv  # Импортируем функцию для загрузки переменных окружения

load_dotenv()  # Загружаем переменные окружения из .env файла

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")  # Получаем URL базы данных из переменной окружения

engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)  # Создаем движок базы данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Создаем сессию
Base = declarative_base()  # Создаем базовый класс для моделей

# Функция для получения сессии базы данных
def get_db():
    """Получение сессии базы данных"""
    db = SessionLocal()  # Создание новой сессии
    try:
        yield db  # Возврат сессии
    finally:
        db.close()  # Закрытие сессии после использования
