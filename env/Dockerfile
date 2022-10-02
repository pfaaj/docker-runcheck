FROM python:3.11.0rc2-slim-bullseye

COPY  requirements.txt .

COPY  docker-runcheck.py .

COPY  Dockerfile .

RUN pip install -r requirements.txt

CMD ["python","./docker-runcheck.py"]

