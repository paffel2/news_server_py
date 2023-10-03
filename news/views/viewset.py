from rest_framework import viewsets, mixins
import logging as log
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


class CRUDViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    http_method_names = ["get", "post", "put", "delete"]

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except NotFound as e:
            log.error(f"NotFound error {e}")
            return Response(str(e), status=404)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=500)
