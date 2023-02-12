from flask import Flask, render_template, Response
import json
import requests
import socket
import os

# Build the URL if the API server from an env var
full_url = 'http://{url}:5000/api/v1/resources/random'.format(url=os.environ['SW_URL'])

# Set up the application
application = Flask(__name__,)

# Define the web page
@application.route("/")
def index():
   """Star Wars Quote home page."""
   # Retrieve JSON document from the API server
   full = json.loads((requests.get(full_url).text))
   # Set the Logo to Display
   if full[0]['movie'] == "The Lord of the Rings":
      logo = "lotr.png"
   else:
      logo = "starwars.png"
   # Generate the web page from the template
   return render_template('starwars.html',quote = full[0]['quote'], character = full[0]['character'], movie = full[0]['movie'], container=socket.gethostname(), logo = logo)

# Run the app
if __name__ == "__main__":
    application.run()
