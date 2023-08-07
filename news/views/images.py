from rest_framework.response import Response
from rest_framework.views import APIView
from ..views.shared import *
from django.http import FileResponse


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
        list_of_urls = []
        for i in images:
            image_id = i.id
            list_of_urls.append(to_image_urls(image_id))
        return Response(list_of_urls)


class GetImageAPIView(APIView):
    def get(self,_,image_id):
        image = Image.objects.get(id=image_id)
        return FileResponse(image.image)