from rest_framework.response import Response
from rest_framework.views import APIView
from ..common import *
from ..serializers import NewsSerializer
from ..swagger import (
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
from ..permissions import DraftOwnsPermission


class DraftsAPIView(generics.GenericAPIView):
    pagination_class = PaginationClass
    permission_classes = [DraftOwnsPermission]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="Get list of drafts",
        manual_parameters=[token_param],
    )
    def get(self, request):
        try:
            log.info("Get own drafts")
            token_uuid = request.META.get("HTTP_TOKEN")
            token = Token.objects.get(token=token_uuid)
            author = Author.objects.get(id=token.owner_id)
            drafts = News.objects.filter(is_published=False, author=author)
            serializer = NewsSerializer(drafts, many=True)
            page = self.paginate_queryset(serializer.data)
            return Response(page, status=200)
        except NotFound as e:
            log.error(f"NotFound error {e}")
            return Response(str(e), status=404)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Add draft",
        responses={201: "draft_id: integer", "other": "something went wrong"},
        manual_parameters=[
            token_param,
            id_form_param("category", None),
            text_form_param("tags", "list of tags id in format [1,2,3]"),
            text_form_param("text"),
            text_form_param("title"),
            image_form_param("main_image", "one image file"),
            image_form_param("images", "one or more image file"),
        ],
    )
    def post(self, request):
        try:
            log.info("Creating draft")
            form = NewsForm(request.POST, request.FILES)
            if form.is_valid():
                token_uuid = request.META.get("HTTP_TOKEN")
                token = Token.objects.get(token=token_uuid)
                news = News()
                news.category = form.cleaned_data.get("category")
                tags = form.cleaned_data.get("tags")
                news.title = form.cleaned_data.get("title")
                news.text = form.cleaned_data.get("text")
                news.author = Author.objects.get(id=token.owner_id)
                main_image = request.FILES.get("main_image")
                images = request.FILES.getlist("images")
                if main_image:
                    print(main_image)
                    to_db_main_image = Image()
                    to_db_main_image.image.save(main_image.name, main_image)
                    news.main_image = to_db_main_image
                news.save()
                images_list = []
                for image in images:
                    if "image" in image.content_type:
                        to_db_image = Image()
                        to_db_image.image.save(image.name, image)
                        images_list.append(to_db_image)
                    else:
                        log.error("BAD IMAGE")
                        return Response(status=500)
                for tag in tags:
                    news.tags.add(tag)
                for image in images_list:
                    news.images.add(image)
                return Response(f"draft_id: {news.id}", status=200)
            else:
                log.error(form.errors.as_data())
                return Response(form.errors.as_data(), status=500)
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
        manual_parameters=[id_param("draft id"), token_param],
    )
    def delete(self, request):
        try:
            log.info("Deleting draft")
            draft_id = request.GET.get("id")
            draft = News.objects.get(id=draft_id)
            self.check_object_permissions(request, draft)
            if not draft.is_published:
                for image in draft.images.all():
                    image.delete()
                if draft.main_image:
                    draft.main_image.delete()
                draft.delete()
                return Response(status=200)
            else:
                log.error("It is not draft")
                return Response("It is not draft", status=500)
        except News.DoesNotExist:
            log.error("News doesn't exist")
            return Response("Draft doesn't exist", status=500)
        except NotFoundException as e:
            return Response(e.detail, status=404)
        except Exception as e:
            log.error(type(e))
            log.error(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Update draft",
        responses={201: "draft_id: integer", "other": "something went wrong"},
        manual_parameters=[
            token_param,
            id_form_param("id", "draft id"),
            id_form_param("category", "category id"),
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
            form = DraftUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                draft_id = form.cleaned_data.get("id")
                news = News.objects.get(id=draft_id)
                self.check_object_permissions(request, news)
                news.category = form.cleaned_data.get("category")
                tags = form.cleaned_data.get("tags")
                news.title = form.cleaned_data.get("title")
                news.text = form.cleaned_data.get("text")
                news.tags.clear()
                for image in news.images.all():
                    image.delete()
                if news.main_image:
                    news.main_image.delete()
                main_image = request.FILES.get("main_image")
                images = request.FILES.getlist("images")
                if main_image:
                    print(main_image)
                    to_db_main_image = Image()
                    to_db_main_image.image.save(main_image.name, main_image)
                    news.main_image = to_db_main_image
                news.save()
                images_list = []
                for image in images:
                    if "image" in image.content_type:
                        to_db_image = Image()
                        to_db_image.image.save(image.name, image)
                        images_list.append(to_db_image)
                    else:
                        log.error("Bad Image")
                        return Response("Bad Image", status=500)
                for tag in tags:
                    news.tags.add(tag)
                for image in images_list:
                    news.images.add(image)
                return Response(f"draft_id: {news.id}", status=200)

            else:
                print(form.errors.as_data())
                return Response(status=404)
        except NotFoundException as e:
            return Response(e.detail, status=404)
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
    permission_classes = [DraftOwnsPermission]

    @swagger_auto_schema(
        operation_description="Get draft by id", manual_parameters=[token_param]
    )
    def get(self, request, draft_id):
        try:
            log.info("Getting draft by id")
            draft = News.objects.get(id=draft_id)
            self.check_object_permissions(request, draft)
            if not draft.is_published:
                log.debug("Serializing")
                serializer = NewsSerializer(draft)
                log.debug("Sending")
                return Response(serializer.data)
            else:
                log.error("It is not draft")
                return Response("It is not draft", status=400)
        except NotFoundException as e:
            return Response(e.detail, status=404)
        except News.DoesNotExist:
            log.error("Draft not exist")
            return Response(status=404)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)
