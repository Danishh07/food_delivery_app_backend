FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use environment variable for port if provided, default to 8002
ENV PORT=8002

# Use the PORT environment variable in the command
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
