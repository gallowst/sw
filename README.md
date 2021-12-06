# Example Flask Application

- Two node Flask Application that provides an API to query a list of Starwars Quotes
- `api` is the container used to host the Starwars API
- `app` is the container used to query the API and provide a dynamic web page with the results

## API Container

The API Container exposes the following `http` endpoints that allow the querying of `quotes.json`

- `/api/v1/resources/query`
  - Appending `?movie=` will search for a quote from a specific movie
  - Appending `?character=` will search for a quote from a specific character
- `/api/v1/resources/random`
  - Gets a random quote
- `/api/v1/resources/all`
  - Gets all quotes

## APP Container

The App Container serves `http` requests and renders the results of `/api/v1/resources/random` in a HTML template.  It also displays the name of the running container to show load balancing operations

## Deployment

- `build.ps1` can be used to deploy the containers as Azure Container Instances
- The individual Dockerfiles can be used to build local instances of the App
- The application code can be built using Dockerfiles that use git to clone the app prior to building as per the AKS demo

### Remote Build of the API Container

~~~dockerfile
FROM python:alpine
LABEL maintainer="containers@computacenter.com"
RUN pip install flask gunicorn

# Install git
RUN apk add git

# Install the app
RUN PAT="kw6h443ksv5c4j6cw63qoydrwcudlaa5lvhvgceod72z2bwz5wja" && \
    B64_PAT=$(printf "%s"":$PAT" | base64) && \
    git -c http.extraHeader="Authorization: Basic ${B64_PAT}" clone https://CC-Azure-DevOps@dev.azure.com/CC-Azure-DevOps/Service-Development/_git/sysops-star-wars-flask-app /starwars
EXPOSE 5000
WORKDIR /starwars/api
CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "wsgi:application"]
~~~

### Remote Build of the APP Container

~~~dockerfile
FROM python:alpine
LABEL maintainer="containers@computacenter.com"
RUN pip install flask gunicorn yieldfrom.urllib.request requests

# Install git
RUN apk add git

# Install the app
RUN PAT="kw6h443ksv5c4j6cw63qoydrwcudlaa5lvhvgceod72z2bwz5wja" && \
    B64_PAT=$(printf "%s"":$PAT" | base64) && \
    git -c http.extraHeader="Authorization: Basic ${B64_PAT}" clone https://CC-Azure-DevOps@dev.azure.com/CC-Azure-DevOps/Service-Development/_git/sysops-star-wars-flask-app /starwars
EXPOSE 80
WORKDIR /starwars/app
CMD ["gunicorn"  , "-b", "0.0.0.0:80", "wsgi:application"]
~~~