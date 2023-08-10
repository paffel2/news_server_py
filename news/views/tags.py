from ..models import Tag
from ..shared import *
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from django.db.utils import IntegrityError
from django.core.paginator import Paginator


class TagsAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get list of tags",
        responses={200: "successfull", "other": "something went wrong"},
    )
    def get(self, request):
        try:
            page_param = request.GET.get("page")
            if page_param != None:
                page = int(page_param)
            else:
                page = 1
            tags = Tag.objects.all()
            paginator = Paginator(tags, 10)
            if page <= paginator.num_pages:
                page_obj = paginator.get_page(page)
            else:
                page_obj = []
            serializer = TagSerializer(page_obj, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response("bad page parameter", status=400)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Create tag",
        responses={200: "successfull", "other": "something went wrong"},
        request_body=PutTagSerializer,
    )
    def post(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            if is_admin(token_uuid):
                data = JSONParser().parse(request)
                serializer_req = PutTagSerializer(data=data)
                serializer_req.is_valid(raise_exception=True)
                serializer_req.save()
                return Response(status=201)
            else:
                print("Not admin")
                return Response(status=404)

        except serializers.ValidationError as e:
            print(e)  # добавить описание логам
            return Response(status=500)
        except TokenExpired:
            print("Token expired")  # сделать нормальные логи
            return Response(status=404)
        except Token.DoesNotExist:
            print("Token not exist")  # сделать нормальные логи
            return Response(status=404)
        except IntegrityError as e:
            if "UNIQUE constraint failed" in e.args[0]:
                return Response("tag already exists", status=403)
            else:
                print(e.args)
                return Response(status=500)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Update tag",
        responses={200: "successfull", "other": "something went wrong"},
        request_body=TagSerializer,
    )
    def put(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            if is_admin(token_uuid):
                data = JSONParser().parse(request)
                serializer_req = TagSerializer(data=data)
                serializer_req.is_valid(raise_exception=True)
                instance = Tag.objects.get(id=data["id"])
                serializer = TagSerializer(data=data, instance=instance)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(status=201)
            else:
                print("Not admin")
                return Response(status=404)
        except serializers.ValidationError as e:
            print(e)  # добавить описание логам
            return Response(status=500)
        except TokenExpired:
            print("Token expired")  # сделать нормальные логи
            return Response(status=404)
        except Token.DoesNotExist:
            print("Token not exist")  # сделать нормальные логи
            return Response(status=404)
        except Tag.DoesNotExist:
            print("Tag doesn't exist")
            return Response(status=500)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Delete tag",
        responses={200: "successfull", "other": "something went wrong"},
        manual_parameters=[id_param("tag id")],
    )
    def delete(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            if is_admin(token_uuid):
                tag_id = request.GET.get("id")
                tag = Tag.objects.get(id=tag_id)
                tag.delete()
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
        except Tag.DoesNotExist:
            print("Tag doesn't exist")
            return Response(status=500)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)
