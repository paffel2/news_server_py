from ..models import Tag
from ..shared import *
from rest_framework.response import Response
from ..serializers import *
from ..models import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from rest_framework import serializers, generics
from django.db.utils import IntegrityError
from rest_framework.exceptions import NotFound


class CommentsAPIView(generics.GenericAPIView):
    queryset = Commentary.objects.all()
    serializer_class = CommentarySerializer
    ordering_fields = ["created", "author__id__username"]
    ordering = ["created"]
    pagination_class = PaginationClass

    @swagger_auto_schema(
        operation_description="Add comment to news",
        responses={201: "successful", "other": "something went wrong"},
        request_body=TextCommentarySerializer,
    )
    def post(self, request, news_id):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            token = Token.objects.get(token=token_uuid)
            if is_token_valid(token):
                data = JSONParser().parse(request)
                data["author"] = token.owner_id.id
                data["news_id"] = news_id
                print(data)
                serializer = PostCommentarySerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(status=201)
        except Exception as e:
            print(e)
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Get comments to news",
        responses={200: CommentarySerializer, "other": "something went wrong"},
    )
    def get(self, _, news_id):
        commentaries = Commentary.objects.filter(news_id=news_id)
        serializer = CommentarySerializer(commentaries, many=True)
        page = self.paginate_queryset(serializer.data)
        return Response(page, status=200)

    @swagger_auto_schema(
        operation_description="Delete comment to news",
        responses={200: "successful", "other": "something went wrong"},
    )
    def delete(self, request, news_id):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            if is_admin(token_uuid):
                commentary_id = request.GET.get("id")
                commentary = Commentary.objects.get(
                    id=commentary_id, news_id=news_id
                )  # по идее фильтрация по новости не нужна, так как id комментария уникально

                commentary.delete()
                return Response(status=200)
        except Exception as e:
            print(e)
            return Response(status=404)
