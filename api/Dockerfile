FROM python:alpine
LABEL maintainer="containers@computacenter.com"
RUN pip install flask gunicorn

RUN mkdir /api
COPY config.py /api
COPY wsgi.py /api
COPY quotes.json /api

EXPOSE 5000
WORKDIR /api/
CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "wsgi:application"]