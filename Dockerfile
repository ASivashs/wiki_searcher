FROM python:3.11-alpine

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY /app .

EXPOSE 5000

CMD ["python3", "wsgi.py"]
