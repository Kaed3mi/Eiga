from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Blog, BlogBangumi, User, Bangumi
from app.serializers import UserModelSerializer,BlogModelSerializer
from app.utils.utils import urlToImgDate
import datetime


# TODO 考虑要不要做游客功能，按理说游客是不能评分的
class BlogInsert(APIView):
    def post(self, request):
        blog_title = str(request.data.get('blog_title'))
        content = str(request.data.get('content'))
        time = request.data.get('time')
        print("blog insert:", request.data)
        user_id = str(request.data.get('user_id'))
        bangumis = list(request.data.get('bangumis'))
        print(request.data)
        try:
            user = User.objects.get(user_id=user_id)
            blog = Blog(
                blog_title=blog_title,
                content=content,
                time=datetime.datetime.fromtimestamp(time / 1000),
                user_id=user
            )
            blog.save()
            for bangumi_id in bangumis:
                bangumi = Bangumi.objects.get(bangumi_id=bangumi_id)
                relate = BlogBangumi.objects.create(blog_id=blog, bangumi_id=bangumi)
                relate.save()
        except Exception as e:
            print(e)
            return Response(1)
        return Response({"blog_id": blog.blog_id})


class BlogDelete(APIView):
    def delete(self, request):
        blog_id = request.GET.get('blog_id')
        try:
            blog = Blog.objects.get(blog_id=blog_id)
            blog.delete()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(0)


class BlogSearch(APIView):
    def get(self, request):
        pattern = request.GET.get('pattern')
        obj_list_data = []
        print('search blog: pattern=' + pattern)
        try:
            list = Blog.objects.filter(blog_title__contains=pattern)
            print(list)
            for obj in list:
                obj_list_data.append({
                    "id": obj.blog_id,
                    "name": obj.blog_title,
                    "description": obj.content
                })
        except Exception as e:
            print(e)
            return Response(1)
        return Response({
            'blogs': obj_list_data
        })


class BlogUpdate(APIView):
    def put(self, request):
        blog_id = request.data.get("blog_id")
        blog_title = str(request.data.get('blog_title'))
        content = str(request.data.get('content'))
        time = request.data.get('time')
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(user_id=user_id)
            blog = Blog.objects.get(blog_id=blog_id)
            blog.user_id = user
            blog.blog_title = blog_title
            blog.content = content
            blog.time = datetime.datetime.fromtimestamp(time / 1000)
            blog.save()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(1)


class BlogQuery(APIView):
    def get(self, request):
        blog_id = request.GET.get('blog_id')
        print('query blog: id=' + blog_id)
        try:
            obj = Blog.objects.get(blog_id=blog_id)
        except Exception as e:
            print(e)
            return Response(1)
        return Response({
            'content': obj.content,
            'blog_title': obj.blog_title,
            'time': obj.time,
            'avatar': urlToImgDate(obj.user_id.avatar),
            'user_id': UserModelSerializer(obj.user_id).data if obj.user_id is not None else '',
        })


class UserBlogQuery(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        obj_list_data = []
        print('UserBlogQuery user_id:' + user_id)
        try:
            list = Blog.objects.filter(user_id=user_id)
            print(list)
            for obj in list:
                obj_list_data.append({
                    "blog_id": BlogModelSerializer(obj).data,
                    "avatar": urlToImgDate(obj.user_id.avatar),
                    "user_name": obj.user_id.user_name,
                })
        except Exception as e:
            print(e)
            return Response(1)
        return Response({
            'blogs': obj_list_data
        })


class RelateBangumi(APIView):
    def post(self, request):
        blog_id = str(request.data.get('blog_id'))
        bangumi_id = str(request.data.get('bangumi_id'))
        print(request.data)
        try:
            obj = BlogBangumi(
                blog_id=blog_id,
                bangumi_id=bangumi_id
            )
            obj.save()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(0)


class RelateDelete(APIView):
    def post(self, request):
        blog_id = str(request.data.get('blog_id'))
        bangumi_id = str(request.data.get('bangumi_id'))
        print(request.data)
        try:
            obj = BlogBangumi.objects.get(blog_id=blog_id, bangumi_id=bangumi_id)
            obj.delete()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(0)
