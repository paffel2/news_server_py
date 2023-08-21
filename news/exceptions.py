class TokenExpired(Exception):
    message = "Token expired"


class HostNotAllowed(Exception):
    message = "Host not allowed"


class ToShortString(Exception):
    message = "String is too short for conversion into list "
