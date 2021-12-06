FROM python:alpine
LABEL maintainer="containers@computacenter.com"
RUN pip install flask gunicorn yieldfrom.urllib.request requests

RUN mkdir /app
COPY . /app

EXPOSE 80
WORKDIR /app/
CMD ["gunicorn"  , "-b", "0.0.0.0:80", "wsgi:application"]