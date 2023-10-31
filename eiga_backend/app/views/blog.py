from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Blog, BlogBangumi


# TODO 考虑要不要做游客功能，按理说游客是不能评分的
class BlogInsert(APIView):
    def post(self, request):
        blog_id = str(request.data.get('blog_id'))
        title = str(request.data.get('title'))
        content = str(request.data.get('content'))
        time = str(request.data.get('time'))
        # foreignKey
        user_id = str(request.data.get('user_id'))
        print(request.data)
        try:
            obj = Blog(
                blog_id=blog_id,
                title=title,
                content=content,
                time=time,
                user_id=user_id
            )
            obj.save()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(0)


class BlogDelete(APIView):
    def post(self, request):
        blog_id = str(request.data.get('blog_id'))
        print(request.data)
        try:
            obj = Blog.objects.get(blog_id=blog_id)
            obj.delete()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(0)


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
