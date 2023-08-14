from .models import *
from rest_framework import serializers
from django.db import models
from drf_yasg import openapi
from news_server_py.settings import (
    ALLOWED_HOSTS,
    ALLOWED_PORT,
)

id_body = openapi.Schema("id", type=openapi.TYPE_INTEGER)


def id_param(decription):
    return openapi.Parameter(
        "id", openapi.IN_QUERY, description=decription, type=openapi.TYPE_INTEGER
    )


token_param = openapi.Parameter(
    "token", openapi.IN_HEADER, description="accesing token", type=openapi.TYPE_STRING
)


class PutCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(max_length=250)
    parent_category = models.IntegerField()

    class Meta:
        model = Category
        fields = ["category_name", "parent_category"]


class CategorySerializer(PutCategorySerializer):
    id = serializers.IntegerField()

    def update(self, instance, validated_data):
        instance.category_name = validated_data.get(
            "category_name", instance.category_name
        )
        instance.id = validated_data.get("id", instance.id)
        instance.parent_category = validated_data.get(
            "parent_category", instance.parent_category
        )
        instance.save()
        return instance

    class Meta:
        model = Category
        fields = ["id", "category_name", "parent_category"]


class PutTagSerializer(serializers.ModelSerializer):
    tag_name = serializers.CharField(max_length=250)

    class Meta:
        model = Tag
        fields = ["tag_name"]


class TagSerializer(PutTagSerializer):
    id = serializers.IntegerField()
    tag_name = serializers.CharField(max_length=250)

    def update(self, instance, validated_data):
        instance.tag_name = validated_data.get("tag_name", instance.tag_name)
        instance.id = validated_data.get("id", instance.id)
        instance.save()
        return instance

    class Meta:
        model = Tag
        fields = ["id", "tag_name"]


class UserShortInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    date_joined = serializers.DateTimeField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "date_joined"]


class UserInfoSerializer(UserShortInfoSerializer):
    id = serializers.IntegerField()
    is_staff = serializers.BooleanField()
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "email",
            "is_staff",
        ]


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ["username", "password"]


class UserRegistrationSerializer(UserLoginSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "email"]


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.UUIDField()

    class Meta:
        model = Token
        fields = ["token"]


class PutAuthorSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.bio = validated_data.get("bio", instance.bio)
        instance.id = validated_data.get("id", instance.id)
        instance.save()
        return instance

    class Meta:
        model = Author
        fields = ["id", "bio"]
        extra_kwargs = {
            "id": {"validators": []},
        }


class AuthorInfo(serializers.ModelSerializer):
    bio = serializers.CharField(max_length=500, required=False)

    class Meta:
        model = Author
        fields = ["bio"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["username"] = instance.id.username
        representation["first_name"] = instance.id.first_name
        representation["last_name"] = instance.id.last_name
        representation["email"] = instance.id.email
        representation["date_joined"] = instance.id.date_joined
        return representation


class ShortNewsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=250)
    text = serializers.CharField(max_length=250)

    class Meta:
        model = News
        fields = ["id", "title", "text"]


class FullCategoryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def to_representation(self, instance):
        self.fields["parent_category"] = FullCategoryInfoSerializer(read_only=True)
        return super(FullCategoryInfoSerializer, self).to_representation(instance)


class ImageIdToUrl(serializers.EmailField):
    def to_representation(self, data):
        data = to_image_urls(data)
        return data


class ImageToUrlSerialzer(serializers.ModelSerializer):
    url = ImageIdToUrl(source="id")

    class Meta:
        model = Image
        fields = ["url"]


def to_image_urls(id):
    if ALLOWED_HOSTS != []:
        str = f"http://{ALLOWED_HOSTS[0]}:{ALLOWED_PORT}/api/images/{id}"
        return str
    else:
        return "error"  # добавить обработку исключений


class NewsSerializer(serializers.ModelSerializer):
    category = FullCategoryInfoSerializer()
    author = AuthorInfo()
    tags = TagSerializer(many=True)
    images = ImageToUrlSerialzer(many=True)
    main_image = ImageToUrlSerialzer()

    class Meta:
        model = News
        fields = "__all__"


class PostCommentarySeriallizer(serializers.ModelSerializer):
    # news_id = serializers.SerializerMethodField()

    class Meta:
        model = Commentary
        fields = "__all__"

    # def add_news_id(self,news_id):


class CommentarySerializer(serializers.ModelSerializer):
    author = UserShortInfoSerializer()
    created = serializers.DateTimeField()
    text = serializers.CharField(max_length=2500)

    class Meta:
        model = Commentary
        fields = "__all__"
