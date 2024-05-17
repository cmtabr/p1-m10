FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt .
COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "api.main:app", "--lifespan", "on", "--host=0.0.0.0", "--port=5000"]