from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    recursor: str = Field(..., description="Type of LLM agent to use")
    threshold: Optional[float] = Field(
        None, description="Threshold for the Rater agent"
    )
    max_depth: int = Field(..., description="Maximum depth for recursion")
    svos: bool = Field(..., description="Extract relations (SVOs) from the result")
    trace: bool = Field(..., description="Show trace of the query execution")
    topic: str = Field(..., description="Topic to explore")
    prompter_name: str = Field(..., description="Name of the prompter to use")


class QueryResponse(BaseModel):
    kind: str = Field(
        ..., description="The type of result (e.g., TRACE, CLAUSES, MODEL, SVOS, COSTS)"
    )
    data: Any = Field(..., description="The data corresponding to the kind")
