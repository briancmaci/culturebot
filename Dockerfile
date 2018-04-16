FROM python:3.6.4-slim-stretch

RUN mkdir /app
WORKDIR /app

RUN mkdir /db

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
COPY run_aquabot.py /app

COPY ./aquabot/db/. /db

ENV DATABASE_PATH /db
ENV SLACK_BOT_TOKEN xoxb-347026176099-eIL17IqSh79utThfAQJ4oIe0
ENV SLACK_VERIFICATION_TOKEN Qhw48BMuKNF7P96r6a0WA4ES
ENV FLASK_APP run_aquabot.py

EXPOSE 5000
CMD flask run --host=0.0.0.0