"""
Модели БД
"""

from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Базовая модель
    """
    pass


class Person(Base):
    """
    Таблица people с нижеперечисленными полями
    Параметр primary_key=True указывает,
    что данный столбец будет представлять первичный ключ.
    Параметр index=True говорит, что для данного столбца
    будет создаваться индекс.
    """
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger)
    email = Column(String)
    name = Column(String)
    timezone = Column(Integer)
    date_time = Column(DateTime)
    systolic = Column(Integer)
    diastolic = Column(Integer)
    pulse = Column(Integer)
    arythmy = Column(String)
    comment = Column(String)
