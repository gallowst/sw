import flask, random, json
from flask import Flask, jsonify, request #render_template, Response,
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from os import getenv
import logging

JAEGER_HOST = getenv('JAEGER_HOST', 'localhost')

application = Flask(__name__,)

log_level = logging.DEBUG
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)
# Create configuration object with enabled logging and sampling of all requests.
config = Config(config={'sampler': {'type': 'const', 'param': 1}, 'logging': True, 'local_agent': {'reporting_host': JAEGER_HOST}}, service_name="starwars")          

jaeger_tracer = config.initialize_tracer()
tracing = FlaskTracing(jaeger_tracer)

# Load in the quotes from disk
with open('quotes.json') as json_file:
    quotes = json.load(json_file)

# Route to show the home page
@application.route('/', methods=['GET'])
def home():
    return '''<h1>Star Wars</h1>
<p>A Star Wars quote API.</p>
<p>Get a <a href=/api/v1/resources/random>random</a> quote</p>
<p>Get <a href=/api/v1/resources/all>all</a> quotes</p>
<p><a href=/api/v1/resources/query>Query</a> for a quote from a specific movie or character</p>'''


# A route to return all of the available entries in our catalog.
@application.route('/api/v1/resources/all', methods=['GET'])
def api_all():
    return jsonify(quotes)

@application.route('/api/v1/resources/query', methods=['GET'])
def api_movie():

    # Create an empty list for our results
    results = []

    if 'movie' in request.args:
        movie = request.args['movie']

        # Loop through the data and match results that fit the requested query
        for quote in quotes:
            if quote['movie'] == movie:
                results.append(quote)

    elif 'character' in request.args:
        character = request.args['character']

        for quote in quotes:
            if quote['character'] == character:
                results.append(quote)
    
    if results:
        # Use the jsonify function from Flask to convert our list of Python dictionaries to the JSON format.
        return jsonify(random.choice(results))

    else:
        return '''<h1>Star Wars</h1>
        <p>A Star Wars quote API.</p>
        <p><b>Error:</b> No Movie or character provided.</p>
        <p>Please specify a Star Wars character or a Film from the following list:
        <ol>
          <li>A New Hope</li>
          <li>The Empire Strikes Back</li>
          <li>Return of the Jedi</li>
          <li>The Phantom Menace</li>
          <li>Revenge of the Sith</li>
          <li>Attack of the Clones</li>
        </ol></p>
        <p>Get a <a href=/api/v1/resources/random>random</a> quote</p>'''

@application.route('/api/v1/resources/random', methods=['GET'])
@tracing.trace()
def api_random():

    # Create an empty list for our results
    results = []
    with jaeger_tracer.start_active_span(
        'random method') as scope:
        results.append(random.choice(quotes))
        scope.span.log_kv({'event': 'generated random trace', 'result': results})
    return jsonify(results)

if __name__ == "__main__":
  application.run()