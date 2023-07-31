from django.http import HttpResponse
from ..models import User
from django.core.serializers.json import Serializer
import json
import django.contrib.auth.hashers as hash
from django.core.exceptions import ObjectDoesNotExist

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
    user.password = hash.make_password(body['password'],salt='123')
    user.save()
    return HttpResponse(status=201)

def users_list(request):
    data =  UserSerializer().serialize(User.objects.all())
    return HttpResponse(data, content_type="application/json")

def delete_user(request):
    body = json.loads(request.body.decode("utf-8"))
    user_id = int(body['id'])
    user = User.objects.get(id=user_id)
    user.delete()
    return HttpResponse(status=200)

def user_handle(request):
    if request.method == 'GET':
        return users_list(request)
    elif request.method == 'POST':
        return registration(request)
    elif request.method == 'DELETE':
        return delete_user(request)
    

def login(request):
    body = json.loads(request.body.decode("utf-8"))
    password_l = hash.make_password(body['password'],salt='123') #Сделать соль конфигурируемой
    username_l = body['username']
    try:
        _ = User.objects.get(username=username_l,password=password_l)
        return HttpResponse(status=200)
    except ObjectDoesNotExist:
        return HttpResponse(status=401)
