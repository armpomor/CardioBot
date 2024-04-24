# Telegram bot CardioBot

[Diary of blood pressure control and self-sensitivity.](https://t.me/Cardio100Bot)

- python 3.11
- aiogram
- aiogram_dialog
- sqlalchemy
- postgresql
- alembic
- docker and docker-compose
- fluentogram ru-en-pl 


## Bot functions

- Record blood pressure, pulse and comments in a diary about your health and medications taken.
- Change the time zone to correctly display the time of entry in the diary.
- Displays recordings on the screen with the ability to edit or delete them.
- Receive your diary as an Excel table.
- Receive statistics of the last 45 entries on the screen in the form of a graph of blood pressure and pulse.
- Send a diary in the form of an Excel table to the specified email.
- Delete the diary from the database at any time.
- Supported languages ru, en, pl
- Deployment via Docker

## Development

- In the config_data.py file from the config package, set the DEVELOPMENT value to True
- Make your .env file using .env.sample as an example
- Use docker-compose_dev.yml, which only runs PostgreSQL.
- Launch the bot from the IDE.

## Server Deployment

- In the get_settings.py file from the config package, set the DEVELOPMENT value to False
- Use docker-compose.yml
- `git clone Cardiobot`
- `cd Cardiobot`
- `vi .env`
- `docker compose -f docker-compose.yml up -d`

## Update on the server after changes

- `git push`  Pushing updates to Github
- `git pull`  Pull up updates on the server
- Run the following commands which will rebuild the container and load it without stopping the database:
- `docker compose -f docker-compose.yml build bot`
- `docker compose -f docker-compose.yml up --no-deps -d bot`