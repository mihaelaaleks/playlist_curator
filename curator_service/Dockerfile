# temp stage
FROM python:3.12.2-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
apt-get install -y --no-install-recommends gcc && \
rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install -e . && pip list
RUN pip install fastapi[standard]

COPY . ./curator_service/

EXPOSE 8000
WORKDIR /app/curator_service

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000", "--reload"]
