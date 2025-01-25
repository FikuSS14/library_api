import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Юнит-тесты

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    """Переопределение зависимости"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

#Создание тестового клиента
client = TestClient(app)

#Фикстура для тестовой базы данных
@pytest.fixture(scope="module")
def test_db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

#регистрация пользователя
def test_create_user(test_db):
    user_data = {"username": "testuser", "password": "password"}
    response = client.post("/register/", json=user_data)
    assert response.status_code == 200
    assert "id" in response.json()

