from sqlalchemy.orm import Session  # Импортируем сессии
from models import User, Book, Author, Reader, BorrowedBook  # Импортируем модели
from schemas import UserCreate, BookCreate, AuthorCreate, ReaderCreate  # Импортируем схемы
from auth import get_password_hash, verify_password  # Импортируем функции для работы с паролями
from datetime import datetime  # Импортируем класс для работы с датой и временем

# Получение пользователя по имени
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()  # Запрос к БД

# Создание нового пользователя
def create_user(db: Session, user: UserCreate): 
    hashed_password = get_password_hash(user.password)  # Хэширование пароля
    db_user = User(username=user.username, hashed_password=hashed_password, role=user.role)  # Создание нового пользователя
    db.add(db_user)  # Добавление в сессию
    db.commit()  # Сохранение
    db.refresh(db_user)  # Обновление пользователя
    return db_user  # Возврат пользователя

# Аутентификация пользователя
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()  # Получение пользователя
    if not user or not verify_password(password, user.hashed_password):
        return False  # Если не удается аутентифицироваться
    return user  # Возврат пользователя

# Получение списка книг
def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()  # Запрос к БД

# Создание новой книги
def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.dict())  # Создание нового экземпляра книги
    db.add(db_book)  # Добавление в сессию
    db.commit()  # Сохранение
    db.refresh(db_book)  # Обновление книги
    return db_book  # Возврат книги

# Получение списка авторов
def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Author).offset(skip).limit(limit).all()  # Запрос к БД

# Создание нового автора
def create_author(db: Session, author: AuthorCreate):
    db_author = Author(**author.dict())  # Создание нового экземпляра автора
    db.add(db_author)  # Добавление в сессию
    db.commit()  # Сохранение
    db.refresh(db_author)  # Обновление автора
    return db_author  # Возврат автора

# Функция для выдачи книги
def borrow_book(db: Session, book_id: int, reader_id: int):
    book = db.query(Book).get(book_id)  # Получение книги
    reader = db.query(Reader).get(reader_id)  # Получение читателя
    if not book or not reader:
        return None  # Если книга или читатель не найдены
    if book.quantity <= 0:
        return None  # Если нет доступных экземпляров
    if len(reader.borrowed_books) >= 5:
        return None  # Если читатель уже взял максимальное количество книг
    borrowed_book = BorrowedBook(book_id=book_id, reader_id=reader_id, borrow_date=datetime.now().date())  # Создание записи об одолженной книге
    book.quantity -= 1  # Уменьшение количества книг в наличии
    db.add(borrowed_book)  # Добавление в сессию
    db.commit()  # Сохранение
    db.refresh(borrowed_book)  # Обновление записи
    return borrowed_book  # Возврат записи об одолженной книге

# Функция для возврата книги
def return_book(db: Session, book_id: int, reader_id: int):
    borrowed_book = db.query(BorrowedBook).filter(BorrowedBook.book_id == book_id, BorrowedBook.reader_id == reader_id).first()  # Получение записи об одолженной
