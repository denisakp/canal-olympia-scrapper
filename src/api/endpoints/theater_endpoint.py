import requests
from fastapi import APIRouter
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from typing import List

from src.services.theater_service import display_all_theater, display_one_theater
from src.api.schemas.theater_schema import TheaterList, Theater
from src.core.exceptions.api_exception import ApiException
from src.core.json.rapid_json import RapidJSONResponse

router = APIRouter()


@router.get("/", tags=["Theaters"], response_model=List[TheaterList])
def load_theaters_endpoint():
    try:
        response = display_all_theater()
        return response
    except ApiException as api_exec:
        return RapidJSONResponse(
            status_code=api_exec.status_code, content=api_exec.message
        )
    except requests.exceptions.RequestException as rqst_exec:
        return RapidJSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=rqst_exec.response["Error"],
        )


@router.get("/{slug}", tags=["Theaters"], response_model=Theater)
def load_theater_info_endpoint(slug: str):
    try:
        response = display_one_theater(slug)
        return response
    except ApiException as api_exec:
        return RapidJSONResponse(
            status_code=api_exec.status_code, content=api_exec.message
        )
    except requests.exceptions.RequestException as rqst_exec:
        return RapidJSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=rqst_exec.response["Error"],
        )
