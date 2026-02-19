FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libatomic1

COPY pyproject.toml .
COPY prisma ./prisma
COPY src ./src

ENV PYTHONPATH=/app

RUN pip install --upgrade pip && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN pip install prisma
RUN prisma generate


CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]