from collections import defaultdict
from typing import List
import logging

from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from src.wraper.request_wraper import load_html_data, host
from src.api.schemas.movies_schema import Movie, MovieDetail, MovieByDate
from src.core.exceptions.api_exception import ApiException, ApiErrorsCode


LOGGER = logging.getLogger(__name__)


def load_movies(theater: str) -> List[Movie]:
    """
    Load movies of a theater
    :param theater: slug
    :return: List af movie
    """
    try:
        resource = (
            f"{host}theaters/{theater}/"
            if "activites-" not in theater
            else f"{host}theaters/{theater.split('-')[-1]}"
        )

        response: List[Movie] = []

        soup = load_html_data(resource)
        theater_movies_element = soup.find_all(
            "ul", class_="theater-movies", attrs={"data-date": True}
        )
        for theater_movie in theater_movies_element:
            date_value = theater_movie["data-date"]
            movies = theater_movie.find_all("li", class_="")
            for movie in movies:
                movie_url = movie.find("a")["href"]
                movie_title = movie.find("h2").get("title")
                hour_span = movie.find("span", class_="hour").text.split(" ")

                movie = Movie(
                    **{
                        "scheduled_date": date_value,
                        "scheduled_hour": hour_span[0],
                        "title": movie_title,
                        "language": hour_span[1],
                        "detail": movie_url,
                    }
                )
                response.append(movie)

        return response
    except Exception as exec_info:
        LOGGER.error(
            "Failed to load movies for theater with slug %s. Exception %s",
            theater,
            str(exec_info),
        )
        raise ApiException(
            status_code=HTTP_404_NOT_FOUND,
            error_code=ApiErrorsCode.MOVIE_LOAD_FAILED,
            message=f"Failed to load movies for theater with slug {theater}",
        )


def load_movie_info(slug: str) -> MovieDetail:
    """
    Load movie info
    :param slug:
    :return:
    """
    resource = f"{host}movies/{slug}/"

    try:
        soup = load_html_data(resource)

        genre = soup.select_one(
            "div.movie-top-container-cover-content > p.genres > span"
        ).text.strip()
        synopsis = soup.select_one("div.synopse-modal > p").text.strip()
        date_time_element = soup.find(
            "div", class_="movie-top-container-cover-content"
        ).find("p")
        out_date = (
            date_time_element.find("span", class_="date")
            .get_text(strip=True)
            .split(":")[1]
            .strip()
        )
        movie_length = (
            date_time_element.find("span", class_="time")
            .get_text(strip=True)
            .split(":")[1]
            .strip()
        )
        trailer = soup.select_one("div.movie > iframe").get("src")

        return MovieDetail(
            **{
                "genre": genre,
                "release_date": out_date,
                "length": movie_length,
                "synopsis": synopsis,
                "trailer": trailer,
            }
        )
    except Exception as exec_info:
        LOGGER.error(
            "Failed to load movie with slug %s. Exception %s", slug, str(exec_info)
        )
        raise ApiException(
            status_code=HTTP_404_NOT_FOUND,
            error_code=ApiErrorsCode.MOVIE_LOAD_FAILED,
            message=f"Failed to load movie with slug {slug}",
        )


def load_movies_per_day(theater: str):
    """
    Load movies per day for a given theater
    :param theater: Slug
    :return:
    """
    try:
        response = load_movies(theater)

        movies_by_date = defaultdict(list)
        for movie in response:
            scheduled_date = movie.scheduled_date
            movie_data = {
                key: value
                for key, value in movie.model_dump().items()
                if key != "scheduled_date"
            }
            movies_by_date[scheduled_date].append(movie_data)
        return [
            {"scheduled_date": date, "movies": movies}
            for date, movies in movies_by_date.items()
        ]
    except Exception as exec_info:
        LOGGER.exception(
            "Failed to load movies per day for theater %s. Exception %s",
            theater,
            str(exec_info),
        )
        raise ApiException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=ApiErrorsCode.MOVIE_LOAD_FAILED,
            message=f"Failed to load movies par day",
        )


def display_movies_by_date(theater, scheduled_date):
    """
    Load movies by date
    :param theater: theater slug
    :param scheduled_date:
    :return:
    """
    try:
        response: List[MovieByDate] = []
        movies = load_movies(theater)
        filtered_movies = [
            movie for movie in movies if movie.scheduled_date == scheduled_date
        ]

        for movie in filtered_movies:
            element = MovieByDate(
                **{
                    "scheduled_hour": movie.scheduled_date,
                    "title": movie.title,
                    "language": movie.language,
                    "detail": movie.detail,
                }
            )
            response.append(element)
        return response
    except Exception as exec_info:
        LOGGER.exception(
            "Failed to load movies by date for theater %s. Exception %s",
            theater,
            str(exec_info),
        )
        raise ApiException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=ApiErrorsCode.MOVIE_LOAD_FAILED,
            message=f"Failed to load movies per day",
        )


def display_movies_by_language(theater, language) -> List[Movie]:
    """
    Load movies by language
    :param theater:
    :param language:
    :return:
    """
    try:
        response: List[Movie] = []
        movies = load_movies(theater)

        filtered_movies = [movie for movie in movies if movie.language == language]

        for movie in filtered_movies:
            element = Movie(
                **{
                    "scheduled_date": movie.scheduled_date,
                    "scheduled_hour": movie.scheduled_hour,
                    "title": movie.title,
                    "detail": movie.detail,
                    "language": movie.language,
                }
            )
            response.append(element)
        return response
    except Exception as exec_info:
        LOGGER.exception(
            "Failed to load movies by language for theater %s. Exception %s",
            theater,
            str(exec_info),
        )
        raise ApiException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=ApiErrorsCode.MOVIE_LOAD_FAILED,
            message=f"Failed to load movies by languages",
        )
