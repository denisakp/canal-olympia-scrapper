from fastapi import APIRouter


from src.api.endpoints import theater_endpoint
from src.api.endpoints import movies_endpoint


api_router = APIRouter()

api_router.include_router(theater_endpoint.router, prefix="/theaters")
api_router.include_router(movies_endpoint.router, prefix="/movies")
