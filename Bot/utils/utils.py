import csv
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
from yagmail import SMTP

# from config.config_dev import EMAIL, EMAIL_PASS
from config.config import EMAIL, EMAIL_PASS


def get_current_time(tz=0) -> datetime:
    """
    Функция изменяет время с utc на московский часовой пояс
    или на пояс, который был введен пользователем
    """
    tz += 3
    delta = timedelta(hours=tz)
    d = datetime.now(timezone.utc) + delta
    return d


def add_datetime(person, tz=0) -> datetime:
    """
    Функция проверяет есть ли в полученном словаре данные
    по ключу data_time. Если нет добавляет текущую дату и время,
    а если есть, тогда из данных по ключам month, day и time формирует
    экземпляр datetime, сохраняет его по ключу date_time и удаляет
    значения с ключами month, day и time.
    Возвращаем измененный словарь
    """
    dict_time = {'morning': 7, 'noon': 13, 'evening': 19}
    if 'time' in person:
        d = datetime(datetime.now().year,
                     int(person['month']),
                     int(person['day']),
                     dict_time[person['time']],
                     0)
        person['date_time'] = d
        del person['time']
        del person['month']
        del person['day']

    else:
        d = get_current_time(tz)
        person['date_time'] = datetime(d.year,
                                       d.month,
                                       d.day,
                                       d.hour,
                                       d.minute)

    return person


def send_email(email):
    """
    Функция отправляет дневник пользователю
    На входе email
    """
    yad = SMTP(EMAIL, EMAIL_PASS)

    contents = ['Привет! Это CardioBot. Дневник во вложении к этому письму.']

    yad.send(email, 'subject', contents, attachments=['./diary/Diary.csv', './diary/Diary.xlsx'])


def save_diary_csv(data):
    """
    Функция записывает и сохраняет дневник в формате csv.
    На входе список списков с данными
    """
    titles = [['Дата-время', 'Systolic', 'Diastolic', 'Pulse', 'Аритмия', 'Comment']]
    titles += data
    with open('./diary/Diary.csv', 'w+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        for row in titles:
            writer.writerow(row)


def save_diary_excel(data):
    """
    Функция сохраняет дневник в excel
    """
    titles = [['Дата-время', 'Systolic', 'Diastolic', 'Pulse', 'Аритмия', 'Comment']]
    titles += data
    df = pd.DataFrame(titles)

    with pd.ExcelWriter('./diary/Diary.xlsx') as writer:
        df.to_excel(writer)


def preparation_data(data):
    """
    Функция извлекает последние 45 записей
    определенного пользователя для построения графика
    """
    values = np.array(data)
    values = np.flip(values, 0)
    return values[:45]


if __name__ == '__main__':
    pass
