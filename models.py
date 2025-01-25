from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text  # Импортируем типы данных для полей модели
from sqlalchemy.orm import relationship  # Импортируем функцию для задания связей между моделями
from sqlalchemy.ext.declarative import declarative_base  # Импортируем базовый класс для создания моделей

Base = declarative_base()  # Создание базового класса для моделей

# Модель пользователя
class User(Base):
    __tablename__ = "users"  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)  # ID пользователя, первичный ключ
    username = Column(String, unique=True, index=True)  # Имя пользователя, уникальное значение
    hashed_password = Column(String)  # Хэшированный пароль
    role = Column(String, default="reader")  # Роль пользователя, по умолчанию "reader"

# Модель книги
class Book(Base):
    __tablename__ = "books"  # Имя таблицы

    id = Column(Integer, primary_key=True, index=True)  # ID книги, первичный ключ
    title = Column(String, index=True)  # Название книги
    description = Column(Text)  # Описание книги
    publication_date = Column(Date)  # Дата публикации
    quantity = Column(Integer)  # Количество экземпляров
    genres = Column(Text)  # Жанры

# Модель автора
class Author(Base):
    __tablename__ = "authors"  # Имя таблицы

    id = Column(Integer, primary_key=True, index=True)  # ID автора, первичный ключ
    name = Column(String, index=True)  # Имя автора
    biography = Column(Text)  # Биография
    date_of_birth = Column(Date)  # Дата рождения

# Связующая модель для книги и автора
class BookAuthor(Base):
    __tablename__ = "book_authors"  # Имя таблицы

    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)  # ID книги
    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)  # ID автора

# Модель читателя
class Reader(Base):
    __tablename__ = "readers"  # Имя таблицы

    id = Column(Integer, primary_key=True, index=True)  # ID читателя, первичный ключ
    user_id = Column(Integer, ForeignKey("users.id"))  # ID пользователя
    borrowed_books = relationship("BorrowedBook", back_populates="reader")  # Связь с одолженными книгами

# Модель одолженной книги
class BorrowedBook(Base):
    __tablename__ = "borrowed_books"  # Имя таблицы

    id = Column(Integer, primary_key=True, index=True)  # ID записи, первичный ключ
    book_id = Column(Integer, ForeignKey("books.id"))  # ID книги
    reader_id = Column(Integer, ForeignKey("readers.id"))  # ID читателя
    borrow_date = Column(Date)  # Дата одолжения
    return_date = Column(Date)  # Дата возврата
    reader = relationship("Reader", back_populates="borrowed_books")  # Связь с моделью Reader
    book = relationship("Book")  # Связь с моделью Book
