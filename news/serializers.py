from .models import *
from rest_framework import serializers
from django.db import models
from drf_yasg import openapi

id_body = openapi.Schema('id',type=openapi.TYPE_INTEGER)
def id_param(decription):
    return openapi.Parameter('id', openapi.IN_QUERY, description=decription, type=openapi.TYPE_INTEGER)

token_param = openapi.Parameter('token',openapi.IN_HEADER,description="accesing token", type=openapi.TYPE_STRING)

class PutCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(max_length=250)
    parent_category = models.IntegerField()

    class Meta:
        model = Category
        fields = ['category_name','parent_category']

class CategorySerializer(PutCategorySerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Category
        fields = ['id','category_name','parent_category']

class PutTagSerializer(serializers.ModelSerializer):
    tag_name = serializers.CharField(max_length=250)

    class Meta:
        model = Tag
        fields = ['tag_name']

class TagSerializer(PutTagSerializer):
    id = serializers.IntegerField()
    tag_name = serializers.CharField(max_length=250)
    
    def update(self,instance,validated_data):
        instance.tag_name = validated_data.get("tag_name",instance.tag_name)
        instance.id = validated_data.get("id",instance.id)
        instance.save()
        return instance
    
    class Meta:
        model = Tag
        fields = ['id','tag_name']

class UserShortInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    date_joined = serializers.DateTimeField()

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name','date_joined']

class UserInfoSerializer(UserShortInfoSerializer):
    id = serializers.IntegerField()
    is_staff = serializers.BooleanField()
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['id','username','first_name', 'last_name','date_joined', 'email','is_staff']

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['username','password']

class UserRegistrationSerializer(UserLoginSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['username','password','first_name', 'last_name','email']


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.UUIDField()

    class Meta:
        model = Token
        fields = ['token']