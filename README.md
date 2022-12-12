## Приложение QRKot

Проект QRKot — приложение для Благотворительного фонда поддержки котиков. Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AndreyIzotov/QRkot_spreadsheets.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас Windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать файл .env:

```
APP_TITLE=                  # Название сервиса
APP_DESCRIPTION=            # Описание проекта 
DATABASE_URL=               # Подключение к базе данных
SECRET=                     # Секретное слово
FIRST_SUPERUSER_EMAIL=      # email суперпользователя, создается при первом запуске
FIRST_SUPERUSER_PASSWORD=   # пароль суперпользователя, создается при первом запуске
TYPE=                       # данные для авторизации в google api
PROJECT_ID=                 # данные для авторизации в google api
PRIVATE_KEY_ID=             # данные для авторизации в google api
PRIVATE_KEY=                # данные для авторизации в google api
CLIENT_EMAIL=               # данные для авторизации в google api
CLIENT_ID=                  # данные для авторизации в google api
AUTH_URI=                   # данные для авторизации в google api
TOKEN_URI=                  # данные для авторизации в google api
AUTH_PROVIDER_X509_CERT_URL=# данные для авторизации в google api
CLIENT_X509_CERT_URL=       # данные для авторизации в google api
EMAIL=                      # электронная почта google аккаунта пользователя
```

Автогенерация миграций:

```
alembic revision --autogenerate -m "First migration"
```

Применение миграций:

```
alembic upgrade head
```

Запуск проекта:

```
uvicorn app.main:app --reload
```

Документация API:

```
http://127.0.0.1:8000/docs
```

### Технологии:
- Python 3.10,8
- FastAPI
- SQLAlchemy 1.4.36
- Git