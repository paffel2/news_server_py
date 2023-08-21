from rest_framework.response import Response
from ..serializers import PutAuthorSerializer, AuthorInfo, id_param, token_param
from ..common import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from rest_framework import serializers, generics
from django.db.utils import IntegrityError
from rest_framework.exceptions import NotFound
import logging as log


class AuthorsAPIView(generics.GenericAPIView):
    pagination_class = PaginationClass

    def get_queryset(self):
        return Author.objects.all()

    @swagger_auto_schema(
        operation_description="Get list of authors",
        responses={200: AuthorInfo, "other": "something went wrong"},
    )
    def get(self, _):
        try:
            log.info("Get authors endpoint")
            authors = Author.objects.all()
            serializer = AuthorInfo(authors, many=True)
            page = self.paginate_queryset(serializer.data)
            log.info("List of authors sending")
            return Response(page, status=200)
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
    def post(self, request):
        try:
            log.info("Create author endpoint")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Checking token")
            if is_admin(token_uuid):
                log.debug("Body parsing")
                data = JSONParser().parse(request)
                log.debug("Serializing")
                serializer_req = PutAuthorSerializer(data=data)
                log.debug("Validation of author info")
                serializer_req.is_valid(raise_exception=True)
                log.debug("Saving author")
                serializer_req.save()
                return Response(status=201)
            else:
                log.error("Not admin")
                return Response(status=404)
        except serializers.ValidationError as e:
            log.error(e)
            return Response(status=500)
        except IntegrityError as e:
            if "FOREIGN KEY constraint failed" in e.args[0]:
                log.error(e.args[0])
                return Response("user not exists", status=500)
            log.error(e)
            return Response(status=404)
        except TokenExpired:
            log.error("Token expired")
            return Response("Token expired", status=403)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Update author",
        responses={200: "successful", "other": "something went wrong"},
        request_body=PutAuthorSerializer,
        manual_parameters=[token_param],
    )
    def put(self, request):
        try:
            log.info("Update author endpoint")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Checking token")
            if is_admin(token_uuid):
                log.debug("Body parsing")
                data = JSONParser().parse(request)
                log.debug("Getting author from database")
                instance = Author.objects.get(id=data["id"])
                log.debug("Serializing")
                serializer = PutAuthorSerializer(data=data, instance=instance)
                log.debug("Validation of author info")
                serializer.is_valid(raise_exception=True)
                log.debug("Saving author")
                serializer.save()
                return Response(status=201)
            else:
                log.error("Not admin")
                return Response(status=404)

        except serializers.ValidationError as e:
            log.error(f"ValidationError: {e}")
            return Response(status=500)
        except IntegrityError as e:
            if "FOREIGN KEY constraint failed" in e.args[0]:
                log.error(e.args[0])
                return Response("user not exists", status=403)
            log.error(f"IntegrityError {e}")
            return Response(status=500)
        except TokenExpired:
            log.error("Token expired")
            return Response("Token expired", status=403)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
        except Author.DoesNotExist:
            log.error("Author doesn't exist")
            return Response(status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Delete author",
        responses={200: "successful", "other": "something went wrong"},
        manual_parameters=[id_param("author id"), token_param],
    )
    def delete(self, request):
        try:
            log.info("Deleting author endpoint")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Checking token")
            if is_admin(token_uuid):
                log.debug("Getting author id from parameters")
                author_id = request.GET.get("id")
                log.debug("Getting author from database")
                author = Author.objects.get(id=author_id)
                log.debug("Deleting author")
                author.delete()
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
        except Author.DoesNotExist:
            log.error("User is not author")
            return Response("User is not author", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)
