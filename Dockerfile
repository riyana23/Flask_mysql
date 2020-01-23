FROM python:3.8.1-alpine3.11
COPY . /usr/src/
WORKDIR /usr/src/
RUN pip install -r requirements.txt

