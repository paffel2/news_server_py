from django.core.serializers.json import Serializer

class CustomSerializer(Serializer):
    def get_dump_object(self, obj):
        return {"id":obj.id, **self._current}