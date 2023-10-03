from ..models import User, Token, Author
import django.contrib.auth.hashers as hash
from django.db.utils import IntegrityError
import uuid
from ..common import *
from news_server_py.settings import SALT
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from ..exceptions import *
from rest_framework.exceptions import NotFound
from rest_framework import generics, mixins
import logging as log
from ..swagger import token_param, id_param
from ..permissions import GetAndPostPermission
from .viewset import CRUDViewSet


class UsersViewSet(CRUDViewSet, mixins.RetrieveModelMixin):
    http_method_names = ["get", "post", "delete"]
    pagination_class = PaginationClass
    permission_classes = [GetAndPostPermission]
    queryset = User.objects.all()
    serializer_class = UserShortInfoSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        elif self.action == "retrieve":
            return UserInfoSerializer
        else:
            return UserShortInfoSerializer

    @swagger_auto_schema(
        operation_description="Get list of users",
        responses={200: "successful", "other": "something went wrong"},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Registration",
        responses={201: "successful", "other": "something went wrong"},
        request_body=UserRegistrationSerializer,
    )
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            log.error(f"ValidationError: {e}")
            return Response("bad json format", status=500)
        except KeyError as e:
            log.error(f"KeyError: {e}")
            return Response(f"not found field {e}", status=500)
        except IntegrityError as e:
            if "UNIQUE constraint failed: news_user.username" in e.args[0]:
                log.error("Username already exist")
                return Response("username already exists", status=500)
            else:
                log.error(f"IntegrityError: {e.args}")
                return Response(status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Deleting user",
        responses={204: "successful", "other": "something went wrong"},
        manual_parameters=[token_param],
    )
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except User.DoesNotExist:
            log.error("User doesn't exist")
            return Response("Tag doesn't exist", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Get profile info",
        responses={200: "successful", "other": "something went wrong"},
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except User.DoesNotExist:
            log.error("User not exist, but token exist")
            return Response(status=404)
        except Exception as e:
            log.error(f"Something wrong {e}")
            return Response(status=404)


class LoginAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Login",
        responses={200: "successful", "other": "something went wrong"},
        request_body=UserLoginSerializer,
    )
    def post(self, request):
        try:
            log.info("Login endpoint")
            data = JSONParser().parse(request)
            serializer_req = UserLoginSerializer(data=data)
            serializer_req.is_valid(raise_exception=True)
            password_l = hash.make_password(data["password"], salt=SALT)
            username_l = data["username"]
            user = User.objects.get(username=username_l, password=password_l)
            token = Token()
            token.owner_id = user
            token.admin_permission = user.is_staff
            try:
                Author.objects.get(id=user.id)
                token.author_permission = True
            except Author.DoesNotExist:
                pass
            token.token = uuid.uuid4()
            token.save()
            serializer_resp = TokenSerializer(token)
            return Response(serializer_resp.data)

        except serializers.ValidationError as e:
            log.error(f"ValidationError: {e}")
            return Response("bad json format", status=500)
        except User.DoesNotExist:
            log.error(f"User doesn't exist")
            return Response("wrong username or password", status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)
