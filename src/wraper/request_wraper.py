import requests
import logging
from bs4 import BeautifulSoup
from starlette.status import HTTP_400_BAD_REQUEST

from src.core.exceptions.api_exception import ApiException, ApiErrorsCode

host = "https://www.canalolympia.com/"


LOGGER = logging.getLogger(__name__)


def send_http_request(url: str) -> requests.Response:
    """
    Send network request
    :param url:
    :return: requests.Response instance
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as exc:
        LOGGER.error("Network request failed for url %s", url)
        raise exc


def load_html_data(host_str: str) -> BeautifulSoup:
    """
    Load HTML data from a given page
    :param host_str: the web page address
    :return: BeautifulSoup instance
    """
    try:
        response = send_http_request(host_str)
        return BeautifulSoup(response.text, "html.parser", from_encoding="utf-8")
    except requests.exceptions.RequestException as request_exec:
        raise ApiException(
            error_code=ApiErrorsCode.NETWORK_REQUEST_FAILED,
            status_code=request_exec.response.status_code
            if request_exec.response
            else HTTP_400_BAD_REQUEST,
            message=f"Request failed for url {host_str}",
        )
    except Exception as exec_err:
        raise exec_err
