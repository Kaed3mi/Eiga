from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Bangumi, Blog
from app.models import BlogBangumi
from app.serializers import BangumiModelSerializer, BlogModelSerializer
from app.utils.utils import urlToImgDate


class BlogBangumiQuery(APIView):
    def get(self, request):
        blog_id = int(request.GET.get('blog_id'))
        obj_list_data = []
        print('search BlogBangumiQuery: blog_id=', blog_id)
        try:
            list = BlogBangumi.objects.filter(blog_id=blog_id)
            print(list)
            for obj in list:
                obj_list_data.append({
                    "image": urlToImgDate(obj.bangumi_id.image),
                    "bangumi_id": BangumiModelSerializer(obj.bangumi_id).data
                })
        except Exception as e:
            print('BlogBangumiQuery failed', e)
            return Response(1)
        print('BlogBangumiQuery succeed')
        return Response({
            'bangumis': obj_list_data
        })


class BangumiBlogQuery(APIView):
    def get(self, request):
        bangumi_id = int(request.GET.get('bangumi_id'))
        obj_list_data = []
        print('search BangumiBlogQuery: bangumi_id=', bangumi_id)
        try:
            list = BlogBangumi.objects.filter(bangumi_id=bangumi_id)
            print(list)
            for obj in list:
                obj_list_data.append({
                    "blog_id": BlogModelSerializer(obj.blog_id).data,
                    "avatar": urlToImgDate(obj.blog_id.user_id.avatar),
                    "user_name": obj.blog_id.user_id.user_name,
                })
        except Exception as e:
            print('BangumiBlogQuery failed', e)
            return Response(1)
        print('BangumiBlogQuery succeed, results of:', len(obj_list_data))
        return Response({
            'blogs': obj_list_data
        })


class BlogBangumiUpdate(APIView):
    def put(self, request):
        print(request.data)
        blog_id = int(request.data.get('blog_id'))
        bangumis = list(request.data.get('bangumis'))
        blog_bangumi_list = BlogBangumi.objects.filter(blog_id=blog_id)
        for blog_bangumi in blog_bangumi_list:
            print("deleting " + str(blog_bangumi.bangumi_id.bangumi_id))
            blog_bangumi.delete()
        for bangumi_id in bangumis:
            blog = Blog.objects.get(blog_id=blog_id)
            bangumi = Bangumi.objects.get(bangumi_id=bangumi_id)
            relate = BlogBangumi.objects.create(blog_id=blog, bangumi_id=bangumi)
            relate.save()
        print(bangumis)
        return Response(1)
