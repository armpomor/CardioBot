# Telegram bot CardioBot

[Дневник контроля артериального давления и самочувствия.](https://t.me/Cardio100Bot)

- aiogram_dialog
- sqlalchemy
- postgresql
- docker and docker-compose
- fluentogram ru-en-pl 


## Функции бота

- Записывать в дневник показатели артериального давления, пульса и комментарии
  о самочувствии и принятых лекарствах.
- Изменять часовой пояс для корректного отображения времени записи в дневнике.
- Выводит на экран записи с возможностью их редактирования или удаления.
- Получать дневник в виде таблицы Exel
- Получать статистику последних 45 записей на экране в виде графика артериального давления и пульса.
- Отправлять на указанный email дневник в виде таблицы Exel.
- В любое время удалять дневник из базы данных.
- Поддерживаемые языки ru, en, pl
- Развертывание через Docker

## Разработка

- В файле config_data.py из пакета config значение DEVELOPMENT установить True
- Сделайте свой файл .env на примере .env.sample
- Использовать docker-compose_dev.yml, который запускает только PostgreSQL.
- Бота запускать из IDE.

## Развертывание на сервере

- В файле get_settings.py из пакета config значение DEVELOPMENT установить False
- Использовать docker-compose.yml
- `git clone Cardiobot`
- `cd Cardiobot`
- `vi .env`
- `docker compose -f docker-compose.yml up -d`

## Обновление на сервере после изменений

- `git push`  Отправка обновлений на Github
- `git pull`  На сервере подтянуть обновления
- Выполнить следующие команды, которые перестроят контейнер
  и загрузят его без остановки базы данных:
- `docker compose -f docker-compose.yml build bot`
- `docker compose -f docker-compose.yml up --no-deps -d bot`