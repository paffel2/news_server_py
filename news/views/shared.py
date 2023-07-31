from django.core.serializers.json import Serializer
from ..models import *

class CustomSerializer(Serializer):
    def get_dump_object(self, obj):
        return {"id":obj.id, **self._current}
    
def is_admin(token_uuid):
    token = Token.objects.get(token=token_uuid)
    return token.admin_permission #добавить проверку наличия токена, а также кастомные исключения

def is_author(token_uuid):
    token = Token.objects.get(token=token_uuid)
    return token.author_permission #возможно стоит сделать проверку по id новости и драфта