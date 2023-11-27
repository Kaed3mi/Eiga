from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Bangumi
from app.models import BangumiRelationship
from app.models import Character
from django.db.models import Q
from app.serializers import BangumiModelSerializer


class BangumiRelationshipQuery(APIView):
    def get(self, request):
        bangumi_id = int(request.GET.get('bangumi_id'))
        obj_list_data = []
        print('search BangumiRelationshipQuery: bangumi_id=', bangumi_id)
        try:
            list = BangumiRelationship.objects.filter(a_id=int(bangumi_id))
            print(list)
            for obj in list:
                obj_list_data.append({
                    "relation": obj.relation,
                    "bangumi_id": BangumiModelSerializer(obj.b_id).data
                })
        except Exception as e:
            print('BangumiRelationshipQuery failed', e)
            return Response(1)
        print('BangumiRelationshipQuery succeed')
        return Response({
            'bangumis': obj_list_data
        })


class BangumiBangumiUpdate(APIView):
    def post(self, request):
        print(request.data.get('bangumis'))
        bangumis = list(request.data.get('bangumis'))
        bangumi_id = int(request.data.get('bangumi_id'))
        bangumis_bangumi_list = BangumiRelationship.objects.filter(a_id=bangumi_id)
        for bangumis_bangumi in bangumis_bangumi_list:
            bangumis_bangumi.delete()
        for attribute in bangumis:
            bangumiA = Bangumi.objects.get(bangumi_id=bangumi_id)
            bangumiB = Bangumi.objects.get(bangumi_id=attribute['bangumi_id'])
            relate = BangumiRelationship.objects.create(
                a_id=bangumiA,
                b_id=bangumiB,
                relation=attribute['bangumi_relation']
            )
            relate.save()
        return Response(1)
