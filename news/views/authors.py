from django.http import HttpResponse
from ..models import *
from django.core.serializers.json import Serializer
import json
from django.core.exceptions import ObjectDoesNotExist

class AuthorSerializer(Serializer):
    def get_dump_object(self, obj):
        return {"id":obj.id.id, "first_name":obj.id.first_name,"last_name":obj.id.last_name,"bio":obj.bio}

def make_author(request):
    author = Author()
    body = json.loads(request.body.decode("utf-8"))
    user_id = int(body['id'])
    if 'bio' in body:
        bio = body['bio']
        author.bio = bio
    user = User.objects.get(id=user_id)
    author.id = user
    author.save()
    return HttpResponse(status=201)

def check_author(request): #служебный энд, возможно стоит его просто убрать и переработать
    body = json.loads(request.body.decode("utf-8"))
    user_id = int(body['id'])
    try:
        _ = Author.objects.get(id=user_id)
        return HttpResponse('true')
    except ObjectDoesNotExist:
        return HttpResponse('false')

def get_all_authors():
    authors = Author.objects.select_related('id')
    data = AuthorSerializer().serialize(authors)
    return HttpResponse(data, content_type="application/json")

def delete_author(request):
    body = json.loads(request.body.decode("utf-8"))
    user_id = int(body['id'])
    author = Author.objects.get(id=user_id)
    author.delete()
    return HttpResponse(status=200)

def update_author(request):
    
    body = json.loads(request.body.decode("utf-8"))
    author_id = int(body['id'])
    author = Author.objects.get(id=author_id)
    if 'bio' in body:
            bio = body['bio']
            author.bio = bio
    author.save()
    return HttpResponse(status=200)
    
def author_handle(request):
    if request.method == 'GET':
        return get_all_authors()
        #return check_author(request)
    elif request.method == 'POST':
        return make_author(request)
    elif request.method == 'DELETE':
        return delete_author(request)
    elif request.method == 'PUT':
        return update_author(request)
