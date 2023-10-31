from django.shortcuts import render, HttpResponse, redirect
 
# Create your views here.
 
from rest_framework import status
from rest_framework.views import APIView
from ..serializers import UserModelSerializer, User
from rest_framework.response import Response
import json
import uuid
 
class VueViews(APIView):
    def get(self, request):
        """获取所有用户信息"""
        # 1. 从数据库中读取用户列表信息
        instance_list = User.objects.all()
        # 2. 实例化序列化器，获取序列化对象
        serializer = UserModelSerializer(instance_list, many=True)
        # 3. 使用serializer.data实现对数据进行序列化成字典
        return Response(serializer.data)
 
    def post(self, request):
        """添加用户信息"""
        # 1. 获取客户端提交的数据，实例化序列化器，获取序列化对象
        serializer = UserModelSerializer(data=request.data)
        # 2. 反序列化[验证数据、保存数据到数据库]
        serializer.is_valid(raise_exception=False)
 
        username = request.data['username']
        print(username)
        passwd = request.data['passwd']
        print(passwd)
        if request.data.get('passwd2', ''):
            userinfo = User.objects.filter(user_name=username)
            print("userinfo")
        
            print(userinfo.__len__() > 0)
            if userinfo.__len__() > 0:
                print('用户已存在')
                info = {"state": "fail1", "tip": '用户已存在'}
                print('用户已存在')
                return HttpResponse(json.dumps(info))
            else:
                passwd2 = request.data['passwd2']
                if passwd2 != passwd:
                    # print('两次密码输入不同，请重新输入')
                    info = {"state": "fail2", "tip": '两次密码输入不同，请重新输入'}
                    return HttpResponse(json.dumps(info))
                else:
                    s = User.objects.create(
                        user_id=uuid.uuid4(),
                        user_name=request.data['username'],
                        email="",
                        password=request.data['passwd'],
                        permission=""
                    )
                    serializer = UserModelSerializer(data=s)
                    serializer.is_valid(raise_exception=False)
                    serializer.save()
                    # print('注册成功')
                # print(username, passwd, passwd2)
        else:
            userinfo = User.objects.filter(user_name=username)
            if userinfo.exists():
                if User.objects.get(user_name=username).password == passwd:
                    # print('登录成功')
                    pass
                else:
                    # print('密码错误，请重新输入')
                    info = {"state": "fail3", "tip": '密码错误，请重新输入'}
                    return HttpResponse(json.dumps(info))
            else:
                # print('用户名不存在，请重新输入')
                info = {"state": "fail4", "tip": '用户名不存在，请重新输入'}
                return HttpResponse(json.dumps(info))
            # print(username, passwd)
 
        # 3. 返回新增的模型数据经过序列化提供给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)