FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir kubernetes

COPY . .

CMD [ "python", "./main.py" ]
