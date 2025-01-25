# Импорт необходимых библиотек и модулей
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas import (
    UserCreate,
    BookCreate,
    AuthorCreate,
    Book,
    Author,
)
from crud import (
    create_user,
    get_books,
    create_book,
    get_authors,
    create_author,
    borrow_book,
    return_book,
    get_user_by_username,
    authenticate_user,
)
from auth import (
    get_current_active_user,
    get_admin_user,
    create_access_token,
)
from models import Base, User
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import List
import logging

# Создание приложения FastAPI
logging.basicConfig(level=logging.INFO)  # Настройка уровня логирования
logger = logging.getLogger(__name__)  # Создание логгера

Base.metadata.create_all(bind=engine)  # Создание всех таблиц в базе данных

app = FastAPI()  # Инициализация приложения FastAPI

# Функция для получения сессии базы данных
def get_db():
    """Получение сессии базы данных"""
    db = SessionLocal()  # Создание новой сессии
    try:
        yield db  # Возврат сессии
    finally:
        db.close()  # Закрытие сессии после использования

# Регистрация нового пользователя
@app.post("/register/", response_model=UserCreate)  # Определение маршрута /register с методом POST
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)  # Получаем пользователя по имени
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")  # Если пользователь уже существует, выбрасываем исключение
    return create_user(db=db, user=user)  # Создаем нового пользователя

# Получение токена
@app.post("/token")  # Определение маршрута /token с методом POST
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)  # Аутентификация пользователя
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",  # Ошибка аутентификации
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)  # Установка времени жизни токена
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )  # Создание токена
    return {"access_token": access_token, "token_type": "bearer"}  # Возвращаем токен

# Получение списка книг
@app.get("/books/", response_model=List[Book])  # Определение маршрута /books с методом GET
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = get_books(db, skip=skip, limit=limit)  # Получение книг из базы данных
    return books  # Возврат списка книг

# Создание новой книги
@app.post("/books/", response_model=Book)  # Определение маршрута для создания книги
def create_book_item(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    return create_book(db=db, book=book)  # Создание книги

# Получение списка авторов
@app.get("/authors/", response_model=List[Author])  # Определение маршрута для получения авторов
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = get_authors(db, skip=skip, limit=limit)  # Получение авторов
    return authors  # Возврат списка авторов

# Создание нового автора
@app.post("/authors/", response_model=Author)  # Определение маршрута для создания автора
def create_author_item(
    author: AuthorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    return create_author(db=db, author=author)  # Создание нового автора

# Выдача книги читателю
@app.post("/borrow/{book_id}/{reader_id}")  # Определение маршрута для выдачи книги
def borrow_book_item(
    book_id: int,
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = borrow_book(db=db, book_id=book_id, reader_id=reader_id)  # Выдача книги
    if not result:
        logger.error(f"Failed to borrow book {book_id} for reader {reader_id}")  # Логирование ошибки
        raise HTTPException(status_code=400, detail="Cannot borrow the book")  # Ошибка при выдаче книги
    logger.info(f"Book {book_id} borrowed by reader {reader_id}")  # Логирование успешного действия
    return {"message": "Book borrowed successfully"}  # Возврат успеха

# Возврат книги
@app.post("/return/{book_id}/{reader_id}")  # Определение маршрута для возврата книги
def return_book_item(
    book_id: int,
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = return_book(db=db, book_id=book_id, reader_id=reader_id)  # Возврат книги
    if not result:
        logger.error(f"Failed to return book {book_id} for reader {reader_id}")  # Логирование ошибки
        raise HTTPException(status_code=400, detail="Cannot return the book")  # Ошибка при возврате
    logger.info(f"Book {book_id} returned by reader {reader_id}")  # Логирование успешного действия
    return {"message": "Book returned successfully"}  # Возврат успеха
