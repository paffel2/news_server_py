from django.http import HttpResponse
from ..models import *
from django.core.serializers.json import Serializer
from django.core.serializers import *
import json
from .shared import *

def create_tag(request):
    tag = Tag()
    body = json.loads(request.body.decode("utf-8"))
    tag.tag_name = body['tag_name']  #Добавить проверки и исключения
    tag.save()
    return HttpResponse(status=201)

def get_tags():
    data =  CustomSerializer().serialize(Tag.objects.all())
    return HttpResponse(data, content_type="application/json")


def update_tag(request):
    
    body = json.loads(request.body.decode("utf-8"))
    tag_id = int(body['id'])
    tag = Tag.objects.get(id=tag_id)    
    # добавить проверку на пустоту тела запроса
    if 'tag_name' in body:
            tag_name = body['tag_name']
            tag.tag_name = tag_name #Добавить проверки и исключения
    tag.save()
    return HttpResponse(status=201)

def tags_handle(request):
    if request.method == 'GET':
        return get_tags()
    elif request.method == 'POST':
        return create_tag(request)
    elif request.method == 'PUT':
           return update_tag(request)
