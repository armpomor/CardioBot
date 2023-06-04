from datetime import timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# from config.config_dev import DB_HOST, DB_USER, DB_NAME, DB_PASS
from config.config import DB_HOST, DB_USER, DB_NAME, DB_PASS
from database.models import Base, Person
from utils.utils import save_diary_csv, save_diary_excel


def connect_db():
    # Для взаимодействия с базой данных создаем движок - объект класса Engine.
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
    # Создаем таблицу
    Base.metadata.create_all(bind=engine)
    return engine


def session_add(person, engine):
    """
    Создаем сессию подключения к базе данных
    и добавляем запись в таблицу
    """
    with Session(autoflush=True, bind=engine) as db:
        # Создаем объект Person для добавления в БД
        user = Person(**person)

        db.add(user)
        db.commit()


def session_delete_person(engine, user_id):
    """
    Создаем сессию подключения к базе данных
    и удаляем пользователя из БД по user_id по его требованию
    """
    with Session(autoflush=True, bind=engine) as db:
        db.query(Person).filter(Person.user_id == user_id).delete(synchronize_session='fetch')
        db.commit()


def session_add_email(engine, user_id, email):
    """
    Добавляем полученный email во все строки по user_id
    """
    with Session(autoflush=True, bind=engine) as db:
        db.query(Person).filter(Person.user_id == user_id).update({"email": email}, synchronize_session='fetch')
        db.commit()


def session_add_timezone(engine, user_id, timezone):
    """
    Изменяет во всех записях время в соответствии с поясом.
    Добавляет полученный часовой пояс во все строки по user_id.
    """
    with Session(autoflush=True, bind=engine) as db:
        notes = db.query(Person).filter(Person.user_id == user_id).all()  # Список всех записей

        for note in notes:
            delta = timezone - note.timezone
            note.date_time += timedelta(hours=delta)
            db.add(note)
            db.commit()

        db.query(Person).filter(Person.user_id == user_id).update({"timezone": timezone}, synchronize_session='fetch')

        db.commit()


def session_number_rows(engine, user_id):
    """
    Функция определяет количество записей определенного пользователя
    """
    with Session(autoflush=True, bind=engine) as db:
        return len(db.query(Person).filter(Person.user_id == user_id).all())


def session_get_all_notes(engine, user_id):
    """
    Функция извлекает все записи определенного пользователя,
    сортирует данные по дате и времени
    и записывает их в файлы в форматах csv и exel.
    Возвращает данные в виде списка списков.
    """
    with Session(autoflush=True, bind=engine) as db:
        notes = db.query(Person).filter(Person.user_id == user_id).order_by(Person.date_time).all()
        data = [[note.date_time, note.systolic, note.diastolic, note.pulse, note.arythmy, note.comment] for note in
                notes]

        save_diary_csv(data)
        save_diary_excel(data)
        return data


def session_get_email_notes(engine, user_id):
    """
    Функция извлекает все записи определенного пользователя
    и проверяет есть ли в записях сохраненный email. Если есть
    возвращает его, если нет возвращает None
    """
    with Session(autoflush=True, bind=engine) as db:
        notes = db.query(Person).filter(Person.user_id == user_id).all()
        data = list(filter(lambda x: x is not None, [[note.email] for note in notes]))[0][0]
        return data


def session_get_timezone_notes(engine, user_id):
    """
    Функция извлекает все записи определенного пользователя
    и проверяет есть ли в записях сохраненный часовой пояс. Если есть
    возвращает его, если нет возвращает None
    """
    with Session(autoflush=True, bind=engine) as db:
        notes = db.query(Person).filter(Person.user_id == user_id).all()
        data = list(filter(lambda x: x is not None, [[note.timezone] for note in notes]))[0][0]
        return data


def session_last_date(engine, user_id):
    """
    Функция извлекает последнюю запись
    пользователя для редактирования, если она есть
    """
    with Session(autoflush=True, bind=engine) as db:
        return db.query(Person).filter(Person.user_id == user_id).order_by(Person.date_time).all()[-1]


def session_delete_note(engine, id):
    """
    Функция удаляет из таблицы одну запись по ее id
    """
    with Session(autoflush=True, bind=engine) as db:
        note = db.query(Person).filter(Person.id == id).one()
        db.delete(note)
        db.commit()


if __name__ == '__main__':
    engine = connect_db()
