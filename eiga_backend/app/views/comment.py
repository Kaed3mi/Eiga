from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Comment, User, Bangumi, Blog, Character
from django.db.models import Q
from app.utils.utils import urlToImgDate
from app.serializers import BlogModelSerializer, BangumiModelSerializer, UserModelSerializer, CharacterModelSerializer
import datetime


class CommentInsert(APIView):
    def post(self, request):
        content = str(request.data.get('content'))
        time = request.data.get('time')
        user_id = str(request.data.get('user_id'))
        bangumi_id = str(request.data.get('bangumi_id'))
        blog_id = str(request.data.get('blog_id'))
        character_id = str(request.data.get('character_id'))
        print(f'time = {time}')
        print(request.data)
        try:
            user = User.objects.get(user_id=user_id)
            bangumi = Bangumi.objects.get(bangumi_id=bangumi_id)
            blog = Blog.objects.get(blog_id=blog_id) if blog_id is not '' else None
            character = Character.objects.get(character_id=character_id) if character_id is not '' else None
            obj = Comment(
                content=content,
                time=datetime.datetime.fromtimestamp(time / 1000),
                user_id=user,
                bangumi_id=bangumi,
                blog_id=blog,
                character_id=character
            )
            obj.save()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(0)


class CommentQuery(APIView):
    def get(self, request):
        comment_id = request.GET.get('comment_id')
        print('query comment: id=' + comment_id)
        try:
            obj = Comment.objects.get(comment_id=comment_id)
        except Exception as e:
            print(e)
            return Response(1)
        user = obj.user_id
        bangumi = obj.bangumi_id
        blog = obj.blog_id
        character = obj.character_id
        return Response({
            'content': obj.content,
            'time': obj.time,
            'user_id': UserModelSerializer(obj.user_id).data if user is not None else '',
            'avatar': urlToImgDate(obj.user_id.avatar) if user is not None else '',
            'bangumi_id': BangumiModelSerializer(obj.bangumi_id).data if bangumi is not None else '',
            'blog_id': BlogModelSerializer(blog.blog_id).data if blog is not None else '',
            'character_id': CharacterModelSerializer(obj.character_id).data if character is not None else '',
        })


class CommentSearch(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        bangumi_id = request.GET.get('bangumi_id')
        blog_id = request.GET.get('blog_id')
        character_id = request.GET.get('character_id')
        print(f'query comment user_id={user_id},bangumi_id={bangumi_id},blog_id={blog_id},character_id={character_id}')
        filter_conditions = Q()
        if user_id is not None:
            filter_conditions &= Q(user_id=user_id)
        if bangumi_id is not None:
            filter_conditions &= Q(bangumi_id=bangumi_id)
        if blog_id is not None:
            filter_conditions &= Q(blog_id=blog_id)
        if character_id is not None:
            filter_conditions &= Q(character_id=character_id)
        obj_list_data = []
        try:
            obj_list = Comment.objects.filter(filter_conditions)
            print(obj_list)
            for obj in obj_list:
                user = obj.user_id
                bangumi = obj.bangumi_id
                blog = obj.blog_id
                character = obj.character_id
                obj_list_data.append({
                    'comment_id': obj.comment_id,
                    'content': obj.content,
                    'time': obj.time,
                    'user_id': UserModelSerializer(obj.user_id).data if user is not None else '',
                    'bangumi_id': BangumiModelSerializer(obj.bangumi_id).data if bangumi is not None else '',
                    'blog_id': BlogModelSerializer(blog.blog_id).data if blog is not None else '',
                    'character_id': CharacterModelSerializer(obj.character_id).data if character is not None else '',
                })
        except Exception as e:
            print(e)
            return Response(1)
        return Response({
            'comments': obj_list_data
        })
