from flask import Flask, render_template, Response
import json
import requests
import socket
import os

# Set up the application
application = Flask(__name__)

# Define the web page
@application.route("/")
def index():
   """Star Wars Quote home page."""
   try:
       # Retrieve JSON document from the API server
       full_url = f"http://{os.environ['SW_URL']}:5000/api/v1/resources/random"
       response = requests.get(full_url)
       response.raise_for_status()
       full = response.json()

       # Generate the web page from the template
       return render_template('starwars.html',
                              quote=full[0]['quote'],
                              character=full[0]['character'],
                              movie=full[0]['movie'],
                              container=socket.gethostname(),
                              logo="starwars.svg")
   except (KeyError, requests.exceptions.RequestException) as e:
       return str(e), 500

# Run the app
if __name__ == "__main__":
    application.run()
