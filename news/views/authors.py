from rest_framework.response import Response
from ..serializers import PutAuthorSerializer, AuthorInfo
from ..swagger import token_param
from ..common import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from django.db.utils import IntegrityError
from rest_framework.exceptions import NotFound
import logging as log
from ..permissions import ReadOnlyPermission
from .viewset import CRUDViewSet


class AuthorsViewSet(CRUDViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorInfo
    permission_classes = [ReadOnlyPermission]
    pagination_class = PaginationClass

    def get_serializer_class(self):
        if self.action == "create":
            return PutAuthorSerializer
        else:
            return self.serializer_class

    @swagger_auto_schema(
        operation_description="Get list of authors",
        responses={200: AuthorInfo, "other": "something went wrong"},
    )
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except NotFound as e:
            log.error(e)
            return Response(str(e), status=404)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Create author",
        responses={201: "successful", "other": "something went wrong"},
        request_body=PutAuthorSerializer,
        manual_parameters=[token_param],
    )
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            log.error(f"ValidationError: {e}")
            return Response(status=500)
        except IntegrityError as e:
            if "FOREIGN KEY constraint failed" in e.args[0]:
                log.error(e.args[0])
                return Response("user not exists", status=500)
            log.error(e)
            return Response(status=404)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Update author",
        responses={200: "successful", "other": "something went wrong"},
        request_body=AuthorInfo,
        manual_parameters=[token_param],
    )
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except serializers.ValidationError as e:
            log.error(f"ValidationError: {e}")
            return Response(status=500)
        except IntegrityError as e:
            if "FOREIGN KEY constraint failed" in e.args[0]:
                log.error(e.args[0])
                return Response("user not exists", status=403)
            log.error(f"IntegrityError {e}")
            return Response(status=500)
        except Author.DoesNotExist:
            log.error("Author doesn't exist")
            return Response(status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Delete author",
        responses={204: "successful", "other": "something went wrong"},
        manual_parameters=[token_param],
    )
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Author.DoesNotExist:
            log.error("User is not author")
            return Response("User is not author", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)
