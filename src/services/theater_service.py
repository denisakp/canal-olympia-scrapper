import logging
from typing import List
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from src.wraper.request_wraper import load_html_data, host
from src.core.exceptions.api_exception import ApiException, ApiErrorsCode
from src.api.schemas.theater_schema import (
    TheaterList,
    Theater,
    SocialNetwork,
    Pricing,
    Schedule,
    Session,
    Movie,
)

LOGGER = logging.getLogger(__name__)


def display_all_theater() -> List[TheaterList]:
    """
    Display a list of theaters
    :return: List of TheaterList model
    """
    try:
        response: List[TheaterList] = []
        soup = load_html_data(host)

        div = soup.find("div", class_="theater-select-nav closed-theater-selection")
        ul = div.find("ul")
        theaters = ul.find_all("li")

        for theater in theaters:
            a_tag = theater.find("a")
            href = a_tag["href"]
            theater_name = a_tag.get_text()

            element = TheaterList(**{"href": href, "name": theater_name})

            response.append(element)
        return response
    except Exception as exec_info:
        LOGGER.error("Failed to load theaters. Exception %s", str(exec_info))
        raise ApiException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=ApiErrorsCode.THEATER_LOAD_FAILED,
            message=f"Failed to load theaters",
        )


def display_one_theater(slug) -> Theater:
    """
    Load details for an existing theater name
    :param slug: Theater slug
    :return: Theater
    """
    resource = f"{host}theaters/{slug}/"

    try:
        soup = load_html_data(resource)

        theater_element = soup.find("div", class_="theater-top-container-cover-wrapper")
        figure_element = theater_element.select_one("figure > img")
        figure = figure_element.get("src") if figure_element else "N/A"

        title = theater_element.select_one("h1").text.strip()
        address = theater_element.select_one("a.adress").get_text(strip=True)

        social_network_element = soup.find_all("a", class_="info-section-rs-icon")
        social_networks: List[SocialNetwork] = []
        for a_element in social_network_element:
            href_value = a_element.get("href")
            img_element = a_element.find("img")
            alt_value = img_element.get("alt") if img_element else "N/A"

            social_network = SocialNetwork(**{"name": alt_value, "href": href_value})
            social_networks.append(social_network)

        pricing_element = soup.find("ul", class_="prices-table")
        pricing: List[Pricing] = []
        elements = pricing_element.find_all("li")
        for element in elements:
            price_name = element.find("span", class_="price-name").get_text(strip=True)
            price_value = element.find("span", class_="price-value").get_text(
                strip=True
            )

            price = Pricing(**{"name": price_name, "amount": price_value})
            pricing.append(price)

        schedule_element = soup.find("div", class_="info-section-hours").find_all("li")
        schedules: List[Schedule] = []
        for schedule in schedule_element:
            schedule_title = schedule.find("span", class_="title").get_text(strip=True)
            schedule_hour = schedule.find("span", class_="hours").get_text(strip=True)

            element = Schedule(
                **{"day_slots": schedule_title, "time_slots": schedule_hour}
            )
            schedules.append(element)

        session_elements = soup.find_all("li", attrs={"data-date": True})
        sessions: List[Session] = []
        for session in session_elements:
            session_date = session.get("data-date")
            session_weekday = session.find("span", class_="week-day").get_text(
                strip=True
            )
            session_week_number = session.find("span", class_="week-number").get_text(
                strip=True
            )

            movies: List[Movie] = load_session_movies(soup, session_date)
            element = Session(
                **{
                    "scheduled_date": session_date,
                    "weekday": session_weekday,
                    "week_number": session_week_number,
                    "movies": movies,
                }
            )
            sessions.append(element)

        return Theater(
            **{
                "figure": figure,
                "title": title,
                "address": address,
                "social_networks": list(social_networks),
                "pricing": list(pricing),
                "schedule": list(schedules),
                "sessions": list(sessions),
            }
        )
    except Exception as exec_info:
        LOGGER.exception(
            "Failed to load theater wit slug %s, Exception %s", slug, str(exec_info)
        )
        raise ApiException(
            status_code=HTTP_404_NOT_FOUND,
            error_code=ApiErrorsCode.THEATER_LOAD_FAILED,
            message=f"Failed to load theater with slug {slug}",
        )


def load_session_movies(soup, session_date) -> List[Movie]:
    """
    Load list of movies for a given session
    :param soup: Beatifulsop instance
    :param session_date: Session date
    :return: List of movies
    """
    response: List[Movie] = []

    movie_elements = soup.find(
        "ul", attrs={"data-date": session_date}, class_="theater-movies"
    ).find_all("li", class_=True)
    for movie in movie_elements:
        movie_url = movie.find("a")["href"]
        movie_title = movie.find("h2").get("title")
        hour_span = movie.find("span", class_="hour").text.split(" ")

        element = Movie(
            **{
                "movie_url": movie_url,
                "movie_title": movie_title,
                "session_hour": hour_span[0],
                "language": hour_span[1],
            }
        )
        response.append(element)
    return response
