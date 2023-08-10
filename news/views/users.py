from ..models import User, Token, Author
import json
import django.contrib.auth.hashers as hash
from django.db.utils import IntegrityError
import uuid
from ..shared import *
from email_validator import validate_email, EmailNotValidError
from news_server_py.settings import SALT
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from ..exceptions import *
from rest_framework.exceptions import NotFound
from rest_framework import generics


class UsersAPIView(generics.GenericAPIView):
    pagination_class = PaginationClass

    @swagger_auto_schema(
        operation_description="Get list of users",
        responses={200: "successfull", "other": "something went wrong"},
    )
    def get(self, _):
        try:
            users = User.objects.all()
            serializer = UserShortInfoSerializer(users, many=True)
            page = self.paginate_queryset(serializer.data)
            return Response(page, status=200)

        except NotFound as e:
            return Response(str(e), status=404)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)
        else:
            return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Registration",
        responses={200: "successfull", "other": "something went wrong"},
        request_body=UserRegistrationSerializer,
    )
    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer_req = UserRegistrationSerializer(data=data)
            if serializer_req.is_valid():
                _ = validate_email(data["email"], check_deliverability=False)
                serializer_req.save(
                    password=hash.make_password(data["password"], salt=SALT)
                )
                return Response(status=201)
            else:
                return Response("bad json format", status=403)
        except EmailNotValidError:
            return Response("bad email addres", status=403)
        except KeyError as e:
            return Response(f"not found field {e}", status=403)
        except IntegrityError as e:
            if "UNIQUE constraint failed: news_user.username" in e.args[0]:
                return Response("username already exists", status=403)
            else:
                print(e.args)
                return Response(status=500)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)

    def delete(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            if is_admin(token_uuid):
                user_id = request.GET.get("id")
                user = User.objects.get(id=user_id)
                user.delete()
                return Response(status=200)
            else:
                print("Is not admin")
                return Response(status=404)
        except json.JSONDecodeError:
            return Response("bad json format", status=403)
        except KeyError as e:
            return Response(f"not found field {e}", status=403)
        except TokenExpired:
            print("Token expired")  # сделать нормальные логи
            return Response(status=404)
        except Token.DoesNotExist:
            print("Token not exist")  # сделать нормальные логи
            return Response(status=404)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(e, status=500)


class LoginAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Login",
        responses={200: "successfull", "other": "something went wrong"},
        request_body=UserLoginSerializer,
    )
    def post(self, request):
        data = JSONParser().parse(request)
        serializer_req = UserLoginSerializer(data=data)
        if serializer_req.is_valid():
            password_l = hash.make_password(data["password"], salt=SALT)
            username_l = data["username"]
            try:
                user = User.objects.get(username=username_l, password=password_l)
            except User.DoesNotExist:
                return Response("wrong username or password", status=401)
            else:
                token = Token()
                token.owner_id = user
                token.admin_permission = user.is_staff
                try:
                    _ = Author.objects.get(id=user.id)
                    token.author_permission = True
                except Author.DoesNotExist:
                    pass
                token.token = uuid.uuid4()
                try:
                    token.save()
                except Exception as e:
                    print(f"Something went wrong {e}")
                    return Response(status=500)
                else:
                    serializer_resp = TokenSerializer(token)
                return Response(serializer_resp.data)


class ProfileAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get profile info",
        responses={200: "successfull", "other": "something went wrong"},
        manual_parameters=[token_param],
    )
    def get(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            token = Token.objects.get(token=token_uuid)
            if is_token_valid(token):
                user_info = User.objects.get(id=token.owner_id.id)
                serializer = UserInfoSerializer(user_info)
                return Response(serializer.data)
            else:
                return Response(status=404)
        except TokenExpired:
            print("Token Expired")  # ЛОГИ
            return Response(
                status=404
            )  # возможно стоит вернуть сообщение об истекшем токене
        except Token.DoesNotExist:
            print("Token not exist")  # сделать нормальные логи
            return Response(status=404)
        except User.DoesNotExist:
            print("User not exist, but token exist")
            return Response(status=404)
        except Exception as e:
            print(f"Something wrong {e}")
            return Response(status=404)


"""

def check_token(request): #тестовый эндпоинт, будет удален, а функционал добавлен, где требуется проверка токена
    token_uuid = request.META.get('HTTP_TOKEN')
    result = is_token_valid(token_uuid)
    return HttpResponse(result) 
"""

"""
            body = json.loads(request.body.decode("utf-8"))
            user = User()
            user.first_name = body['first_name']
            user.last_name = body['last_name']
            email_info = validate_email(body['email'],check_deliverability=False)
            email = email_info.normalized
            user.email = email
            user.username = body['username']
            user.password = hash.make_password(body['password'],salt=SALT)
            try:
                user.save()
            except ValueError as e:
            #добавить логи
                return Response(status=403)
            else:
                return Response(status=201)
"""
