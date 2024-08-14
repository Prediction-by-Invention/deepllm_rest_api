# DeepLLM REST API

## Overview

This is a fork of the [original DeepLLM project](https://github.com/ptarau/recursors) by Paul Tarau.
This fork was created with the endorsement of the original author so that a REST API and some other functionality could be added in the hope that it would useful.

All queries and information about the DeepLLM project should start with the original repository.

[Back to top](#table-of-contents)

## Setup

- You should create a `.env` in the root of your project and place your OpenAI API key in there.

```
# OpenAI API
OPENAI_API_KEY=sk-blahblahblah
```
- DeepLLM will pick it up from here.
- Alternatively, set up the usual `OPENAI_API_KEY` environmental variable.

[Back to top](#table-of-contents)

## Steps to Install DeepLLM from GitHub

### Clone the Repository:

First, clone the repository to your local machine using git and `cd` into the directory.

### Create a Virtual Environment (Optional but recommended):

It's a good practice to create a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

## REST API

- DeepLLM comes with a FastAPI Swagger API.
- You can use the provided script below to start it:

```bash
bin/deepllm-fastapi
```

- The REST API Swagger documentation will be available at http://0.0.0.0:8000/docs
- You can call the API with `curl` as below:

```bash
curl -X 'POST' \
  'http://localhost:8000/v1/query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "recursor": "Recursor",
  "threshold": 0.5,
  "max_depth": 1,
  "svos": true,
  "trace": false,
  "topic": "artificial general intelligence",
  "prompter_name": "scientific_concept_explorer"
}'
```

### Input JSON Example

```json
{
  "recursor": "Recursor",
  "threshold": 0.5,
  "max_depth": 1,
  "svos": true,
  "trace": false,
  "topic": "artificial general intelligence",
  "prompter_name": "scientific_concept_explorer"
}
```

[Back to top](#table-of-contents)

## Docker

- DeepLLM comes with a Docker build file.
- You can run the REST api using Docker.

### Docker Build

- You can use the provided script below to build the Docker image:

```bash
bin/docker-build
```

### Docker Run

- You can use the provided script below to run the Docker image :

```bash
bin/docker-run
```

[Back to top](#table-of-contents)

