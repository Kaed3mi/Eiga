import base64
import mimetypes

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
import os
import shutil

from eiga_backend.settings import ASSETS_ROOT


class UserRegister(APIView):
    def post(self, request):
        # TODO need an approach to generate user_id!!!
        user_name = str(request.data.get('username'))
        email = str(request.data.get('email'))
        password = str(request.data.get('password'))
        permission = "user"

        image_base64 = request.data.get("image")
        print('data:', request.data)
        print('image_base64:', image_base64)

        # 数据库中头像对应路径
        if image_base64 == "default":  # 注册时并没有指定头像
            avatar = "avatars/default.jpg"
        else:
            # 如果有头像的记得保存
            image_str = base64.b64decode(image_base64.split(',')[1])
            print(image_base64)
            image_type = image_base64.split(';')[0].split(':')[1]
            file_ext = mimetypes.guess_extension(image_type)
            if not file_ext:
                file_ext = '.png'

            avatar = "avatars/" + email.split('.')[0] + file_ext
            with open(ASSETS_ROOT + avatar, 'wb') as f:
                f.write(image_str)

        print(request.data)
        user_info = User.objects.filter(email=email)
        if user_info.__len__() > 0:
            print("email has been registered")
            return_information = {"state": "0", "exception": "email_registered", "tips": "邮箱已被注册"}
            return HttpResponse(json.dumps(return_information))
        else:
            try:
                s = User.objects.create(
                    user_name=user_name,
                    email=email,
                    password=password,
                    permission=permission,
                    avatar=avatar
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
        print('user query request = ', request.data)
        user_id = request.data.get('user_id')
        user_info = User.objects.filter(user_id=user_id)
        if user_info.__len__() == 0:
            print("user not exist")
            return_information = {"state": "0", "exception": "user_not_exist", "tip": "用户不存在"}
            return HttpResponse(json.dumps(return_information))
        else:
            user = User.objects.get(user_id=user_id)
            print("the avatar: " + str(user.avatar))
            if user.avatar == "default":
                avatar_path = "avatars\default.jpg"
            else:
                avatar_path = str(user.avatar)
            with open(ASSETS_ROOT + avatar_path, 'rb') as f:
                image_data = base64.b64encode(f.read())
            return_information = {
                "state": "1",
                "exception": "",
                "tip": "success",
                "user_id": user_id,
                "username": user.user_name,
                "email": user.email,
                "password": user.password,
                "permission": user.permission,
                "avatar": user.avatar,
                "avatar_path": avatar_path,
                "image_data": str(image_data)[2:-1]
            }
            return HttpResponse(json.dumps(return_information))


class UserUpdateInfo(APIView):
    """用于用户更新信息
    {
    username:
    email:
    password:
    }
    """

    def post(self, request):
        user_id = str(request.data.get('user_id'))
        username = str(request.data.get('username'))
        email = str(request.data.get('email'))
        password = str(request.data.get('password'))
        user = User.objects.get(user_id=user_id)
        print(user.user_name)
        if User.objects.filter(user_id=user_id).__len__() == 0:
            print("user not exist")
            return Response(1)
        try:
            print(username, email, password)
            if username != '':
                user.user_name = username
            if email != '':
                user.email = email
            if password != '':
                user.password = password  # 听说这样可以确保密码以安全的方式进行哈希处理。
            user.save()
            return Response(0)
        except Exception as e:
            print(e)
            return Response(1)


@csrf_exempt
def upload_avatar(request):
    if request.method == 'POST':
        print(request.body)
        print("user_id: " + request.POST.get('user_id', ''))
        req_id = request.POST.get('user_id', '')
        user_info = User.objects.get(user_id=req_id)
        print(user_info)
        # print(request.FILES.get('file'))
        avatar = request.FILES.get('file')
        print(avatar)
        if avatar:
            # 保存头像到服务器
            file_path = default_storage.save(ASSETS_ROOT + 'avatars/' + avatar.name, ContentFile(avatar.read()))
            print(file_path)
            if user_info.avatar == "avatars/default.jpg":
                print("the user has the default avatar and we change it to " + str(file_path))
                user_info.avatar = str(file_path)
                user_info.save()
            else:
                print("now we will delete the original avatar")
                legacy_avatar = ASSETS_ROOT + user_info.avatar
                print(legacy_avatar)
                if os.path.exists(legacy_avatar):
                    os.remove(legacy_avatar)
                else:
                    print("path didn't find check it")
                user_info.avatar = str(file_path)
                user_info.save()

            # 返回头像的 URL
            avatar_url = f"{settings.MEDIA_URL}{avatar.name}"
            with open(file_path, 'rb') as f:
                image_data = base64.b64encode(f.read())
            return_information = {'state': '1', 'exception': '', 'avatar_url': avatar_url,
                                  'image_data': str(image_data)[2:-1]}
            return HttpResponse(json.dumps(return_information))
        else:
            return JsonResponse({'status': 'error', 'message': 'No file uploaded'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


class UserSearch(APIView):
    def get(self, request):
        pattern = request.GET.get('pattern')
        obj_list_data = []
        print('search user: pattern=' + pattern)
        try:
            list = User.objects.filter(user_name__contains=pattern)
            print(list)
            for obj in list:
                obj_list_data.append({
                    "id": obj.user_id,
                    "name": obj.user_name,
                })
        except Exception as e:
            print(e)
            return Response(1)
        return Response({
            'users': obj_list_data
        })
