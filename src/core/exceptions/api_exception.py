class ApiErrorsCode:
    NETWORK_REQUEST_FAILED = 10
    FAILED_TO_LOAD_HTML_DATA = 20

    THEATER_NOT_FOUND = 30
    THEATER_LOAD_FAILED = 31

    MOVIE_NOT_FOUND = 40
    MOVIE_LOAD_FAILED = 41


class ApiException(Exception):
    def __init__(self, status_code: int, error_code: int, message: str):
        super().__init__(message)
        self.__status_code = status_code
        self.__error_code = error_code
        self.__message = message

    @property
    def message(self):
        return {"error_code": self.__error_code, "message": self.__message}

    @property
    def status_code(self):
        return self.__status_code

    @property
    def error_code(self):
        return self.__error_code

    @staticmethod
    def server_internal_error() -> dict:
        return {"error_code": 500, "message": "server internal error"}
