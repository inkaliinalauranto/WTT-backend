
FROM python:3.10

WORKDIR /code

COPY . /code

RUN chmod -R 755 /code

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]