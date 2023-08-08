from django.core.exceptions import ObjectDoesNotExist

class TokenExpired(Exception):
    message = "Token expired"

class TokenNotExist(ObjectDoesNotExist):
    pass