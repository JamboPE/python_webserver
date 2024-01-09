# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /python_webserver-docker
COPY dependencies dependencies
RUN pip3 install -r dependencies
COPY . .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]