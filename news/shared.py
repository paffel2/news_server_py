from django.core.serializers.json import Serializer
from .models import *
from news_server_py.settings import ALLOWED_HOSTS,ALLOWED_PORT,TOKEN_LIFE_TIME
import datetime
import time
from .exceptions import *

class CustomSerializer(Serializer):
    def get_dump_object(self, obj):
        return {"id":obj.id, **self._current}
    
def is_admin(token_uuid):
        token = Token.objects.get(token=token_uuid)
        return token.admin_permission and is_token_valid(token)
    

def is_author(token_uuid):
        token = Token.objects.get(token=token_uuid)
        return token.author_permission and is_token_valid(token) #возможно стоит сделать проверку по id новости и драфта

def to_image_urls(id):
    if ALLOWED_HOSTS != []:
        str = f'http://{ALLOWED_HOSTS[0]}:{ALLOWED_PORT}/api/images/{id}'
        return str
    else:
        return "error" #добавить обработку исключений

def is_token_valid(token):
        now = time.mktime(datetime.datetime.now().timetuple())
        creation_time = time.mktime(token.creation_time.timetuple())
        delta = now - creation_time #разобраться с разницей во времени в базе данных и на сервере
        if delta < TOKEN_LIFE_TIME:
            return True
        else:
            raise TokenExpired()


def is_news_owner(token_uuid,news_id):
    token = Token.objects.get(token=token_uuid)
    news = News.objects.get(id=news_id)
    author = Author.objects.get(id=token.owner_id)
    return is_token_valid(token) and author == news.author