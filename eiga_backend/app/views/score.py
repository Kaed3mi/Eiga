import base64

from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Score, User, Bangumi
from app.serializers import BangumiModelSerializer, ScoreModelSerializer
from app.utils.utils import getBangumiScoreAndRank, urlToImgDate
from eiga_backend.settings import ASSETS_ROOT, RANK_PAGE_SIZE


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


class BangumiRankQuery(APIView):
    """
    需要page字段，每个页面只许展示5个番组，所以返回的番组是5*page - 4到5*page排名的番组
    """

    def get(self, request):
        page = int(request.GET.get('page'))
        print(request.GET)
        try:
            if RANK_PAGE_SIZE * page - RANK_PAGE_SIZE > Bangumi.objects.count():
                raise Exception('页数过大！')
            total = Bangumi.objects.count()
            raw_bangumis = []
            for bangumi in Bangumi.objects.all():
                rater_cnt = Score.objects.filter(bangumi_id=bangumi.bangumi_id).__len__()
                total_score = Score.objects.filter(bangumi_id=bangumi.bangumi_id).aggregate(total=Sum('score'))
                bangumi.bangumi_rater_cnt = rater_cnt
                bangumi.bangumi_score = total_score['total'] / rater_cnt if total_score['total'] else 0.0
                raw_bangumis.append(bangumi)
            print(raw_bangumis)
            sorted_bangumis = sorted(raw_bangumis, key=lambda x: x.bangumi_score, reverse=True)
            print(sorted_bangumis)
            bangumis = []
            for bangumi in sorted_bangumis:
                bangumis.append({
                    'bangumi_id': bangumi.bangumi_id,
                    'bangumi_name': bangumi.bangumi_name,
                    'bangumi_score': bangumi.bangumi_score,
                    'bangumi_rank': len(bangumis) + 1,
                    'bangumi_rater_cnt': bangumi.bangumi_rater_cnt,
                    'image': urlToImgDate(bangumi.image)
                })
        except Exception as e:
            print(e)
            return Response(1)
        return Response({
            'page_size': RANK_PAGE_SIZE,
            'bangumis': bangumis,
            'total': total
        })


class MyBangumiQuery(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        if Score.objects.filter(user_id_id=user_id).__len__() == 0:
            return Response({'bangumis': []})
        obj_list = Score.objects.filter(user_id_id=user_id)
        bangumis = []
        for obj in obj_list:
            bangumi = Bangumi.objects.get(bangumi_id=obj.bangumi_id.bangumi_id)
            bangumis.append({
                'bangumi_id': bangumi.bangumi_id,
                'bangumi_name': bangumi.bangumi_name,
                'image': urlToImgDate(bangumi.image),
                'my_score': obj.score
            })
            # print(bangumis)
        bangumis = sorted(bangumis, key=lambda x: x['my_score'], reverse=True)
        return Response({
            'bangumis': bangumis
        })
