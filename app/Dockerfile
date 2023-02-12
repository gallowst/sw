FROM python:alpine

RUN apk upgrade expat
RUN mkdir /app
RUN adduser -D gunicorn
RUN chown gunicorn:gunicorn /app
USER gunicorn
ENV PATH="/app/bin:${PATH}"
COPY ./requirements.txt .
RUN python3 -m venv /app && source /app/bin/activate && python3 -m pip install --use-pep517 -r requirements.txt
COPY . /app
EXPOSE 8080
WORKDIR /app/
CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "wsgi:application"]
