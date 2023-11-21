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
        print(email + " " + password)
        user_info = User.objects.fliter(email=email)
        print(user_info)
        if user_info.__len__() == 0:
            print("user not exist")
            return_information = {"state": "0", "exception": "user_not_exist", "tip": "用户不存在"}
            return HttpResponse(json.dumps(return_information))
        else:
            if password == User.objects.get(email=email).password:
                print("login success")
                return_information = {"state": "1", "exception": "", "tip": "登录成功"}
                return HttpResponse(json.dumps(return_information))
            else:
                return_information = {"state": "0", "exception": "password_wrong", "tip": "密码错误"}
                return HttpResponse(json.dumps(return_information))
