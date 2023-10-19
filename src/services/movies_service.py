from collections import defaultdict

from src.wraper.request_wraper import load_html_data, host


def load_movies(theater: str):
    """
    Load movies of a theater
    :param theater:
    :return:
    """
    resource = (
        f"{host}theaters/{theater}/"
        if "activites-" not in theater
        else f"{host}theaters/{theater.split('-')[-1]}"
    )

    response = []

    soup = load_html_data(resource)
    theater_movies = soup.find_all(
        "ul", class_="theater-movies", attrs={"data-date": True}
    )
    for theater_movie in theater_movies:
        date_value = theater_movie["data-date"]
        movies = theater_movie.find_all("li", class_="")
        for movie in movies:
            movie_url = movie.find("a")["href"]
            movie_title = movie.find("h2").get("title")
            hour_span = movie.find("span", class_="hour").text.split(" ")

            movie = {
                "scheduled_date": date_value,
                "scheduled_hour": hour_span[0],
                "title": movie_title,
                "language": hour_span[1],
                "detail": movie_url,  # il faut mettre l'addres de l'api qui affiche le détail d'un movie
            }

            response.append(movie)

    return response


def load_movie_info(slug: str):
    """
    Load movie info
    :param slug:
    :return:
    """
    resource = f"{host}movies/{slug}/"

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

    return {
        "genre": genre,
        "release_date": out_date,
        "length": movie_length,
        "synopsis": synopsis,
        "trailer": trailer,
    }


def load_movies_per_day(theater: str):
    """
    Affichier la liste des films par jour pour une salle
    :param theater:
    :return:
    """
    response = load_movies(theater)

    movies_by_date = defaultdict(list)
    for movie in response:
        scheduled_date = movie["scheduled_date"]
        movie_data = {
            key: value for key, value in movie.items() if key != "scheduled_date"
        }
        movies_by_date[scheduled_date].append(movie_data)
    return [
        {"scheduled_date": date, "movies": movies}
        for date, movies in movies_by_date.items()
    ]


# afficher les films dans une plage de date
# Rechercher les films
# -le weekend, rechercher les films qui sont du weekend
# -à partir d'une heure : recherche les films a partir de 20 h (pour un jour/ pour l'ensemble de la semaine)
# - affichier les films de la matiné / de l'aprèm / de la nuit
# rechercher les films par les catégories/genre


def display_movies_by_date(theater, scheduled_date):
    response = []
    movies = load_movies(theater)
    filtered_movies = [
        movie for movie in movies if movie["scheduled_date"] == scheduled_date
    ]

    for movie in filtered_movies:
        element = {
            "scheduled_hour": movie["scheduled_hour"],
            "movie_title": movie["title"],
            "language": movie["language"],
            "info": movie["detail"],
        }
        response.append(element)
    return response


def display_movies_by_language(theater, language):
    response = []
    movies = load_movies(theater)

    filtered_movies = [movie for movie in movies if movie["language"] == language]

    for movie in filtered_movies:
        element = {
            "scheduled_date": movie["scheduled_date"],
            "scheduled_hour": movie["scheduled_hour"],
            "movie_title": movie["title"],
            "info": movie["detail"],
        }
        response.append(element)
    return response
