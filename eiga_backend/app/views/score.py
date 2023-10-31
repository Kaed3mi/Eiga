from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Score


# TODO 考虑要不要做游客功能，按理说游客是不能评分的
class ScoreInsert(APIView):
    def post(self, request):
        user_id = str(request.data.get('user_id'))
        bangumi_id = str(request.data.get('bangumi_id'))
        score = str(request.data.get('score'))
        print(request.data)
        try:
            obj = Score(
                user_id=user_id,
                bangumi_id=bangumi_id,
                score=score
            )
            obj.save()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(0)


class ScoreUpdate(APIView):
    def post(self, request):
        user_id = str(request.data.get('user_id'))
        bangumi_id = str(request.data.get('bangumi_id'))
        score = str(request.data.get('score'))
        print(request.data)
        try:
            obj = Score.objects.get(user_id=user_id, bangumi_id=bangumi_id)
            obj.score = score
            obj.save()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(0)


class ScoreDelete(APIView):
    def post(self, request):
        user_id = str(request.data.get('user_id'))
        bangumi_id = str(request.data.get('bangumi_id'))
        print(request.data)
        try:
            obj = Score.objects.get(user_id=user_id, bangumi_id=bangumi_id)
            obj.delete()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(0)
