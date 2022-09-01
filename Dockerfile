FROM python:3.10

WORKDIR /API

COPY ./requirements.txt /API/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /API/requirements.txt

COPY . /API/

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]