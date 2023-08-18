FROM python:3.7-slim

WORKDIR /app
ADD . /app
RUN pip install -r /app/requirements.txt

CMD python main.py