FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-mysql-client gcc && \
    pip install --no-cache-dir flask mysql-connector-python && \
    apt-get purge -y gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY wait-for-db.sh ./
COPY app.py ./
COPY templates ./templates

ENTRYPOINT ["./wait-for-db.sh"]
CMD ["python", "app.py"]
