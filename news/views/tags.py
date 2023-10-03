from ..models import Tag
from ..common import *
from rest_framework.response import Response
from ..serializers import *
from ..models import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from rest_framework import serializers, generics
from django.db.utils import IntegrityError
from rest_framework.exceptions import NotFound
import logging as log
from ..swagger import token_param, id_param
from ..permissions import ReadOnlyPermission


class TagsAPIView(generics.GenericAPIView):
    pagination_class = PaginationClass
    permission_classes = [ReadOnlyPermission]

    def get_queryset(self):
        return Tag.objects.all()

    @swagger_auto_schema(
        operation_description="Get list of tags",
        responses={200: "successful", "other": "something went wrong"},
    )
    def get(self, _):
        try:
            log.info("Getting list of tags endpoint")
            log.debug("Getting list of tags from database")
            tags = Tag.objects.all()
            log.debug("Serializing")
            serializer = TagSerializer(tags, many=True)
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
        operation_description="Create tag",
        responses={200: "successful", "other": "something went wrong"},
        request_body=PutTagSerializer,
        manual_parameters=[token_param],
    )
    def post(self, request):
        try:
            log.info("Create tag endpoint")
            log.debug("Body parsing")
            data = JSONParser().parse(request)
            log.debug("Serializing")
            serializer_req = PutTagSerializer(data=data)
            log.debug("Validation")
            serializer_req.is_valid(raise_exception=True)
            log.debug("Saving")
            obj = serializer_req.save()
            id = obj.id
            return Response(f"tag_id: {id}", status=201)

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
    def put(self, request):
        try:
            log.info("Update tag endpoint")
            log.debug("Body parsing")
            data = JSONParser().parse(request)
            log.debug("Getting tag from database")
            instance = Tag.objects.get(id=data["id"])
            log.debug("Serializing")
            serializer = TagSerializer(data=data, instance=instance)
            log.debug("Validation")
            serializer.is_valid(raise_exception=True)
            log.debug("Saving")
            serializer.save()
            return Response(status=201)
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
        responses={200: "successful", "other": "something went wrong"},
        manual_parameters=[id_param("tag id"), token_param],
    )
    def delete(self, request):
        try:
            log.info("Delete tag endpoint")
            log.debug("Getting tag id from query params")
            tag_id = request.GET.get("id")
            log.debug("Getting category from database")
            tag = Tag.objects.get(id=tag_id)
            log.debug("Deleting")
            tag.delete()
            return Response(status=200)
        except Tag.DoesNotExist:
            log.error("Tag doesn't exist")
            return Response("Tag doesn't exist", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)
