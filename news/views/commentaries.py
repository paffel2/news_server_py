from ..common import *
from rest_framework.response import Response
from ..serializers import *
from ..swagger import token_param, id_param
from ..models import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from rest_framework import serializers, generics
from rest_framework.exceptions import NotFound
import logging as log
from ..permissions import CommentariesPermission


class CommentsAPIView(generics.GenericAPIView):
    queryset = Commentary.objects.all()
    serializer_class = CommentarySerializer
    ordering_fields = ["created", "author__id__username"]
    ordering = ["created"]
    pagination_class = PaginationClass
    permission_classes = [CommentariesPermission]

    @swagger_auto_schema(
        operation_description="Add comment to news",
        responses={201: "successful", "other": "something went wrong"},
        request_body=TextCommentarySerializer,
        manual_parameters=[token_param],
    )
    def post(self, request, news_id):
        try:
            log.info("Creating commentary")
            token_uuid = request.META.get("HTTP_TOKEN")
            token = Token.objects.get(token=token_uuid)
            data = JSONParser().parse(request)
            data["author"] = token.owner_id.id
            data["news_id"] = news_id
            serializer = PostCommentarySerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=201)
        except serializers.ValidationError as e:
            if "news_id" in e.get_codes():
                log.error("News doesn't exist")
                return Response("News doesn't exist", status=500)
            log.error(f"Validation error: {e}")
            return Response(status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Get comments to news",
        responses={200: CommentarySerializer, "other": "something went wrong"},
    )
    def get(self, _, news_id):
        try:
            log.info("Getting commentaries to news")
            news = News.objects.get(id=news_id)
            commentaries = Commentary.objects.filter(news_id=news.id)
            serializer = CommentarySerializer(commentaries, many=True)
            page = self.paginate_queryset(serializer.data)
            return Response(page, status=200)
        except News.DoesNotExist:
            log.error("News doesn't exist")
            return Response("News doesn't exist", status=404)
        except NotFound as e:
            log.error(f"NotFound error {e}")
            return Response(str(e), status=404)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Delete comment to news",
        responses={200: "successful", "other": "something went wrong"},
        manual_parameters=[id_param("comment id"), token_param],
    )
    def delete(self, request, news_id):
        try:
            log.info("Deleting commentary")
            commentary_id = request.GET.get("id")
            commentary = Commentary.objects.get(
                id=commentary_id, news_id=news_id
            )  # по идее фильтрация по новости не нужна, так как id комментария уникально
            self.check_object_permissions(request, commentary)
            commentary.delete()
            return Response(status=200)

        except NotFoundException as e:
            return Response(e.detail, status=404)
        except Commentary.DoesNotExist:
            log.error("Commentary not exist")
            return Response("Commentary not exist", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)
