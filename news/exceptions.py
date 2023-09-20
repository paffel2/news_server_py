from rest_framework.exceptions import APIException
from rest_framework import status


class TokenExpired(Exception):
    message = "Token expired"


class HostNotAllowed(Exception):
    message = "Host not allowed"


class ToShortString(Exception):
    message = "String is too short for conversion into list "


class NotFoundException(APIException):
    """
    raises API exceptions with custom messages and custom status codes
    """

    status_code = status.HTTP_404_NOT_FOUND
    default_code = "error"

    def __init__(self, detail="Not found", status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code
