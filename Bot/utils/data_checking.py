from typing import Any

from pyisemail import is_email


def check_systolic(text: str) -> int:
    """
    Checking the entered systolic pressure data
    """
    if text.isdigit() and 50 <= int(text) <= 250:
        return int(text)
    raise ValueError


def check_diastolic(text: str) -> int:
    """
    Checking the entered diastolic pressure data
    """
    if text.isdigit() and 30 <= int(text) <= 180:
        return int(text)
    raise ValueError


def check_pulse(text: str) -> int:
    """
    Checking the entered heart rate data
    """
    if text.isdigit() and 0 <= int(text) <= 220:
        return int(text)
    raise ValueError


def check_comment(text: str) -> str:
    """
    Checking the entered comment
    for length. No longer than 50 characters
    """
    if len(text) <= 50:
        return text
    raise ValueError


def check_email(email: str) -> str:
    """
    Email validity check
    :param email:
    :return:
    """
    if is_email(address=email, check_dns=True):
        return email
    raise ValueError


def date_str(data: list[list[Any]]) -> list[list[Any]]:
    """
    Convert datetime in records to str
    """
    return [
        [
            item[0].strftime("%Y-%m-%d %H:%M"),
            item[1],
            item[2],
            item[3],
            item[4],
            item[5],
        ]
        for item in data
    ]
