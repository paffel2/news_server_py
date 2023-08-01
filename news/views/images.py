from django.http import HttpResponse,FileResponse
from ..models import Image, ImageForm
from django.core.serializers.json import Serializer
import json
import django.contrib.auth.hashers as hash
from django.core.exceptions import ObjectDoesNotExist
import uuid
from .shared import *
from email_validator import validate_email, EmailNotValidError

def upload_image(request):
    form = ImageForm(request.POST,request.FILES)
    print(form)
    if form.is_valid():
        print("is valid")
        form.save()
        return HttpResponse(status=200)
    else:
        print("invalid")
        return HttpResponse(status=404)

def get_image(_,image_id):
    image = Image.objects.get(id=image_id)
    return FileResponse(image.image)
# добавить обработку ошибок    

def get_image_urls():
    images = Image.objects.all()
    list_of_urls = []
    for i in images:
        image_id = i.id
        list_of_urls.append(to_image_urls(image_id))
    return HttpResponse(list_of_urls)


def images_handler(request):
    if request.method == 'GET':
        return get_image_urls()
    elif request.method == 'POST':
        return upload_image(request)