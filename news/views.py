from django.http import HttpResponse
from .models import *
from django.core.serializers.json import Serializer
from django.core.serializers import *
import json

# Create your views here.

# serialization

class CustomSerializer(Serializer):
    def get_dump_object(self, obj):
        return {"id":obj.id, **self._current}
    
# endpoints

#categories
def create_category(request):
        category = Category()
        body = json.loads(request.body.decode("utf-8"))
        category.category_name = body['category_name'] #Добавить проверки и исключения
        if 'parent_category' in body:
            parent_id = int(body['parent_category'])
            parent = Category.objects.get(id=parent_id)
            category.parent_category = parent #Добавить проверки и исключения
            
        category.save()
        return HttpResponse(status=201)

def get_categories():
        data = CustomSerializer().serialize(Category.objects.all())
        return HttpResponse(data, content_type="application/json")

def update_category(request):
    
    body = json.loads(request.body.decode("utf-8"))
    category_id = int(body['id'])
    category = Category.objects.get(id=category_id)
    #Добавить проверку что тело не пустое
    if 'parent_category' in body:
            parent_id = int(body['parent_category'])
            parent = Category.objects.get(id=parent_id)
            category.parent_category = parent #Добавить проверки и исключения
    
    if 'category_name' in body:
            category_name = body['category_name']
            category.category_name = category_name #Добавить проверки и исключения
    category.save()
    return HttpResponse(status=201)

#tags 
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


# handlers - возможно стоит разнести по модулям
def category_handle(request):
        if request.method == 'GET':
           return get_categories()
        elif request.method == 'POST':
           return create_category(request)
        elif request.method == 'PUT':
           return update_category(request)
        
def tags_handle(request):
    if request.method == 'GET':
        return get_tags()
    elif request.method == 'POST':
        return create_tag(request)
    elif request.method == 'PUT':
           return update_tag(request)