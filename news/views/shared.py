from django.core.serializers.json import Serializer
from ..models import *
from django.core.exceptions import ObjectDoesNotExist
from news_server_py.settings import ALLOWED_HOSTS,ALLOWED_PORT,TOKEN_LIFE_TIME
import datetime
import time

class CustomSerializer(Serializer):
    def get_dump_object(self, obj):
        return {"id":obj.id, **self._current}
    
def is_admin(token_uuid):
    try:
        token = Token.objects.get(token=token_uuid)
        return token.admin_permission #добавить проверку наличия токена, а также кастомные исключения
    except ObjectDoesNotExist:
        return False

def is_author(token_uuid):
    try:
        token = Token.objects.get(token=token_uuid)
        return token.author_permission #возможно стоит сделать проверку по id новости и драфта
    except ObjectDoesNotExist:
        return False

def to_image_urls(id):
    if ALLOWED_HOSTS != []:
        str = f'http://{ALLOWED_HOSTS[0]}:{ALLOWED_PORT}/images/{id}'
        return str
    else:
        return "error" #добавить обработку исключений

def is_token_valid(token_uuid):
    try:
        token = Token.objects.get(token=token_uuid)
        now = time.mktime(datetime.datetime.now().timetuple())
        creation_time = time.mktime(token.creation_time.timetuple())
        delta = now - creation_time #разобраться с разницей во времени в базе данных и на сервере
        return delta < TOKEN_LIFE_TIME
    except ObjectDoesNotExist:
        return False