FROM python:3.6.4-slim-stretch

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
COPY run_aquabot.py /app

CMD [ "python", "./run_aquabot.py" ]