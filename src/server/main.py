import sys
from pathlib import Path
from typing import Any

import uvicorn
import yaml  # noqa
from fastapi import FastAPI
from starlette.responses import HTMLResponse

from src.deepllm.exceptions.api_exception import APIException
from src.deepllm.util.file_path_util import FilePathUtil

# add parent path to sys.path
sys.path.insert(0, Path(__file__).parent.__str__())
sys.path.insert(0, Path(__file__).parent.parent.__str__())
sys.path.insert(0, Path(__file__).parent.parent.parent.__str__())

app = FastAPI()


def load_openapi():
    """Load the Prompt Bouncer OpenAPI spec from a YAML file."""
    if app.openapi_schema:
        return app.openapi_schema
    with open(FilePathUtil.api_spec_path(), "r") as file:
        try:
            openapi_schema = yaml.safe_load(file)
            app.openapi_schema = openapi_schema
            return app.openapi_schema
        except Exception as error:
            raise APIException(message=error.__str__())


# load the API spec
app.openapi = load_openapi  # type: ignore


@app.get("/")
def get_root() -> Any:
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DeepLLM API</title>
    </head>
    <body>
        <h1>Welcome to the DeepLLM API</h1>
        <p><a href="/docs">Go to API Documentation</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/v1/query")
def do_query(request) -> Any:
    try:
        request: str = request.prompt
        print(request)
        return None
    except Exception as error:
        raise APIException(error.__str__())


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
