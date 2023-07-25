FROM python:3.7

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./app /code/app

RUN pip install --no-cache-dir -r requirements.txt --upgrade && \
    pip install -r requirements.txt


EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]