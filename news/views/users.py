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
from rest_framework import generics
import logging as log
from ..swagger import token_param, id_param


class UsersAPIView(generics.GenericAPIView):
    pagination_class = PaginationClass

    def get_queryset(self):
        return User.objects.all()

    @swagger_auto_schema(
        operation_description="Get list of users",
        responses={200: "successful", "other": "something went wrong"},
    )
    def get(self, _):
        try:
            log.info("Getting list of users endpoint")
            log.debug("Getting list of users from database")
            users = User.objects.all()
            log.debug("Serializing")
            serializer = UserShortInfoSerializer(users, many=True)
            log.debug("Applying pagination")
            page = self.paginate_queryset(serializer.data)
            log.debug("Sending list of users")
            return Response(page, status=200)

        except NotFound as e:
            log.error(f"NotFound error {e}")
            return Response(str(e), status=404)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=404)

    @swagger_auto_schema(
        operation_description="Registration",
        responses={200: "successful", "other": "something went wrong"},
        request_body=UserRegistrationSerializer,
    )
    def post(self, request):
        try:
            log.info("Registration endpoint")
            log.debug("Getting request body")  # добавить аватар
            data = JSONParser().parse(request)
            log.debug("Serializing")
            serializer_req = UserRegistrationSerializer(data=data)
            log.debug("Validation")
            serializer_req.is_valid(raise_exception=True)
            log.debug("Saving user")
            serializer_req.save(
                password=hash.make_password(data["password"], salt=SALT)
            )
            return Response(status=201)
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
        responses={200: "successful", "other": "something went wrong"},
        manual_parameters=[id_param("user_id"), token_param],
    )
    def delete(self, request):
        try:
            log.info("Deleting user endpoint")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Checking token")
            if is_admin(token_uuid):
                log.debug("Getting users's id from params")
                user_id = request.GET.get("id")
                log.debug("Getting users from database")
                user = User.objects.get(id=user_id)
                log.debug("Deleting user")
                user.delete()
                return Response(status=200)
            else:
                log.error("Is not admin")
                return Response(status=404)
        except TokenExpired:
            log.error("Token expired")
            return Response("Token expired", status=403)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(e, status=404)


class LoginAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Login",
        responses={200: "successful", "other": "something went wrong"},
        request_body=UserLoginSerializer,
    )
    def post(self, request):
        try:
            log.info("Login endpoint")
            log.debug("Getting request body")
            data = JSONParser().parse(request)
            log.debug("Serializing")
            serializer_req = UserLoginSerializer(data=data)
            log.debug("Validation")
            serializer_req.is_valid(raise_exception=True)
            log.debug("Getting username and password hash")
            password_l = hash.make_password(data["password"], salt=SALT)
            username_l = data["username"]
            log.debug("Getting user")
            user = User.objects.get(username=username_l, password=password_l)
            log.debug("Generating token")
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


class ProfileAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get profile info",
        responses={200: "successful", "other": "something went wrong"},
        manual_parameters=[token_param],
    )
    def get(self, request):
        try:
            log.info("Profile endpoint")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            token = Token.objects.get(token=token_uuid)
            log.debug("Checking token")
            is_token_valid(token)
            log.debug("Getting user info")
            user_info = User.objects.get(id=token.owner_id.id)
            serializer = UserInfoSerializer(user_info)
            return Response(serializer.data)
        except TokenExpired:
            log.error("Token Expired")
            return Response("Token Expired", status=403)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
        except User.DoesNotExist:
            log.error("User not exist, but token exist")
            return Response(status=404)
        except Exception as e:
            log.error(f"Something wrong {e}")
            return Response(status=404)
