FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		build-essential \
		default-libmysqlclient-dev \
		pkg-config \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY infirmary_backend /app

EXPOSE 8000

CMD ["gunicorn", "infirmary.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
