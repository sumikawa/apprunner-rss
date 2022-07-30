FROM python:alpine

WORKDIR /app

COPY ./app /app

RUN pip install Flask requests dropbox boto3 feedgenerator

CMD ["python", "index.py"]
