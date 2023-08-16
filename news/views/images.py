from rest_framework.response import Response
from rest_framework.views import APIView
from ..shared import *
from django.http import FileResponse
from ..serializers import ImageToUrlSerializer
from drf_yasg.utils import swagger_auto_schema


class ImagesAPIView(APIView):  # использовалось для тестов, можно удалить
    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            id = str(form.instance.id)
            return Response(id, status=200)
        else:
            print("invalid")
            return Response(status=404)

    def get(self, _):
        images = Image.objects.all()
        serializer = ImageToUrlSerializer(images, many=True)
        return Response(serializer.data)

    def delete(self, request):
        image_id = request.GET.get("id")
        image = Image.objects.get(id=image_id)
        image.delete()
        return Response(status=200)


class GetImageAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get image by id",
    )
    def get(self, _, image_id):
        image = Image.objects.get(id=image_id)
        return FileResponse(image.image)
