"""Buy Smart Trust API — FastAPI entrypoint."""

import os
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.trust import router as trust_router
from services import trust_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _cors_origins() -> list[str]:
    raw = os.getenv("ALLOWED_ORIGINS", "")
    if raw.strip():
        return [origin.strip() for origin in raw.split(",") if origin.strip()]
    return [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading review corpora...")
    trust_service.init_corpora()
    yield


app = FastAPI(
    title="Buy Smart Trust API",
    version="0.4.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(trust_router, prefix="/api/trust")


@app.get("/api/health")
def health():
    path_a, path_b = trust_service.corpus_paths()
    return {
        "status": "ok",
        "phase": "3-api",
        "corpus_a": str(path_a),
        "corpus_b": str(path_b),
    }
