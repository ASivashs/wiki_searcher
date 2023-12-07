FROM python:3.11-alpine

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN python3 -m spacy download en_core_web_lg
RUN python3 -m spacy download en_core_web_sm

COPY /app .

EXPOSE 5000

CMD ["python3", "wsgi.py"]
