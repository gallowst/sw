from flask import Flask, render_template, Response
import json
import requests
import socket
import os
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from os import getenv
import logging

JAEGER_HOST = getenv('JAEGER_HOST', 'localhost')

# Build the URL if the API server from an env var
full_url = 'http://{url}:5000/api/v1/resources/random'.format(url=os.environ['SW_URL'])

# Set up the application
application = Flask(__name__,)

log_level = logging.DEBUG
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)
# Create configuration object with enabled logging and sampling of all requests.
config = Config(config={'sampler': {'type': 'const', 'param': 1},
                        'logging': True,
                        'local_agent':
                        # Also, provide a hostname of Jaeger instance to send traces to.
                        {'reporting_host': JAEGER_HOST}},
               # Service name can be arbitrary string describing this particular web service.
               service_name="starwars")
jaeger_tracer = config.initialize_tracer()
tracing = FlaskTracing(jaeger_tracer)

# Define the web page
@application.route("/")
def index():
   """Star Wars Quote home page."""
   # Retrieve JSON document from the API server
   full = json.loads((requests.get(full_url).text))
   # Generate the web page from the template
   return render_template('starwars.html',quote = full[0]['quote'], character = full[0]['character'], movie = full[0]['movie'], container=socket.gethostname())

# Run the app
if __name__ == "__main__":
    application.run()
