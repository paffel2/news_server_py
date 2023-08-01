from django.core.serializers.json import Serializer
from ..models import *
from django.core.exceptions import ObjectDoesNotExist


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