FROM python:3.10

WORKDIR /API

COPY ./requirements.txt /API/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /API/requirements.txt

COPY . /API/

CMD ["uvicorn", "Service_API:app"]