from rest_framework.views import APIView
from ..common import *
from django.http import FileResponse
from drf_yasg.utils import swagger_auto_schema
import logging as log


class GetImageAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get image by id",
    )
    def get(self, _, image_id):
        try:
            log.info("Getting image endpoint")
            log.debug("Get image from database")
            image = Image.objects.get(id=image_id)
            log.debug("sending")
            return FileResponse(image.image)
        except Image.DoesNotExist:
            log.error("Image doesn't exist")
            return Response("Image doesn't exist", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)
