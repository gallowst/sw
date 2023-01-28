import flask, random, json
from flask import Flask, render_template, Response, jsonify, request
from jaeger_client import Config
from flask_opentracing import FlaskTracing

application = Flask(__name__,)

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
def api_random():

    # Create an empty list for our results
    results = []
    results.append(random.choice(quotes))
    return jsonify(results)

def initialise_tracer():
  config = Config(
     config={ 'sampler': {'type': 'const','param': 1},
   }, 
   service_name="sw-api")
  return config.initialize_tracer()

flask_tracer = FlaskTracing(initialise_tracer, True, application)

if __name__ == "__main__":
  application.run()
