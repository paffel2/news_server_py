from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import CategorySerializer, PutCategorySerializer, id_param
from ..views.shared import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from rest_framework import serializers


class CategoryAPIView(APIView):
    
    @swagger_auto_schema(operation_description="Get list of categories", responses={200: 'successfull', 'other':'something went wrong'})
    def get(self, _):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(operation_description="Create category", responses={200: 'successfull', 'other':'something went wrong'},request_body=PutCategorySerializer)
    def post(self,request):
        try:
            data = JSONParser().parse(request)
            serializer_req = PutCategorySerializer(data=data)
            if serializer_req.is_valid(raise_exception=True):
                serializer_req.save()
                return Response(status=201)
            else:
                return Response("bad json format", status=403)
        except serializers.ValidationError as e:
            print(e) #добавить описание логам
            return Response(status=500)
        except Exception as e:
            print(e)
            return Response(status=500)

    @swagger_auto_schema(operation_description="Update category", responses={200: 'successfull', 'other':'something went wrong'},request_body=CategorySerializer)
    def put(self,request):
        try:
            data = JSONParser().parse(request)
            serializer_req = CategorySerializer(data=data)
            if serializer_req.is_valid():
                instance = Category.objects.get(id=data['id'])
                serializer = CategorySerializer(data=data,instance=instance)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(status=201)
            else:
                Response("bad json format", status=403)
        except serializers.ValidationError as e:
            print(e) #добавить описание логам
            return Response(status=500)
        except Exception as e:
            print(e)
            return Response(status=500)

    @swagger_auto_schema(operation_description="Delete category", responses={200: 'successfull', 'other':'something went wrong'},manual_parameters=[id_param('category id')])
    def delete(self,request):
        category_id = request.GET.get('id')
        category = Category.objects.get(id=category_id)
        category.delete()
        return Response(status=200)