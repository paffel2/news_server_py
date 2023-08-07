from ..models import Tag
from .shared import *
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import json
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from rest_framework import serializers


#id_param = openapi.Parameter('id', openapi.IN_QUERY, description="object id", type=openapi.TYPE_INTEGER)

class TagsAPIView(APIView):
    #serializer_class = TagSerializer
    @swagger_auto_schema(operation_description="Get list of tags", responses={200: 'successfull', 'other':'something went wrong'})
    def get(self,_):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags,many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Create tag", responses={200: 'successfull', 'other':'something went wrong'},request_body=PutTagSerializer)
    def post(self,request):
        try:
            data = JSONParser().parse(request)
            serializer_req = PutTagSerializer(data=data)
            if serializer_req.is_valid():
                serializer_req.save()
                return Response(status=201)
            else:
                Response("bad json format", status=403)
        except AssertionError:
            print("tag not added")
            return Response(status=404)
        except serializers.ValidationError as e:
            print(e) #добавить описание логам
            return Response(status=500)
        except Exception as e:
            print(e)
            return Response(status=500)
    
    @swagger_auto_schema(operation_description="Update tag", responses={200: 'successfull', 'other':'something went wrong'},request_body=TagSerializer)
    def put(self,request):
        try:
            data = JSONParser().parse(request)
            serializer_req = TagSerializer(data=data)
            if serializer_req.is_valid():
                instance = Tag.objects.get(id=data['id'])
                serializer = TagSerializer(data=data,instance=instance)
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
    
    @swagger_auto_schema(operation_description="Delete tag", responses={200: 'successfull', 'other':'something went wrong'},manual_parameters=[id_param('tag id')])
    def delete(self,request):
        tag_id = request.GET.get('id')
        tag = Tag.objects.get(id=tag_id)
        tag.delete()
        return Response(status=200)