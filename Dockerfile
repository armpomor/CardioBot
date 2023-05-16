FROM python:3.10-slim-bullseye
LABEL author=armpomor

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./Bot /Bot

WORKDIR /Bot

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt


CMD ["python", "bot.py"]