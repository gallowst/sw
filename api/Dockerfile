FROM python:alpine

RUN apk add --no-cache --upgrade \
    expat && \
    adduser -D gunicorn && \
    mkdir /api && \
    chown gunicorn:gunicorn /api
USER gunicorn
ENV PATH="/api/bin:${PATH}"
WORKDIR /api/
COPY ./requirements.txt .
RUN python3 -m venv /api && \
    source /api/bin/activate && \
    pip install --no-cache-dir --use-pep517 -r requirements.txt
COPY config.py wsgi.py quotes.json ./

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:application"]
