FROM python:3.12-slim

WORKDIR /usr/src/app

COPY requirements.txt .

COPY ./schema.sql .

# Required for installing psycopg2 with slim image
RUN apt-get update && apt-get install -y \
  libpq-dev \
  gcc

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000/tcp
