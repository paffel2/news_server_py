from django.http import HttpResponse
from ..models import *
from django.core.serializers.json import Serializer
from django.core.serializers import *
import json

class UserSerializer(Serializer):
    def get_dump_object(self, obj):
        return {"id":obj.id, "first_name":obj.first_name,"last_name":obj.last_name,"date_joined":obj.date_joined} 

#users

def registration(request): #изучить про шифрование и доступ
    body = json.loads(request.body.decode("utf-8"))
    user = User()
    user.first_name = body['first_name']
    user.last_name = body['last_name']
    user.email = body['email']
    user.username = body['username']
    user.password = body['password']
    user.save()
    return HttpResponse(status=201)

def users_list(request):
    data =  UserSerializer().serialize(User.objects.all())
    return HttpResponse(data, content_type="application/json")

def user_handle(request):
    if request.method == 'GET':
        return users_list(request)
    elif request.method == 'POST':
        return registration(request)