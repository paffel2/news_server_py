from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import PutAuthorSerializer, AuthorInfo, id_param
from ..shared import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from rest_framework import serializers, generics
from django.db.utils import IntegrityError
from rest_framework.exceptions import NotFound


class AuthorsAPIView(generics.GenericAPIView):
    pagination_class = PaginationClass

    @swagger_auto_schema(
        operation_description="Get list of authors",
        responses={200: "successfull", "other": "something went wrong"},
    )
    def get(self, _):
        try:
            authors = Author.objects.all()
            serializer = AuthorInfo(authors, many=True)
            page = self.paginate_queryset(serializer.data)
            return Response(page, status=200)
        except NotFound as e:
            return Response(str(e), status=404)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Create author",
        responses={201: "successfull", "other": "something went wrong"},
        request_body=PutAuthorSerializer,
    )
    def post(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            if is_admin(token_uuid):
                data = JSONParser().parse(request)
                serializer_req = PutAuthorSerializer(data=data)
                serializer_req.is_valid(raise_exception=True)
                serializer_req.save()
                return Response(status=201)
            else:
                print("Not admin")
                return Response(status=404)
        except serializers.ValidationError as e:
            print(e)
            return Response(status=500)
        except IntegrityError as e:
            if "FOREIGN KEY constraint failed" in e.args[0]:
                return Response("user not exists", status=403)
            return Response(status=404)
        except TokenExpired:
            print("Token expired")  # сделать нормальные логи
            return Response(status=404)
        except Token.DoesNotExist:
            print("Token not exist")  # сделать нормальные логи
            return Response(status=404)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Update author",
        responses={200: "successfull", "other": "something went wrong"},
        request_body=PutAuthorSerializer,
    )
    def put(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            if is_admin(token_uuid):
                data = JSONParser().parse(request)
                serializer_req = PutAuthorSerializer(data=data)
                serializer_req.is_valid(raise_exception=True)
                instance = Author.objects.get(id=data["id"])
                serializer = PutAuthorSerializer(data=data, instance=instance)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(status=201)
            else:
                print("Not admin")
                return Response(status=404)

        except serializers.ValidationError as e:
            print("ValidationError:")
            print(e)  # добавить описание логам
            return Response(status=500)
        except IntegrityError as e:
            if "FOREIGN KEY constraint failed" in e.args[0]:
                return Response("user not exists", status=403)
            return Response(status=404)
        except TokenExpired:
            print("Token expired")  # сделать нормальные логи
            return Response(status=404)
        except Token.DoesNotExist:
            print("Token not exist")  # сделать нормальные логи
            return Response(status=404)
        except Author.DoesNotExist:
            print("Author doesn't exist")
            return Response(status=404)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Delete author",
        responses={200: "successfull", "other": "something went wrong"},
        manual_parameters=[id_param("author id")],
    )
    def delete(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            if is_admin(token_uuid):
                author_id = request.GET.get("id")
                author = Author.objects.get(id=author_id)
                author.delete()
                return Response(status=200)
            else:
                print("Not admin")
                return Response(status=404)
        except TokenExpired:
            print("Token expired")  # сделать нормальные логи
            return Response(status=404)
        except Token.DoesNotExist:
            print("Token not exist")  # сделать нормальные логи
            return Response(status=404)
        except Author.DoesNotExist:
            print("User is not author")
            return Response(status=404)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=404)
