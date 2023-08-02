from django.http import HttpResponse
from ..models import User, Token, Author
from django.core.serializers.json import Serializer
import json
import django.contrib.auth.hashers as hash
from django.core.exceptions import ObjectDoesNotExist
import uuid
from .shared import *
from email_validator import validate_email, EmailNotValidError
from news_server_py.settings import SALT


class UserShortInfoSerializer(Serializer):
    def get_dump_object(self, obj):
        return {"id":obj.id, "first_name":obj.first_name,"last_name":obj.last_name,"date_joined":obj.date_joined} 

class UserInfoSerializer(Serializer):
    def get_dump_object(self, obj):
        return {"id":obj.id, "first_name":obj.first_name,"last_name":obj.last_name,"date_joined":obj.date_joined, "email":obj.email,"is_admin":obj.is_staff} 


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
        user.password = hash.make_password(body['password'],salt=SALT)
        try:
            user.save()
        except ValueError as e:
            #добавить логи
            return HttpResponse(status=403)
        else:
            return HttpResponse(status=201)
    except EmailNotValidError:
        return HttpResponse("bad email addres",status=403)
    except json.JSONDecodeError:
        return HttpResponse("bad json format", status=403)
    except KeyError as e:
        return HttpResponse(f'not found field {e}',status=403)
    except Exception as e:
        return HttpResponse(status=500)

def users_list(_):
    try:
        data =  UserShortInfoSerializer().serialize(User.objects.all())
    except Exception as e:
        return HttpResponse(status=500)
    else:
        return HttpResponse(data, content_type="application/json")

def delete_user(request):
    token_uuid = request.META.get('HTTP_TOKEN')
    if is_admin(token_uuid):
        try:
            body = json.loads(request.body.decode("utf-8"))
            user_id = int(body['id'])
            user = User.objects.get(id=user_id)
            user.delete()
            return HttpResponse(status=200)
        except json.JSONDecodeError:
            return HttpResponse("bad json format", status=403)
        except KeyError as e:
            return HttpResponse(f'not found field {e}',status=403)
        except Exception as e:
            return HttpResponse(e,status=500)
    else:
        return HttpResponse(status=404)


def user_handle(request):
    if request.method == 'GET':
        return get_own_user_information(request)
    elif request.method == 'POST':
        return registration(request)
    elif request.method == 'DELETE':
        return delete_user(request)
    

class TokenSerializer(Serializer):
    def get_dump_object(self, obj):
        return {"token":obj.token,"is_admin":obj.admin_permission,"is_author":obj.author_permission} 

def login(request):
    body = json.loads(request.body.decode("utf-8"))
    password_l = hash.make_password(body['password'],salt=SALT)
    username_l = body['username']
    try:
        user = User.objects.get(username=username_l,password=password_l)
    except ObjectDoesNotExist:
        return HttpResponse("wrong username or password", status=401)
    else:
        token = Token()
        token.owner_id = user
        token.admin_permission = user.is_staff
        try:
            _ = Author.objects.get(id=user.id)
            token.author_permission=True
        except ObjectDoesNotExist:
            pass
        except Exception:
            return HttpResponse(status=500)
        token.token = uuid.uuid4()
        try:
            token.save()
        except Exception:
            return HttpResponse(status=500)
        else:
            data = TokenSerializer().serialize([token])
            struct = json.loads(data)
            returning_data = json.dumps(struct[0])
            return HttpResponse(returning_data,status=200)
    
def get_own_user_information(request):
    token_uuid = request.META.get('HTTP_TOKEN')
    token = Token.objects.get(token=token_uuid)
    user_info = User.objects.get(id=token.owner_id.id)
    #здесь используется костыль для сериализации данных в json
    data = UserInfoSerializer().serialize([user_info]) #сначала сериализуем объект, упаковав его в список, так как требуется, чтобы объект был вгутри iterable
    struct = json.loads(data) #десериализуем объект обратно
    returning_data = json.dumps(struct[0]) #сериализуем его снова (вариант с преобразованием model_to_dict не работает, так как вылетает ошибка при преобразовании времени и uuid)
    #костыль используется для того, чтобы избежать списка
    #возможно стоило использовать что-то другое
    return HttpResponse(returning_data,content_type="application/json")

def check_token(request): #тестовый эндпоинт, будет удален, а функционал добавлен, где требуется проверка токена
    token_uuid = request.META.get('HTTP_TOKEN')
    result = is_token_valid(token_uuid)
    return HttpResponse(result) 