FROM python:alpine

RUN apk add --no-cache --upgrade \
    expat && \
    adduser -D gunicorn && \
    mkdir /app && \
    chown gunicorn:gunicorn /app
USER gunicorn
ENV PATH="/app/bin:${PATH}"
WORKDIR /app/
COPY requirements.txt ./
RUN python3 -m venv /app && \
    source /app/bin/activate && \
    pip install --no-cache-dir --use-pep517 -r requirements.txt
COPY . .

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:application"]
