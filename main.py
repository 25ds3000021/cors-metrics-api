
import time
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-e57llf.example.com"

@app.middleware("http")
async def add_headers(request: Request, call_next):
    start_time = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        raise
    finally:
        process_time = time.perf_counter() - start_time

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = str(max(0.0, process_time))

    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/stats")
def get_stats(values: str):
    try:
        numbers = [int(value.strip()) for value in values.split(",")]

        if not numbers:
            raise ValueError("Empty list")

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Please provide comma-separated integers"
        )

    return {
        "email": "25ds3000021@ds.study.iitm.ac.in",
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers)
    }
