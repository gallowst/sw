# Example Flask Application

[![Build Status](https://dev.azure.com/gallowst/docker/_build/latest?definitionId=20&branchName=master)](https://dev.azure.com/gallowst/docker/_build/latest?definitionId=20&branchName=master)

- Two node Flask Application that provides an API to query a list of Example Quotes
- `api` is the container used to host the Example API
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