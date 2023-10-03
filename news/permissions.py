from rest_framework import permissions
from .common import is_admin, is_token_valid
from .exceptions import NotFoundException, TokenExpired
from .models import Token, Author
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


class DraftOwnsPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            token = Token.objects.get(token=token_uuid)

            if (
                obj.author.id == token.owner_id and request.method in ["PUT", "GET"]
            ) or (token.owner_id.is_staff and request.method == "DELETE"):
                if is_token_valid(token):
                    return True
                else:
                    log.error("Token expired")
                    raise NotFoundException(detail="Token expired")
            else:
                log.error("Not access")
                raise NotFoundException()
        except Token.DoesNotExist:
            log.error("Token doesn't exist")
            raise NotFoundException()

    def has_permission(self, request, view):
        if request.method in ["POST", "DELETE", "PUT", "GET"]:
            try:
                token_uuid = request.META.get("HTTP_TOKEN")
                token = Token.objects.get(token=token_uuid)
                if token.owner_id.is_staff and request.method == "DELETE":
                    pass
                else:
                    _ = Author.objects.get(id=token.owner_id)
                if is_token_valid(token):
                    return True
                else:
                    log.error("Token expired")
                    raise NotFoundException(detail="Token expired")
            except Token.DoesNotExist:
                log.error("Token doesn't exist")
                raise NotFoundException()

            except TokenExpired:
                log.error("Token expired")
                raise NotFoundException()
            except Author.DoesNotExist:
                log.error("Not author")
                raise NotFoundException()
        else:
            raise NotFoundException()


class NewsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        elif request.method in ["DELETE", "POST"]:
            try:
                token_uuid = request.META.get("HTTP_TOKEN")
                token = Token.objects.get(token=token_uuid)

                if token.owner_id.is_staff:
                    pass
                else:
                    _ = Author.objects.get(id=token.owner_id)
                if is_token_valid(token):
                    return True
                else:
                    log.error("Token expired")
                    raise NotFoundException(detail="Token expired")
            except Token.DoesNotExist:
                log.error("Token doesn't exist")
                raise NotFoundException()
            except TokenExpired:
                log.error("Token expired")
                raise NotFoundException()
            except Author.DoesNotExist:
                log.error("Not author")
                raise NotFoundException()

    def has_object_permission(self, request, view, obj):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            token = Token.objects.get(token=token_uuid)

            if (obj.author.id == token.owner_id and request.method == "POST") or (
                token.owner_id.is_staff and request.method == "DELETE"
            ):
                if is_token_valid(token):
                    return True
                else:
                    log.error("Token expired")
                    raise NotFoundException(detail="Token expired")
            else:
                log.error("Not owner")
                raise NotFoundException()
        except Token.DoesNotExist:
            log.error("Token doesn't exist")
            raise NotFoundException()


class CommentariesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        elif request.method in ["POST", "DELETE"]:
            try:
                token_uuid = request.META.get("HTTP_TOKEN")
                token = Token.objects.get(token=token_uuid)
                if is_token_valid(token):
                    pass
                else:
                    log.error("Token expired")
                    raise NotFoundException(detail="Token expired")
                if (
                    request.method == "DELETE"
                    and token.owner_id.is_staff
                    or request.method == "POST"
                ):
                    return True
                else:
                    raise NotFoundException()
            except Token.DoesNotExist:
                log.error("Token doesn't exist")
                raise NotFoundException()
            except TokenExpired:
                log.error("Token expired")
                raise NotFoundException()
            except Author.DoesNotExist:
                log.error("Not author")
                raise NotFoundException()
