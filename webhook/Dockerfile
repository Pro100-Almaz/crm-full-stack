FROM python:3.11.4-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY ../.env .env

CMD ["uvicorn", "src.app:app","--host", "0.0.0.0", "--port", "5000"]