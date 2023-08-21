from django.core.serializers.json import Serializer
from .models import *
from news_server_py.settings import TOKEN_LIFE_TIME
import datetime
import time
from .exceptions import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomSerializer(Serializer):
    def get_dump_object(self, obj):
        return {"id": obj.id, **self._current}


def is_admin(token_uuid):
    token = Token.objects.get(token=token_uuid)
    return token.owner_id.is_staff and is_token_valid(token)


def is_author(token_uuid):
    try:
        token = Token.objects.get(token=token_uuid)
        _ = Author.objects.get(id=token.owner_id)
        return is_token_valid(token)
    except Author.DoesNotExist:
        return False


def is_token_valid(token):
    now = time.mktime(datetime.datetime.now().timetuple())
    creation_time = time.mktime(token.creation_time.timetuple())
    delta = now - creation_time
    if delta < TOKEN_LIFE_TIME:
        return True
    else:
        raise TokenExpired()


def is_news_owner(token_uuid, news_id):
    try:
        token = Token.objects.get(token=token_uuid)
        news = News.objects.get(id=news_id)
        author = Author.objects.get(id=token.owner_id)
        return is_token_valid(token) and author == news.author
    except Author.DoesNotExist:
        return False


class PaginationClass(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(data)

    def get_paginated_response_schema(self, schema):
        return schema


def from_str_to_list_of_ints(string):
    if len(string) < 3:
        raise ToShortString
    else:
        string_without_brackets = string[1:-1]
        list_of_ints = [int(x) for x in string_without_brackets.split(",")]
        return list_of_ints
