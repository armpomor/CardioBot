"""
Модуль для построения графиков статистики
"""

import matplotlib.dates as dates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FixedFormatter


def create_array(data):
    """
    Создаем массив из data.
    Убираем из массива комментарии и наличие аритмии.
    Возвращаем словарь {date_time: value, systolic: value, diastolic: value, pulse: value}
    """
    array = np.array(data)
    values = array[..., :4]
    date_time = values[..., 0]
    systolic = values[..., 1]
    diastolic = values[..., 2]
    pulse = values[..., 3]
    return dict(date_time=date_time, systolic=systolic, diastolic=diastolic, pulse=pulse)


def create_statistics(data):
    """
    Функция строит график статистики.
    На входе список списков
    """
    values = create_array(data)

    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot()

    x = values['date_time']
    y1 = values['systolic']
    y2 = values['diastolic']
    y3 = values['pulse']

    ax.plot(x, y1, label=u'Systolic')
    ax.scatter(x, y1)
    ax.plot(x, y2, label=u'Diastolic')
    ax.scatter(x, y2)
    ax.plot(x, y3, label=u'Pulse')
    ax.scatter(x, y3)

    ax.legend()

    ax.grid()

    time_format = dates.DateFormatter('%m-%d')

    ax.xaxis.set_major_formatter(time_format)
    ax.xaxis.set_tick_params(rotation=50)

    ax.yaxis.set_major_locator(FixedLocator(list(range(40, 260, 10))))
    ax.yaxis.set_major_formatter(FixedFormatter(list(range(40, 260, 10))))
    ax.yaxis.set_tick_params(which='major', labelleft=True, labelright=True)

    fig.savefig('diary/Diary.png', dpi=300)
    # plt.show()


if __name__ == '__main__':
    pass
