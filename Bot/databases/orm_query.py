import logging
from datetime import datetime
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from databases.models import Person, UserData

logger = logging.getLogger(__name__)


async def orm_get_id_user(
    async_session: async_sessionmaker[AsyncSession], user_id: int
) -> list[int]:
    """
    By user_id we extract the user id
    :param async_session:
    :param user_id: id in telegram
    :return:
    """
    async with async_session() as session:
        users = select(Person).where(Person.user_id == user_id)
        result = await session.scalars(users)

        return [user.id for user in result]


async def orm_add_user(
    async_session: async_sessionmaker[AsyncSession], data: dict[str, Any]
) -> None:
    """
    Add a new user to the database if it is not there.
    :param async_session:
    :param data:
    :return:
    """
    if len(await orm_get_id_user(async_session, data["user_id"])):
        return
    async with async_session() as session:
        person = Person(
            user_id=data["user_id"],
            name=data["name"],
            language_code=data["language_code"],
            email="",
        )

        session.add(person)
        await session.commit()


async def orm_add_data_user(
    async_session: async_sessionmaker[AsyncSession], data: dict[str, Any]
) -> None:
    """
    Adding the data entered by the user
    :param async_session:
    :param data:
    :return:
    """
    async with async_session() as session:
        pk = await orm_get_id_user(async_session, data["user_id"])

        user_data = UserData(
            date_time=data["date_time"],
            systolic=data["systolic"],
            diastolic=data["diastolic"],
            pulse=data["pulse"],
            arrhythmia=data["arrhythmia"],
            comment=data["comment"],
            person_id=pk[0],
        )

        session.add(user_data)
        await session.commit()


async def orm_delete_user_data(
    async_session: async_sessionmaker[AsyncSession], user_id: int
) -> None:
    """
    We delete all entries entered by the user
    :param async_session:
    :param user_id:
    :return:
    """
    async with async_session() as session:
        pk = await orm_get_id_user(async_session, user_id)

        query = await session.execute(
            select(UserData).where(UserData.person_id == pk[0])
        )
        objects = query.scalars().all()

        for obj in objects:
            await session.delete(obj)

        await session.commit()


async def orm_update_user(
    async_session: async_sessionmaker[AsyncSession], data: dict[str, Any], user_id: int
) -> None:
    """
    Updating user data
    :param async_session:
    :param data:
    :param user_id:
    :return:
    """
    async with async_session() as session:
        query = update(Person).where(Person.user_id == user_id).values(**data)

        await session.execute(query)
        await session.commit()


async def orm_get_user_timezone(
    async_session: async_sessionmaker[AsyncSession], user_id: int
) -> int:
    """
    Using user_id, we retrieve the user's timezone
    :param async_session:
    :param user_id:
    :return:
    """
    async with async_session() as session:
        pk = await orm_get_id_user(async_session, user_id)
        if len(pk) < 1:
            return 0
        user = await session.get(Person, pk)

        return user.timezone if user.timezone is not None else 0


async def orm_get_user_email(
    async_session: async_sessionmaker[AsyncSession], user_id: int
) -> str | None:
    """
    By user_id we retrieve the user's email
    :param async_session:
    :param user_id:
    :return:
    """
    async with async_session() as session:
        pk = await orm_get_id_user(async_session, user_id)
        user = await session.get(Person, pk)

        return user.email


async def orm_get_user_data(
    async_session: async_sessionmaker[AsyncSession], user_id: int
) -> list[list[Any]]:
    """
    By user_id we retrieve all user records
    :param async_session:
    :param user_id:
    :return:
    """
    async with async_session() as session:
        pk = await orm_get_id_user(async_session, user_id)

        query = await session.execute(
            select(UserData)
            .where(UserData.person_id == pk[0])
            .order_by(UserData.date_time)
        )

        objects = query.scalars().all()

        data = [
            [
                obj.date_time,
                obj.systolic,
                obj.diastolic,
                obj.pulse,
                obj.arrhythmia,
                obj.comment,
            ]
            for obj in objects
        ]

        return data


async def orm_get_row_user_data(
    async_session: async_sessionmaker[AsyncSession], user_id: int, date: datetime
) -> UserData:
    """
    Using user_id and datetime, extract
    a string from user records
    """
    async with async_session() as session:
        pk = await orm_get_id_user(async_session, user_id)

        query = await session.execute(
            select(UserData).where(
                UserData.person_id == pk[0] and UserData.date_time == date
            )
        )

        return query.scalar()


async def orm_delete_row_user_data(
    async_session: async_sessionmaker[AsyncSession], user_id: int, date: datetime
) -> None:
    """
    Removing a line from a user's records
    """
    async with async_session() as session:
        obj = await orm_get_row_user_data(async_session, user_id, date)

        await session.delete(obj)

        await session.commit()
