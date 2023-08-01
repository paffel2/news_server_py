from django.http import HttpResponse
from ..models import Category
import json
from .shared import *


def create_category(body):
        #body = json.loads(request.body.decode("utf-8"))
        #uuid_token = body['token']
        #if is_admin(uuid_token):
        category = Category()
        #        body = json.loads(request.body.decode("utf-8"))
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

def update_category(body):
    
    #body = json.loads(request.body.decode("utf-8"))
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

def delete_category(body):
    #body = json.loads(request.body.decode("utf-8"))
    category_id = int(body['id'])
    category = Category.objects.get(id=category_id)
    category.delete()
    return HttpResponse(status=200)

def category_handle(request):
        if request.method == 'GET':
           return get_categories()
        else:
           body = json.loads(request.body.decode("utf-8"))
           uuid_token = body['token']
           if is_admin(uuid_token):
                if request.method == 'POST':
                        return create_category(body)
                elif request.method == 'PUT':
                        return update_category(body)
                elif request.method == 'DELETE':
                        return delete_category(body)
           else:
                return HttpResponse(status=404)