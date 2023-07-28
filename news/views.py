from django.http import HttpResponse
from .models import *
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import json

# Create your views here.

# serialization

class CategoryEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Category):
            return {"name": obj.name, "parent_category": obj.parent_category}
        return super().default(obj)


def get_categories(_):
        categories = Category.objects.all()
        
        data = serialize("json", categories, fields=('category_name', 'parent_category'))
        return HttpResponse(data, content_type="application/json")

def create_category(request):
        category = Category()
        body = json.loads(request.body.decode("utf-8"))
        category.category_name = body['category_name']
        if 'parent_category' in body:
            parent_id = int(body['parent_category'])
            parent = Category.objects.get(id=parent_id)
            category.parent_category = parent
            
        category.save()
        print(body)
        return HttpResponse(status=201)

def category_handle(request):
        if request.method == 'GET':
           return get_categories(request)
        elif request.method == 'POST':
           return create_category(request)
        