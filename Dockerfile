# ---- Build ----
FROM python:3.12-slim AS builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --upgrade pip && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---- Runtime ----
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "sitechx.asgi:application"]
