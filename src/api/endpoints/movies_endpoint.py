import requests
from fastapi import APIRouter
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from typing import Any, List

from src.services.movies_service import (
    load_movies,
    load_movie_info,
    load_movies_per_day,
    display_movies_by_date,
    display_movies_by_language,
)
from src.core.exceptions.api_exception import ApiException
from src.core.json.rapid_json import RapidJSONResponse
from src.api.schemas.movies_schema import Movie, MovieDetail, MovieByDate

router = APIRouter()


@router.get("/{theater}", tags=["Movies"], response_model=List[Movie])
def load_movies_endpoint(theater: str):
    try:
        response = load_movies(theater)
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


@router.get("/{slug}/info", tags=["Movies"], response_model=MovieDetail)
def load_movie_info_endpoint(slug: str):
    try:
        response = load_movie_info(slug)
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


@router.get("/{theater}/movies-per-day", tags=["Movies"], response_model=Any)
def load_movies_per_day_endpoint(theater: str):
    try:
        response = load_movies_per_day(theater)
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


@router.get(
    "/{theater}/display-by-date/{date}",
    response_model=List[MovieByDate],
    tags=["Movies"],
)
def display_movies_by_date_endpoint(theater: str, date: str):
    try:
        response = display_movies_by_date(theater, date)
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


@router.get(
    "/{theater}/display-by-language/{language}", response_model=Any, tags=["Movies"]
)
def display_movies_by_date_endpoint(theater: str, language: str):
    try:
        response = display_movies_by_language(theater, language)
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
