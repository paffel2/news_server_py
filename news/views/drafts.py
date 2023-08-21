from rest_framework.response import Response
from rest_framework.views import APIView
from ..common import *
from ..serializers import (
    NewsSerializer,
    id_param,
    token_param,
    id_form_param,
    text_form_param,
    image_form_param,
)
from rest_framework import generics
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema
import logging as log
from rest_framework.parsers import MultiPartParser


class DraftsAPIView(generics.GenericAPIView):
    pagination_class = PaginationClass

    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="Get list of drafts",
        manual_parameters=[token_param],
    )
    def get(self, request):
        try:
            log.info("Get own drafts")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Checking token")
            token = Token.objects.get(token=token_uuid)
            if is_author(token_uuid):
                log.debug("Getting author from database")
                author = Author.objects.get(id=token.owner_id)
                log.debug("Getting drafts from database")
                drafts = News.objects.filter(is_published=False, author=author)
                log.debug("Serializing")
                serializer = NewsSerializer(drafts, many=True)
                log.debug("Applying pagination")
                page = self.paginate_queryset(serializer.data)
                return Response(page, status=200)
            else:
                log.error("Not author")
                return Response(status=404)
        except NotFound as e:
            log.error(f"NotFound error {e}")
            return Response(str(e), status=404)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
        except TokenExpired:
            log.error("Token expired")
            return Response("Token expired", status=403)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Add draft",
        responses={201: "draft_id: integer", "other": "something went wrong"},
        manual_parameters=[
            token_param,
            id_form_param("category_id", None),
            id_form_param("tags", "list of tags id in format [1,2,3]"),
            text_form_param("text"),
            text_form_param("title"),
            image_form_param("main_image", "one image file"),
            image_form_param("images", "one or more image file"),
        ],
    )
    def post(self, request):
        try:
            log.info("Creating draft")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Checking token")
            if is_author(token_uuid):
                log.debug("Parse form")
                form = NewsForm(request.POST, request.FILES)
                log.debug("Form validation")
                if form.is_valid():
                    token = Token.objects.get(token=token_uuid)
                    log.debug("Creating news")
                    news = News()
                    log.debug("Adding category")
                    news.category = form.cleaned_data.get("category")
                    log.debug("Getting tags")
                    tags = form.cleaned_data.get("tags")
                    log.debug("Adding title")
                    news.title = form.cleaned_data.get("title")
                    log.debug("Adding text")
                    news.text = form.cleaned_data.get("text")
                    log.debug("Adding author")
                    news.author = Author.objects.get(id=token.owner_id)
                    log.debug("Getting main image")
                    main_image = request.FILES.get("main_image")
                    log.debug("Getting other images")
                    images = request.FILES.getlist("images")
                    log.debug("Adding main image")
                    to_db_main_image = Image()
                    to_db_main_image.image.save(main_image.name, main_image)
                    news.main_image = to_db_main_image
                    log.debug("Saving news")
                    news.save()
                    images_list = []
                    log.debug("Adding other images and relations")
                    for image in images:
                        if "image" in image.content_type:
                            to_db_image = Image()
                            to_db_image.image.save(image.name, image)
                            images_list.append(to_db_image)
                        else:
                            log.error("BAD IMAGE")
                            return Response(status=500)
                    log.debug("Adding tags relations")
                    for tag in tags:
                        news.tags.add(tag)
                    for image in images_list:
                        news.images.add(image)
                    return Response(f"draft_id: {news.id}", status=200)
                else:
                    log.error(form.errors.as_data())
                    return Response(form.errors.as_data(), status=500)
            else:
                log.error("Not author")
                return Response(status=404)
        except TokenExpired:
            log.error("Token expired")
            return Response("Token expired", status=403)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
        except Tag.DoesNotExist:
            log.error("Tag not exist")
            return Response("Tag not exist", status=500)
        except Category.DoesNotExist:
            log.error("Category not exist")
            return Response("Category not exist", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Delete draft",
        responses={200: "successful", "other": "something went wrong"},
        manual_parameters=[id_param("draft id")],
    )
    def delete(self, request):
        try:
            log.info("Deleting draft")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Getting draft id from query params")
            draft_id = request.GET.get("id")
            log.debug("Checking token")
            if is_admin(token_uuid) or is_news_owner(token_uuid, draft_id):
                draft = News.objects.get(id=draft_id)
                log.debug("Checking draft")
                if not draft.is_published:
                    log.debug("Deleting images")
                    for image in draft.images.all():
                        image.delete()
                    log.debug("Deleting main image")
                    draft.main_image.delete()
                    log.debug("Deleting draft")
                    draft.delete()
                    return Response(status=200)
                else:
                    log.error("It is not draft")
                    return Response("It is not draft", status=500)
            else:
                log.error("No access")
                return Response(status=404)
        except TokenExpired:
            log.error("Token expired")
            return Response("Token expired", status=403)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
        except News.DoesNotExist:
            log.error("News doesn't exist")
            return Response("Draft doesn't exist", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Update draft",
        responses={201: "draft_id: integer", "other": "something went wrong"},
        manual_parameters=[
            token_param,
            id_form_param("category_id", None),
            id_form_param("tags", "list of tags id in format [1,2,3]"),
            text_form_param("text"),
            text_form_param("title"),
            image_form_param("main_image", "one image file"),
            image_form_param("images", "one or more image file"),
        ],
    )
    def put(self, request):
        try:
            log.info("Creating draft")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Parse form")
            form = DraftUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                log.debug("Getting draft_id from form")
                draft_id = form.cleaned_data.get("id")
                log.debug("Checking author")
                if is_news_owner(token_uuid, draft_id):
                    log.debug("Getting draft from database")
                    news = News.objects.get(id=draft_id)
                    log.debug("Updating category")
                    news.category = form.cleaned_data.get("category")
                    log.debug("Getting tags")
                    tags = form.cleaned_data.get("tags")
                    log.debug("Updating title")
                    news.title = form.cleaned_data.get("title")
                    log.debug("Updating text")
                    news.text = form.cleaned_data.get("text")
                    log.debug("Deleting old images")
                    for image in news.images.all():
                        image.delete()
                    news.main_image.delete()
                    log.debug("Getting main image")
                    main_image = request.FILES.get("main_image")
                    log.debug("Getting other images")
                    images = request.FILES.getlist("images")
                    log.debug("Adding main image")
                    to_db_main_image = Image()
                    to_db_main_image.image.save(main_image.name, main_image)
                    news.main_image = to_db_main_image
                    log.debug("Saving draft")
                    news.save()
                    images_list = []
                    log.debug("Adding other images and relations")
                    for image in images:
                        if "image" in image.content_type:
                            to_db_image = Image()
                            to_db_image.image.save(image.name, image)
                            images_list.append(to_db_image)
                        else:
                            log.error("Bad Image")
                            return Response("Bad Image", status=500)
                    log.debug("Adding tags relations")
                    for tag in tags:
                        news.tags.add(tag)
                    for image in images_list:
                        news.images.add(image)
                    return Response(f"draft_id: {news.id}", status=200)
                else:
                    log.error("No access")
                    return Response(status=404)
            else:
                print(form.errors.as_data())
                return Response(status=404)
        except TokenExpired:
            log.error("Token expired")
            return Response("Token expired", status=403)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
        except Tag.DoesNotExist:
            log.error("Tag not exist")
            return Response("Tag not exist", status=500)
        except Category.DoesNotExist:
            log.error("Category not exist")
            return Response("Category not exist", status=500)
        except News.DoesNotExist:
            log.error("Draft not exist")
            return Response(status=404)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)


class FullDraftAPIView(APIView):
    def get(self, request, draft_id):
        try:
            log.info("Getting draft by id")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Checking token")
            if is_author(token_uuid):
                log.debug("Getting draft from database")
                draft = News.objects.get(id=draft_id)
                if not draft.is_published:
                    log.debug("Serializing")
                    serializer = NewsSerializer(draft)
                    log.debug("Sending")
                    return Response(serializer.data)
                else:
                    log.error("It is not draft")
                    return Response("It is not draft", status=400)
            else:
                log.error("No access")
                return Response(status=404)
        except News.DoesNotExist:
            log.error("Draft not exist")
            return Response(status=404)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)
