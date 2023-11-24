from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Bangumi


# TODO 这里的操作需要核验权限组是否达标，不过呢我还没写。
class BangumiInsert(APIView):
    def post(self, request):
        bangumi_id = str(request.data.get('bangumi_id'))
        bangumi_name = str(request.data.get('bangumi_name'))
        bangumi_intro = str(request.data.get('bangumi_intro'))
        print(request.data)
        try:
            obj = Bangumi(
                bangumi_id=bangumi_id,
                bangumi_name=bangumi_name,
                bangumi_intro=bangumi_intro
            )
            obj.save()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(0)


class BangumiUpdate(APIView):
    def post(self, request):
        bangumi_id = str(request.data.get('bangumi_id'))
        bangumi_name = str(request.data.get('bangumi_name'))
        bangumi_intro = str(request.data.get('bangumi_intro'))
        print(request.data)
        try:
            obj = Bangumi.objects.get(bangumi_id=bangumi_id)
            obj.bangumi_name = bangumi_name
            obj.bangumi_intro = bangumi_intro
            obj.save()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(0)


class BangumiDelete(APIView):
    def post(self, request):
        bangumi_id = str(request.data.get('bangumi_id'))
        try:
            obj = Bangumi.objects.get(bangumi_id=bangumi_id)
            obj.delete()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(0)


class BangumiQuery(APIView):
    def get(self, request):
        bangumi_id = request.GET.get('bangumi_id')
        print('query bangumi: id=' + bangumi_id)
        try:
            obj = Bangumi.objects.get(bangumi_id=bangumi_id)
        except Exception as e:
            print(e)
            return Response(1)
        return Response({
            'bangumi_name': obj.bangumi_name,
            'bangumi_intro': obj.bangumi_intro,
            'bangumi_score': obj.bangumi_score
        })


class BangumiSearch(APIView):
    def get(self, request):
        pattern = request.GET.get('pattern')
        bangumi_list_data= []
        print('search bangumi: pattern=' + pattern)
        try:
            bangumi_list = Bangumi.objects.filter(bangumi_name__contains=pattern)
            print(bangumi_list)
            for bangumi in bangumi_list:
                bangumi_list_data.append({
                    "id": bangumi.bangumi_id,
                    "name": bangumi.bangumi_name,
                })
        except Exception as e:
            print(e)
            return Response(1)
        return Response({
            'bangumis': bangumi_list_data
        })
