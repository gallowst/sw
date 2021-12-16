FROM python:alpine

RUN mkdir /app
RUN adduser -D gunicorn
RUN chown gunicorn:gunicorn /app
USER gunicorn
ENV PATH="/app/bin:${PATH}"
RUN python3 -m venv /app && source /app/bin/activate && python3 -m pip install flask gunicorn yieldfrom.urllib.request requests
COPY . /app

EXPOSE 80
WORKDIR /app/
CMD ["gunicorn"  , "-b", "0.0.0.0:80", "wsgi:application"]