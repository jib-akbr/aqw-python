# Build stage
FROM python:3.10.11-alpine AS builder

RUN apk add --no-cache gcc musl-dev libffi-dev

WORKDIR /app

COPY requirements.txt . 

RUN pip install --no-cache-dir --no-compile --prefer-binary -r requirements.txt

COPY . .

FROM python:3.10.11-alpine

WORKDIR /app

RUN apk add --no-cache libffi

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app /app

RUN rm -rf /app/.git /app/tests /app/docs

CMD ["python", "main-web.py"]
