# temp stage
FROM python:3.12.2-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
apt-get install -y --no-install-recommends gcc && \
rm -rf /var/lib/apt/lists/*

COPY curator_service/ ./curator_service/
COPY pyproject.toml .


RUN pip install -e .


EXPOSE 8000

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]