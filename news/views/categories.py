from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import (
    CategorySerializer,
    PutCategorySerializer,
    id_param,
    FullCategoryInfoSerializer,
)
from ..shared import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from rest_framework import serializers, generics
from django.db.utils import IntegrityError
from rest_framework.exceptions import NotFound


class CategoryAPIView(generics.GenericAPIView):
    pagination_class = PaginationClass

    @swagger_auto_schema(
        operation_description="Get list of categories",
        responses={200: "successfull", "other": "something went wrong"},
    )
    def get(self, _):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            page = self.paginate_queryset(serializer.data)
            return Response(page, status=200)
        except NotFound as e:
            return Response(str(e), status=404)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Create category",
        responses={200: "successfull", "other": "something went wrong"},
        request_body=PutCategorySerializer,
    )
    def post(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            if is_admin(token_uuid):
                data = JSONParser().parse(request)
                serializer_req = PutCategorySerializer(data=data)
                serializer_req.is_valid(raise_exception=True)
                obj = serializer_req.save()
                id = obj.id
                return Response(f"category_id: {id}", status=201)
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
                return Response("category already exists", status=403)
            else:
                print(e.args)
                return Response(status=500)
        except Exception as e:
            # print(type(e))
            print(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Update category",
        responses={200: "successfull", "other": "something went wrong"},
        request_body=CategorySerializer,
    )
    def put(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            if is_admin(token_uuid):
                data = JSONParser().parse(request)
                serializer_req = CategorySerializer(data=data)
                serializer_req.is_valid(raise_exception=True)
                instance = Category.objects.get(id=data["id"])
                serializer = CategorySerializer(data=data, instance=instance)
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
        except Category.DoesNotExist:
            print("Category doesn't exist")
            return Response(status=500)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Delete category",
        responses={200: "successfull", "other": "something went wrong"},
        manual_parameters=[id_param("category id")],
    )
    def delete(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            if is_admin(token_uuid):
                category_id = request.GET.get("id")
                category = Category.objects.get(id=category_id)
                category.delete()
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
        except Category.DoesNotExist:
            print("Category doesn't exist")
            return Response(status=500)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)
