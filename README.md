# Описание приложения.
Приложение написано на FastAPI.

Есть возможнсоть запуска приложения в docker compose.

База данных- PostgreSQL.

Redis используется в качестве хранилища токенов.

Менеджер зависимостей- Poetry.
Миграции выполнены с помощью Alembic.
## Описание обеспечения безопасности приложения.
Защиат от SQL инекций обеспечена с помощью использования ORM SQLAlchemy.
Пароли хранятся не в исходном виде, а в виде хешей.
Функционал приложения доступен только пользователям с валидным токеном.
Если у пользователя время действия токена истекло, необходимо выполнить вход в систему повторно.
Возможность добавлять, изменять, получать, удалять данные о пользователях имеют только пользователи
с уровнем доступа "admin".
## Исходные данные.
При запуске приложения через docker compose, в базе данных уже есть 2 пользователя:
пользователь1 c email = "email1@mail.ru" и паролем "password" с уровнем доступа "admin";

пользователь2 с email = "email2@mail.ru" и паролем "password2" с уровнем доступа "user".
Используйте данные email и пароль для авторизации.
# Взаимодействие с приложением.
После запуска приложения, взаимодейстовать с ним можно по ссылке "http://хост:порт/docs".
Для регистрации нового пользователя, перейдите по ссылке "/api/v1/user_registration" и заполните необходимые данные.
Для авторизации перейдите по ссылке "/api/v1/login" и заполните необходимые данные.
Так же в приложении доступны функции добавления нового пользователя, обновление данных пользователя, получение списка всех пользователей,
удаление пользователя.
Инстркции по запуску приложения в docker compose и локально содержатся в следующих разделах.
# Запуск приложения в docker compose.
Перед запуском приложения, необходимо установить значения для переменных окружения в файле ".env-non-dev",
который находится в корневой директории.

В данном файле находятся следующие переменные окружения:

POSTGRES_DB,

POSTGRES_USER- имя пользователя базы данных,

POSTGRES_PASSWORD- пароль для базы данных,

DB_USER- имя пользователя базы данных,

PASSWORD- пароль для базы данных,

DB_HOST- хост базы данных,

DB_NAME- имя базы данных,

DB_PORT- порт базы данных,

REDIS_HOST- хост Redis,

REDIS_PORT- порт для Redis,

APP_HOST- хост для запуска приложения,

APP_PORT- порт для запуска приложения,

SECRET_KEY- ключ для шифрования паролей,

ALGORITHM- алгоритм для генерации токенов,

ACCESS_TOKEN_EXPIRE_MINUTES- время действий токена.

Для сборки контейнеров необходимо выполнить команду "docker compose build" в терминале из корневой директории.
Для запуска приложения необходимо выполнить команду "docker compose up app" в терминале из корневой директории.
# Запуск приложения локально.
Для запуска приложения, необходимо, чтобы были запущены серверы PostgreSQL и Redis.
Для установки зависимостей необходимо выполнить команду "poetry install" в терминале из корневой директории.
Для активации виртуального окружения необходимо выполнить команду "poetry shell" в терминале из корневой жиректории.
Перед запуском приложения, необходимо установить значения для переменных окружения в файле ".env", который находится в корневой директории.

В фацле ".env" содержатся следующие переменные окружения:

DB_USER- имя пользователя базы данных,

PASSWORD- пароль для базы данных,

DB_HOST- хост базы данных,

DB_NAME- имя базы данных,

DB_PORT- порт базы данных,

REDIS_HOST- хост Redis,

REDIS_PORT- порт для Redis,

APP_HOST- хост для запуска приложения,

APP_PORT- порт для запуска приложения,

SECRET_KEY- ключ для шифрования паролей,

ALGORITHM- алгоритм для генерации токенов,

ACCESS_TOKEN_EXPIRE_MINUTES- время действий токена.

Для выполнения миграций, необходимо выполнить команду "alembic upgrade head" 2 раза подряд в терминале из директории
"/test_task_ns/app".
Для создания ролей для пользователей необходимо выполнить команду "python create_roles.py" в терминале из директории
"/test_task_ns/app".
Для создания пользователей необходимо выполнить команду "python create_users.py" в терминале из директории
"/test_task_ns/app".
После выполнения этих команд, в базе данных будет создано 2 пользователя:
пользователь1 c email = "email1@mail.ru" и паролем "password" с уровнем доступа "admin";

пользователь2 с email = "email2@mail.ru" и паролем "password2" с уровнем доступа "user".
Используйте данные email и пароль для авторизации.
Для запуска приложения необходимо выполнить команду "python main.py" в терминале из директории
"/test_task_ns/app".
