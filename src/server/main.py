import sys
from pathlib import Path
from typing import Any, Generator

import uvicorn
import yaml  # noqa
from fastapi import FastAPI
from starlette.responses import HTMLResponse, StreamingResponse

# add parent path to sys.path
sys.path.insert(0, Path(__file__).parent.__str__())
sys.path.insert(0, Path(__file__).parent.parent.__str__())
sys.path.insert(0, Path(__file__).parent.parent.parent.__str__())

from src.deepllm.api import (
    activate_svos,
    deactivate_svos,
    run_advisor,
    run_rater,
    run_recursor,
)
from src.deepllm.exceptions.api_exception import APIException
from src.deepllm.rest_api.entities import QueryRequest, QueryResponse
from src.deepllm.util.file_path_util import FilePathUtil
from src.deepllm.prompters import prompter_dict

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
async def do_query(query: QueryRequest) -> StreamingResponse:
    try:
        print(query)

        if query.svos:
            activate_svos()
        else:
            deactivate_svos()

        prompters = prompter_dict()

        def generate_response() -> Generator[QueryResponse, None, None]:
            if query.recursor == "Recursor":
                g = run_recursor(
                    initiator=query.topic, prompter=prompters[query.prompter_name], lim=query.max_depth
                )
            elif query.recursor == "Advisor":
                g = run_advisor(
                    initiator=query.topic, prompter=prompters[query.prompter_name], lim=query.max_depth
                )
            else:
                g = run_rater(
                    initiator=query.topic,
                    prompter=prompters[query.prompter_name],
                    lim=query.max_depth,
                    threshold=query.threshold,
                )

            for kind, data in g:
                yield QueryResponse(kind=kind, data=data).json()

        return StreamingResponse(generate_response(), media_type = "application/text; charset=utf-8") # noqa

    except Exception as error:
        raise APIException(error.__str__())


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
