from django.http import HttpResponse
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