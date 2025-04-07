FROM python:3.11
WORKDIR /Job_Portal
COPY requirements.txt /Job_Portal/

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . /Job_Portal/

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Job_Portal.wsgi:application"]
