from rest_framework.response import Response
from rest_framework.views import APIView
from ..shared import *
from django.http import FileResponse
from ..serializers import ImageToUrlSerialzer



class ImagesAPIView(APIView):
    
    def post(self,request):
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            id = str(form.instance.id)
            return Response(id,status=200)
        else:
            print("invalid")
            return Response(status=404)
    
    def get(self,_):
        images = Image.objects.all()
        serializer = ImageToUrlSerialzer(images,many=True)
        return Response(serializer.data)


class GetImageAPIView(APIView):
    def get(self,_,image_id):
        image = Image.objects.get(id=image_id)
        return FileResponse(image.image)