# CardioBot
[@Cardio100Bot](https://t.me/Cardio100Bot)

Telegram-bot с PostgreSQL, SQLAlchemy и Docker.
Дневник контроля артериального давления и самочувствия.

## Функции
- Сохранять в дневнике показатели артериального давления, пульса и комментарии 
о самочувствии и принятых лекарствах.
- Изменять часовой пояс. По умолчанию записывается московское время.
- Получать статистику последних 45 записей на экран в виде графика.
- Отправлять на указанный email дневник в виде .xlsx и .csv таблиц.
- В любое время удалять дневник из базы данных.
- Доступ к базе данных через Adminer
- Развертывание через Docker

## Разработка 
- Использовать config_dev.py из пакета config.
- Сделайте свой файл .env на примере .env.sample 
- В модулях, где используются константы(TOKEN и т.д.)
необходимо изменить импорты.
- В файле .env прописать DB_HOST=127.0.0.1
- Использовать docker-compose_dev.yml, который запускает только PostgreSQL.
- Бота запускать из IDE.

## Развертывание на сервере
- Использовать config.py из пакета config.
Соответственно в модулях, где используются константы(TOKEN и т.д.)
необходимо изменить импорты.
- В файле .env прописать DB_HOST=db
- Использовать docker-compose.yml

### На сервере
- `install docker`
- `install docker compose`
- `git clone Cardiobot`
- `cd Cardiobot`
- `vi .env`
- `docker compose -f docker-compose.yml build`
- `docker compose -f docker-compose.yml up -d`

## Обновление на сервере после изменений
- `git push`  Отправка обновлений на Github
- `git pull`  На сервере
- Выполнить следующие команды, которые перестроят контейнер
и загрузят его без остановки базы данных:
- `docker compose -f docker-compose.yml build bot`
- `docker compose -f docker-compose.yml up --no-deps -d bot`