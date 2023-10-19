from fastapi import FastAPI

from src.api.router import api_router

VERSION = "/api/v1"

app = FastAPI(openapi_url=f"{VERSION}/openapi.json")

app.include_router(api_router, prefix=f"{VERSION}")
