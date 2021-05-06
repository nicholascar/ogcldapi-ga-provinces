FROM python:3.7.8-slim-buster

EXPOSE 5000

# Python requirements
COPY ./requirements.txt ./
COPY ./requirements-provinces.txt ./
RUN pip install -r ./requirements.txt
RUN pip install -r ./requirements-provinces.txt

# API
COPY ./api ./api

# data
COPY ./data ./data

WORKDIR ./api

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]
