FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /app
EXPOSE 8000
ADD . /app
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app