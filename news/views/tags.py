from ..models import Tag
from ..common import *
from rest_framework.response import Response
from ..serializers import *
from ..models import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from django.db.utils import IntegrityError
from rest_framework.exceptions import NotFound
import logging as log
from ..swagger import token_param
from ..permissions import ReadOnlyPermission
from .viewset import CRUDViewSet


class TagsViewSet(CRUDViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [ReadOnlyPermission]
    pagination_class = PaginationClass

    @swagger_auto_schema(
        operation_description="Get list of tags",
        responses={200: "successful", "other": "something went wrong"},
    )
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except NotFound as e:
            log.error(f"NotFound error {e}")
            return Response(str(e), status=404)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Create tag",
        responses={201: "successful", "other": "something went wrong"},
        request_body=TagSerializer,
        manual_parameters=[token_param],
    )
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            log.error(f"Validation error: {e}")
            return Response(status=500)
        except IntegrityError as e:
            if "UNIQUE constraint failed" in e.args[0]:
                log.error("Tag already exists")
                return Response("Tag already exists", status=500)
            else:
                log.error(f"IntegrityError: {e}")
                return Response(status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Update tag",
        responses={200: "successful", "other": "something went wrong"},
        request_body=TagSerializer,
        manual_parameters=[token_param],
    )
    def update(self, request, *args, **kwargs):
        try:
            log.debug("ENDPOINT REACHED")
            return super().update(request, *args, **kwargs)
        except serializers.ValidationError as e:
            log.error(f"Validation error: {e}")
            return Response(status=500)
        except Tag.DoesNotExist:
            log.error("Tag doesn't exist")
            return Response("Tag doesn't exist", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Delete tag",
        responses={204: "successful", "other": "something went wrong"},
        manual_parameters=[token_param],
    )
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Tag.DoesNotExist:
            log.error("Tag doesn't exist")
            return Response("Tag doesn't exist", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)
