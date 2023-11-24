from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Bangumi
from app.models import BangumiRelationship
from app.models import Character
from django.db.models import Q
from app.serializers import BangumiModelSerializer


class BangumiRelationshipQuery(APIView):
    def get(self, request):
        bangumi_id = request.GET.get('bangumi_id')
        obj_list_data = []
        print('search BangumiRelationshipQuery: bangumi_id=' + bangumi_id)
        try:
            list = BangumiRelationship.objects.filter(a_id=bangumi_id)
            print(list)
            for obj in list:
                obj_list_data.append({
                    "relation": obj.relation,
                    "bangumi_id": BangumiModelSerializer(obj.b_id).data
                })
        except Exception as e:
            print(e)
            return Response(1)
        return Response({
            'bangumis': obj_list_data
        })
