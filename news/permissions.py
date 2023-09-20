from rest_framework import permissions
from .common import is_admin, is_token_valid
from .exceptions import NotFoundException, TokenExpired
from .models import Token
import logging as log


class GenericOnlyAdminPermission(permissions.BasePermission):
    def __init__(self, safe_methods) -> None:
        self.safe_methods = safe_methods
        super().__init__()

    def has_permission(self, request, view):
        if request.method in self.safe_methods:
            return True
        else:
            try:
                token_uuid = request.META.get("HTTP_TOKEN")
                token = Token.objects.get(token=token_uuid)
                if token.owner_id.is_staff:
                    if is_token_valid(token):
                        return True
                    else:
                        log.error("Token expired")
                        raise NotFoundException(detail="Token expired")
                else:
                    log.error("Not admin")
                    raise NotFoundException()
            except Token.DoesNotExist:
                log.error("Token doesn't exist")
                raise NotFoundException()

            except TokenExpired:
                log.error("Token expired")
                raise NotFoundException()


class ReadOnlyPermission(GenericOnlyAdminPermission):
    def __init__(self) -> None:
        super().__init__(["GET"])


class GetAndPostPermission(GenericOnlyAdminPermission):
    def __init__(self) -> None:
        super().__init__(["GET", "POST"])
