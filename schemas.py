from pydantic import BaseModel  # Импортируем базовый класс для схем
from typing import List, Optional

# Схема для создания пользователя
class UserCreate(BaseModel):
    username: str  # Имя пользователя
    password: str  # Пароль пользователя
    role: Optional[str] = "reader"  # Роль, по умолчанию "reader"

# Схема для пользователя в базе данных
class UserInDB(UserCreate):
    id: int  # Идентификатор пользователя
    hashed_password: str  # Хэшированный пароль

    class Config:
        from_attributes = True  # Конфигурация для Pydantic

# Базовая схема для книги
class BookBase(BaseModel):
    title: str  # Название книги
    description: str  # Описание книги
    publication_date: str  # Дата публикации
    authors: List[int]  # Список идентификаторов авторов
    genres: List[str]  # Жанры
    quantity: int  # Количество экземпляров

# Схема для создания книги
class BookCreate(BookBase):
    pass  # Унаследовать все поля от BookBase

# Схема для книги из базы данных
class Book(BookBase):
    id: int  # Идентификатор книги

    class Config:
        from_attributes = True

# Базовая схема для автора
class AuthorBase(BaseModel):
    name: str  # Имя автора
    biography: str  # Биография автора
    date_of_birth: str  # Дата рождения

# Схема для создания автора
class AuthorCreate(AuthorBase):
    pass  # Унаследовать все поля от AuthorBase

# Схема для автора из базы данных
class Author(AuthorBase):
    id: int  # Идентификатор автора

    class Config:
        from_attributes = True

# Базовая схема для читателя
class ReaderBase(BaseModel):
    user_id: int  # Идентификатор пользователя

class ReaderCreate(ReaderBase):
    pass  # Унаследовать все поля от ReaderBase

class Reader(ReaderBase):
    id: int  # Идентификатор читателя
    borrowed_books: List[int]  # Список идентификаторов одолженных книг

    class Config:
        from_attributes = True

# Базовая схема для одолженной книги
class BorrowedBookBase(BaseModel):
    book_id: int  # Идентификатор книги
    reader_id: int  # Идентификатор читателя
    borrow_date: str  # Дата рождения
    return_date: Optional[str]  # Дата возврата

class BorrowedBookCreate(BorrowedBookBase):
    pass  # Унаследовать все поля от BorrowedBookBase

class BorrowedBook(BorrowedBookBase):
    id: int  # Идентификатор записи об одолженной книге

    class Config:
        from_attributes = True

# Схема для данных токена
class TokenData(BaseModel):
    username: Optional[str] = None  # Имя пользователя

# Схема для токена
class Token(BaseModel):
    access_token: str  # Токен доступа
    token_type: str  # Тип токена
