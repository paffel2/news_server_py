from ..shared import *
from rest_framework.response import Response
from ..serializers import *
from ..models import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from rest_framework import serializers, generics
from rest_framework.exceptions import NotFound
import logging as log


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
        manual_parameters=[token_param],
    )
    def post(self, request, news_id):
        try:
            log.info("Creating commentary")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Getting Token from database")
            token = Token.objects.get(token=token_uuid)
            log.debug("Checking token")
            if is_token_valid(token):
                log.debug("Parsing request body")
                data = JSONParser().parse(request)
                log.debug("Adding user info")
                data["author"] = token.owner_id.id
                log.debug("Adding news info")
                data["news_id"] = news_id
                log.debug("Serializing")
                serializer = PostCommentarySerializer(data=data)
                log.debug("Validation")
                serializer.is_valid(raise_exception=True)
                log.debug("Saving")
                serializer.save()
                return Response(status=201)
        except serializers.ValidationError as e:
            if "news_id" in e.get_codes():
                log.error("News doesn't exist")
                return Response("News doesn't exist", status=500)
            log.error(f"Validation error: {e}")
            return Response(status=500)
        except TokenExpired:
            log.error("Token expired")
            return Response("Token expired", status=403)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
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
            log.debug("Getting news by id")
            news = News.objects.get(id=news_id)
            log.debug("Getting comments")
            commentaries = Commentary.objects.filter(news_id=news.id)
            log.debug("Serializing")
            serializer = CommentarySerializer(commentaries, many=True)
            log.debug("Applying pagination")
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
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Checking token")
            if is_admin(token_uuid):
                log.debug("Getting comment id from params")
                commentary_id = request.GET.get("id")
                log.debug("Getting comment")
                commentary = Commentary.objects.get(
                    id=commentary_id, news_id=news_id
                )  # по идее фильтрация по новости не нужна, так как id комментария уникально
                log.debug("Deleting")
                commentary.delete()
                return Response(status=200)
        except TokenExpired:
            log.error("Token expired")
            return Response("Token expired", status=403)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
        except Commentary.DoesNotExist:
            log.error("Commentary not exist")
            return Response("Commentary not exist", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)
