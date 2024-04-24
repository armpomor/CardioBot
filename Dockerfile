FROM python:3.11-slim-bullseye
LABEL author=armpomor

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./Bot /Bot

WORKDIR /Bot

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt


CMD ["python", "__main__.py"]