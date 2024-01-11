FROM python:3.11-alpine AS builder

WORKDIR /app

COPY requirements.txt .

RUN apk --no-cache add build-base \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.11-alpine

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app .

EXPOSE 5000

ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV AWS_REGION="us-east-1"
ENV E_HOURS=168
ENV PYTHONUNBUFFERED 0

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
