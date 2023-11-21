from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import User
from django.shortcuts import render, HttpResponse, redirect
import json


class UserRegister(APIView):
    def post(self, request):
        # TODO need an approach to generate user_id!!!
        user_id = str(request.data.get('user_id'))
        user_name = str(request.data.get('username'))
        email = str(request.data.get('email'))
        password = str(request.data.get('password'))
        permission = "user"
        user_id = email
        print(request.data)
        user_info = User.objects.filter(email=email)
        if user_info.__len__() > 0:
            print("email has been registered")
            return_information = {"state": "0", "exception": "email_registered", "tips": "邮箱已被注册"}
            return HttpResponse(json.dumps(return_information))
        else:
            try:
                s = User.objects.create(
                    user_id=user_id,
                    user_name=user_name,
                    email=email,
                    password=password,
                    permission=permission,
                    avatar="default"
                )
                s.save()
            except Exception as e:
                print(e)
                return_information = {"state": "0", "exception": e, "tips": "db_create发生异常"}
                return HttpResponse(json.dumps(return_information))
            print("register success! ")
            return_information = {"state": "1", "exception": "", "tips": "注册成功"}
            return HttpResponse(json.dumps(return_information))


class UserLogin(APIView):
    def post(self, request):
        email = str(request.data.get('email'))
        password = str(request.data.get('password'))
        print(User.objects.get(email=email).password)
        user_info = User.objects.filter(email=email)
        print(user_info)
        if user_info.__len__() == 0:
            print("user not exist")
            return_information = {"state": "0", "exception": "user_not_exist", "tip": "用户不存在"}
            return HttpResponse(json.dumps(return_information))
        else:
            if password == User.objects.get(email=email).password:
                user_information = {'user_id': User.objects.get(email=email).user_id,
                                    'username': User.objects.get(email=email).user_name,
                                    'permission': User.objects.get(email=email).permission}
                print("login success " + str(user_information))
                return_information = {
                    "state": "1",
                    "exception": "",
                    "tip": "登录成功",
                    'user_id': User.objects.get(email=email).user_id,
                    'username': User.objects.get(email=email).user_name,
                    'permission': User.objects.get(email=email).permission
                }
                return HttpResponse(json.dumps(return_information))
            else:
                return_information = {"state": "0", "exception": "password_wrong", "tip": "密码错误"}
                return HttpResponse(json.dumps(return_information))


class UserInfoQuery(APIView):
    def post(self, request):
        user_id = str(request.data.get('user_id'))
        user_info = User.objects.filter(user_id=user_id)
        print(user_info)
        if user_info.__len__() == 0:
            print("user not exist")
            return_information = {"state": "0", "exception": "user_not_exist", "tip": "用户不存在"}
            return HttpResponse(json.dumps(return_information))
        else:
            user = User.objects.get(user_id=user_id)
            print(user)
            return_information = {
                "state": "1",
                "exception": "",
                "tip": "success",
                "user_id": user_id,
                "username": user.user_name,
                "email": user.email,
                "password": user.password,
                "permission": user.permission,
                "avatar": user.avatar
            }
            return HttpResponse(json.dumps(return_information))

@csrf_exempt
def upload_avatar(request):
    if request.method == 'POST':
        print(request.FILES.get('file'))
        avatar = request.FILES.get('file')
        print(avatar)
        if avatar:
            # 保存头像到服务器
            file_path = default_storage.save('avatars/' + avatar.name, ContentFile(avatar.read()))
            print(file_path)
            # 返回头像的 URL
            avatar_url = f"{settings.MEDIA_URL}{file_path}"
            return JsonResponse({'status': 'success', 'avatar_url': avatar_url})
        else:
            return JsonResponse({'status': 'error', 'message': 'No file uploaded'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
