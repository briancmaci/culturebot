FROM python:3.6.4-slim-stretch

ADD run_aquabot.py /
COPY requirements.txt /

RUN pip install -r requirements.txt

ADD . /aquabot

CMD [ "python", "./run_aquabot.py" ]