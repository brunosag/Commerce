ARG PYTHON_VERSION=3.10-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

ENV SECRET_KEY "CZIiuV31MoOhiWhLd2s2K5sbig2yFR0b4PZT9XOEuYtVok545c"
RUN python manage.py collectstatic --noinput
RUN python3 manage.py migrate
RUN python3 manage.py create_categories
RUN python3 manage.py create_listings

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "commerce.wsgi"]
