from django.http import HttpResponse
from ..models import User, Token, Author
from django.core.serializers.json import Serializer
import json
import django.contrib.auth.hashers as hash
from django.core.exceptions import ObjectDoesNotExist
import uuid
from .shared import *
from email_validator import validate_email, EmailNotValidError


class UserSerializer(Serializer):
    def get_dump_object(self, obj):
        return {"id":obj.id, "first_name":obj.first_name,"last_name":obj.last_name,"date_joined":obj.date_joined} 

#users

def registration(request): #изучить про шифрование и доступ
    try:
        body = json.loads(request.body.decode("utf-8"))
        user = User()
        user.first_name = body['first_name']
        user.last_name = body['last_name']
        email_info = validate_email(body['email'],check_deliverability=False)
        email = email_info.normalized
        user.email = email
        user.username = body['username']
        user.password = hash.make_password(body['password'],salt='123')
        user.save()
        return HttpResponse(status=201)
    except EmailNotValidError:
        return HttpResponse("bad email addres",status=403)

def users_list():
    data =  UserSerializer().serialize(User.objects.all())
    return HttpResponse(data, content_type="application/json")

def delete_user(request):
    body = json.loads(request.body.decode("utf-8"))
    uuid_token = body['token']
    if is_admin(uuid_token):
        user_id = int(body['id'])
        user = User.objects.get(id=user_id)
        user.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)


def user_handle(request):
    if request.method == 'GET':
        return users_list()
    elif request.method == 'POST':
        return registration(request)
    elif request.method == 'DELETE':
        return delete_user(request)
    

class TokenSerializer(Serializer):
    def get_dump_object(self, obj):
        return {"token":obj.token,"is_admin":obj.admin_permission,"is_author":obj.author_permission} 

def login(request):
    body = json.loads(request.body.decode("utf-8"))
    password_l = hash.make_password(body['password'],salt='123') #Сделать соль конфигурируемой
    username_l = body['username']
    try:
        user = User.objects.get(username=username_l,password=password_l)
        token = Token()
        token.owner_id = user
        token.admin_permission = user.is_staff
        try:
            _ = Author.objects.get(id=user.id)
            token.author_permission=True
        except ObjectDoesNotExist:
            pass
        token.token = uuid.uuid4()
        token.save()
        data = TokenSerializer().serialize([token])
        return HttpResponse(data,status=200)
    except ObjectDoesNotExist:
        return HttpResponse(status=401)