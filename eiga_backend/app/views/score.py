from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Score, User, Bangumi
from app.serializers import BangumiModelSerializer

# TODO 考虑要不要做游客功能，按理说游客是不能评分的
class ScoreInsert(APIView):
    def post(self, request):
        user_id = str(request.data.get('user_id'))
        bangumi_id = str(request.data.get('bangumi_id'))
        score = str(request.data.get('score'))
        print(request.data)
        try:
            user = User.objects.get(user_id=user_id)
            bangumi = Bangumi.objects.get(bangumi_id=bangumi_id)
            obj = Score(
                user_id=user,
                bangumi_id=bangumi,
                score=score
            )
            obj.save()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(0)


class ScoreUpdate(APIView):
    def put(self, request):
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


class ScoreQuery(APIView):
    def get(self, request):
        bangumi_id = request.GET.get('bangumi_id')
        user_id = request.GET.get('user_id')
        print(f"score query:user_id={user_id},bangumi_id={bangumi_id}")
        try:
            obj = Score.objects.get(bangumi_id=bangumi_id, user_id=user_id)
        except Exception as e:
            print(e)
            return Response(1)
        print(f"score query:score = {obj.score}")
        return Response({
            'score': obj.score
        })


class BangumiScoreQuery(APIView):
    def get(self, request):
        bangumi_id = request.GET.get('bangumi_id')
        average_score = 0.0
        print(request.data)
        try:
            obj_list = Score.objects.filter(bangumi_id=bangumi_id)
            bangumi_list_data = []
            total = 0.0
            i = 0
            for score in obj_list:
                total += score.score
                i += 1
            average_score = -1 if i is 0 else total / i
        except Exception as e:
            print(e)
            return Response(1)
        return Response({
            'score': average_score
        })

class GetUserScores(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        try:
            obj_list = Score.objects.filter(user_id=user_id)
            bangumis = []
            for obj in obj_list:
                # Bangumi.objects.filter(bangumi_id=obj.bangumi_id).get(0).bangumi_cover需要获得封面
                bangumis.append({
                    'bangumi': BangumiModelSerializer(obj.bangumi_id).data,
                    'score': obj.score
                })
        except Exception as e:
            print(e)
            return Response(1)
        return Response({
            'bangumis': bangumis
        })
