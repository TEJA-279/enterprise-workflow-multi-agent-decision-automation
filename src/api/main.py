import os
from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.api.metrics import api_metrics
from src.workflows.memory_workflow import MemoryWorkflow


app = FastAPI(
    title="Enterprise Workflow API",
    version="1.0.0",
)


# Allow frontend to connect to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "http://127.0.0.1:5500,http://localhost:5500",
        ).split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


workflow = MemoryWorkflow(
    os.getenv("MEMORY_DATABASE_PATH", "memory.db")
)


class WorkflowRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=2000)


class WorkflowResponse(BaseModel):
    decision: str
    errors: list[str]
    run_id: str = ""
    stage_timings_ms: dict[str, float] = Field(default_factory=dict)


@app.middleware("http")
async def record_request_metrics(request: Request, call_next):
    started_at = perf_counter()
    successful = True

    try:
        response = await call_next(request)
        successful = response.status_code < 400
        return response
    except Exception:
        successful = False
        raise
    finally:
        api_metrics.record(
            latency_ms=(perf_counter() - started_at) * 1000,
            successful=successful,
        )


@app.get("/")
def root():

    return {
        "message": "Enterprise Workflow API is running."
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-workflow-api",
    }


@app.get("/metrics")
def metrics():
    return api_metrics.snapshot()


@app.post(
    "/workflow",
    response_model=WorkflowResponse,
)
def run_workflow(
    request: WorkflowRequest
):

    result = workflow.run(
        session_id=request.session_id,
        user_query=request.message,
    )

    return {
        "decision": result.get(
            "decision",
            "",
        ),

        "errors": result.get(
            "errors",
            [],
        ),
        "run_id": result.get("run_id", ""),
        "stage_timings_ms": result.get(
            "stage_timings_ms",
            {},
        ),
    }