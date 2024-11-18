
FROM python:3.10

WORKDIR /app

COPY . /app

RUN chmod -R 755 /app

RUN pip install -r requirements.txt

COPY . .


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]