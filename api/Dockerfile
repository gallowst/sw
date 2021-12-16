FROM python:alpine

RUN mkdir /api
RUN adduser -D gunicorn
RUN chown gunicorn:gunicorn /api
USER gunicorn
ENV PATH="/api/bin:${PATH}"
RUN python3 -m venv /api && source /api/bin/activate && python3 -m pip install flask gunicorn

COPY config.py /api
COPY wsgi.py /api
COPY quotes.json /api

EXPOSE 5000
WORKDIR /api/
CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "wsgi:application"]