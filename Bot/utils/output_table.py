from typing import Any

import openpyxl
import pandas as pd


def create_diary(user_id: int) -> None:
    """
    Create a diary for the user with the name user_id
    :param user_id:
    :return:
    """
    wb = openpyxl.Workbook()
    wb.save(f"./tables/{user_id}.xlsx")


def save_data_excel(data: list[list[Any]], user_id: int) -> None:
    """
    The function saves the diary in Excel.
    Required libraries: pandas and openpyxl
    :param user_id:
    :param data:
    :return:
    """
    titles = [["DateTime", "Systolic", "Diastolic", "Pulse", "Arrhythmia", "Comment"]]
    titles += data
    df = pd.DataFrame(titles)

    create_diary(user_id)

    with pd.ExcelFile(f"./tables/{user_id}.xlsx") as writer:
        df.to_excel(writer)
