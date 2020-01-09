FROM python:3.6.9

RUN mkdir /code
WORKDIR /code

COPY . ./
RUN pip install -r requirement.txt
