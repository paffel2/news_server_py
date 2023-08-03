from ..models import Tag
from .shared import *
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import json
from drf_yasg.utils import swagger_auto_schema

class TagsAPIView(APIView):
    serializer_class = TagSerializer

    def get(self,_):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        body = json.loads(request.body.decode("utf-8"))
        tag = Tag()
        tag.tag_name = body['tag_name']  #Добавить проверки и исключения
        tag.save()
        return Response(status=201)
    
    def put(self,request):
        body = json.loads(request.body.decode("utf-8"))
        tag_id = int(body['id'])
        tag = Tag.objects.get(id=tag_id) 
        tag.tag_name = body['tag_name']  #Добавить проверки и исключения
        tag.save()
        return Response(status=201)
    
    def delete(self,request):
        body = json.loads(request.body.decode("utf-8"))
        tag_id = int(body['id'])
        tag = Tag.objects.get(id=tag_id)
        tag.delete()
        return Response(status=200)