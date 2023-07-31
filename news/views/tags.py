from django.http import HttpResponse
from ..models import Tag
import json
from .shared import *

def create_tag(body):
    tag = Tag()
    #body = json.loads(request.body.decode("utf-8"))
    tag.tag_name = body['tag_name']  #Добавить проверки и исключения
    tag.save()
    return HttpResponse(status=201)

def get_tags():
    data =  CustomSerializer().serialize(Tag.objects.all())
    return HttpResponse(data, content_type="application/json")


def update_tag(body):
    
    #body = json.loads(request.body.decode("utf-8"))
    tag_id = int(body['id'])
    tag = Tag.objects.get(id=tag_id)    
    # добавить проверку на пустоту тела запроса
    if 'tag_name' in body:
            tag_name = body['tag_name']
            tag.tag_name = tag_name #Добавить проверки и исключения
    tag.save()
    return HttpResponse(status=201)

def delete_tag(body):
    #body = json.loads(request.body.decode("utf-8"))
    tag_id = int(body['id'])
    tag = Tag.objects.get(id=tag_id)
    tag.delete()
    return HttpResponse(status=200)

def tags_handle(request):
    if request.method == 'GET':
        return get_tags()
    else:
        body = json.loads(request.body.decode("utf-8"))
        uuid_token = body['token']
        if is_admin(uuid_token):
            if request.method == 'POST':
                return create_tag(body)
            elif request.method == 'PUT':
                return update_tag(body)
            elif request.method == 'DELETE':
                return delete_tag(body)
        else:
            return HttpResponse(status=404)
