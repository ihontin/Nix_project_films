FROM python:3.9-slim

WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app" ]
