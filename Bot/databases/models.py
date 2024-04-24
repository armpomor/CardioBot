from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger)
    email = Column(String)
    name = Column(String)
    timezone = Column(Integer)
    language_code = Column(String)
    user_data = relationship("UserData")

    def __repr__(self) -> str:
        return f"{self.name} : {self.user_id}"


class UserData(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    systolic = Column(Integer)
    diastolic = Column(Integer)
    pulse = Column(Integer)
    arrhythmia = Column(String)
    comment = Column(String)
    person_id = Column(Integer, ForeignKey("people.id"))
