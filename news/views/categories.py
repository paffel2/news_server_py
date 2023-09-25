from rest_framework.response import Response
from ..serializers import CategorySerializer
from ..swagger import id_param, token_param
from ..common import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from rest_framework import serializers, generics
from django.db.utils import IntegrityError
from rest_framework.exceptions import NotFound
import logging as log
from ..permissions import ReadOnlyPermission
from .viewset import CRUDViewSet


class CategoryViewSet(CRUDViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyPermission]
    pagination_class = PaginationClass

    @swagger_auto_schema(
        operation_description="Get list of categories",
        responses={200: "successful", "other": "something went wrong"},
    )
    def list(self, request, *args, **kwargs):  # перенести в crud класс
        try:
            return super().list(request, *args, **kwargs)
        except NotFound as e:
            log.error(f"NotFound error {e}")
            return Response(str(e), status=404)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Create category",
        responses={201: "category_id: integer", "other": "something went wrong"},
        request_body=CategorySerializer,
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
                log.error("Category already exists")
                return Response("Category already exists", status=500)
            else:
                log.error(f"IntegrityError: {e}")
                return Response(status=404)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Update category",
        responses={200: "successful", "other": "something went wrong"},
        request_body=CategorySerializer,
        manual_parameters=[token_param],
    )
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except serializers.ValidationError as e:
            log.error(f"Validation error: {e}")
            return Response(status=500)
        except Category.DoesNotExist:
            log.error("Category doesn't exist")
            return Response("Category doesn't exist", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Delete category",
        responses={204: "successful", "other": "something went wrong"},
        manual_parameters=[token_param],
    )
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Category.DoesNotExist:
            log.error("Category doesn't exist")
            return Response("Category doesn't exist", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)
