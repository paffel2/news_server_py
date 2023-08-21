from rest_framework.response import Response
from ..serializers import CategorySerializer, PutCategorySerializer
from ..swagger import id_param, token_param
from ..common import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from rest_framework import serializers, generics
from django.db.utils import IntegrityError
from rest_framework.exceptions import NotFound
import logging as log


class CategoryAPIView(generics.GenericAPIView):
    pagination_class = PaginationClass

    def get_queryset(self):
        return Category.objects.all()

    @swagger_auto_schema(
        operation_description="Get list of categories",
        responses={200: CategorySerializer, "other": "something went wrong"},
    )
    def get(self, _):
        try:
            log.info("Getting list of categories endpoint")
            log.debug("Getting list of categories from database")
            categories = Category.objects.all()
            log.debug("Serializing")
            serializer = CategorySerializer(categories, many=True)
            log.debug("Applying pagination")
            page = self.paginate_queryset(serializer.data)
            log.debug("Sending list of categories")
            return Response(page, status=200)
        except NotFound as e:
            log.error(f"NotFound error {e}")
            return Response(str(e), status=404)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Create category",
        responses={200: "category_id: integer", "other": "something went wrong"},
        request_body=PutCategorySerializer,
        manual_parameters=[token_param],
    )
    def post(self, request):
        try:
            log.info("Create category endpoint")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Checking token")
            if is_admin(token_uuid):
                log.debug("Body parsing")
                data = JSONParser().parse(request)
                log.debug("Serializing")
                serializer_req = PutCategorySerializer(data=data)
                log.debug("Validation")
                serializer_req.is_valid(raise_exception=True)
                log.debug("Saving")
                obj = serializer_req.save()
                id = obj.id
                return Response(f"category_id: {id}", status=201)
            else:
                log.error("Not admin")
                return Response(status=404)

        except serializers.ValidationError as e:
            log.error(f"Validation error: {e}")
            return Response(status=500)
        except TokenExpired:
            log.error("Token expired")
            return Response("Token expired", status=403)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
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
    def put(self, request):
        try:
            log.info("Update category endpoint")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Checking token")
            if is_admin(token_uuid):
                log.debug("Body parsing")
                data = JSONParser().parse(request)
                log.debug("Getting category from database")
                instance = Category.objects.get(id=data["id"])
                log.debug("Serializing")
                serializer = CategorySerializer(data=data, instance=instance)
                log.debug("Validation")
                serializer.is_valid(raise_exception=True)
                log.debug("Saving")
                serializer.save()
                return Response(status=201)
            else:
                log.error("Not admin")
                return Response(status=404)
        except serializers.ValidationError as e:
            log.error(f"Validation error: {e}")
            return Response(status=500)
        except TokenExpired:
            log.error("Token expired")
            return Response("Token expired", status=403)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
        except Category.DoesNotExist:
            log.error("Category doesn't exist")
            return Response("Category doesn't exist", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Delete category",
        responses={200: "successful", "other": "something went wrong"},
        manual_parameters=[id_param("category id"), token_param],
    )
    def delete(self, request):
        try:
            log.info("Delete category endpoint")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Checking token")
            if is_admin(token_uuid):
                log.debug("Getting category id from query params")
                category_id = request.GET.get("id")
                log.debug("Getting category from database")
                category = Category.objects.get(id=category_id)
                log.debug("Deleting")
                category.delete()
                return Response(status=200)
            else:
                log.error("Not admin")
                return Response(status=404)
        except TokenExpired:
            log.error("Token expired")
            return Response("Token expired", status=403)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
        except Category.DoesNotExist:
            log.error("Category doesn't exist")
            return Response("Category doesn't exist", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)
