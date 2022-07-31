FROM python:alpine

WORKDIR /app

COPY ./app /app

RUN python -m pip install --upgrade pip
RUN pip install Flask
RUN pip install -r requirements.txt -t .

CMD ["python", "index.py"]
