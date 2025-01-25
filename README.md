*Установите необходимые библиотеки из requirements.txt

*Создайте базу данных PostgreSQL и настройте файл .env

---
DATABASE_URL=postgresql://name:password@localhost/library_db
SECRET_KEY=mysecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
Вставьте свои name, password
---
*Чтобы запустить сервер, используйте команду

uvicorn main:app --reload 

*Приложение будет доступно по адресу http://127.0.0.1:8000/docs

*Убедитесь, что вы находитесь в каталоге, где находится файл main.py.
