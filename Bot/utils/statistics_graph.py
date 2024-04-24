"""
Module for plotting
blood pressure and pulse.
"""

import logging
from typing import Any

import matplotlib.dates as dates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FixedFormatter

logger = logging.getLogger(__name__)


def create_array(data: list[list[Any]]) -> dict[str, Any]:
    """
    We remove comments and arrhythmia from the array.
    :param data:
    :return:
    """
    array = np.array(data)
    values = array[..., :4]
    date_time = values[..., 0]
    systolic = values[..., 1]
    diastolic = values[..., 2]
    pulse = values[..., 3]
    return dict(
        date_time=date_time, systolic=systolic, diastolic=diastolic, pulse=pulse
    )


def data_num_lines(data: list[list[Any]], num: int) -> np.ndarray:
    """
    The function retrieves num of the user's latest posts
    """
    values = np.array(data)
    values = np.flip(values, 0)

    return values[:num]


def create_statistics(data: list[list[Any]], user_id: int) -> None:
    """
    The function plots a graph of pressure and pulse.
    Saves by user_id
    """
    values = create_array(data)

    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot()

    x = values["date_time"]
    y1 = values["systolic"]
    y2 = values["diastolic"]
    y3 = values["pulse"]

    ax.plot(x, y1, label="Systolic")
    ax.scatter(x, y1)
    ax.plot(x, y2, label="Diastolic")
    ax.scatter(x, y2)
    ax.plot(x, y3, label="Pulse")
    ax.scatter(x, y3)

    ax.legend()

    ax.grid()

    time_format = dates.DateFormatter("%m-%d")

    ax.xaxis.set_major_formatter(time_format)
    ax.xaxis.set_tick_params(rotation=50)

    ax.yaxis.set_major_locator(FixedLocator(list(range(40, 260, 10))))
    ax.yaxis.set_major_formatter(FixedFormatter(list(range(40, 260, 10))))
    ax.yaxis.set_tick_params(which="major", labelleft=True, labelright=True)

    fig.savefig(f"./tables/{user_id}.png", dpi=300)
    # plt.show()
