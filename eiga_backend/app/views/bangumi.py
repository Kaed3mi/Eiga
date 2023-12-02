import base64
import mimetypes
import os

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Bangumi
from app.utils.utils import getBangumiScoreAndRank, urlToImgDate
from eiga_backend.settings import ASSETS_ROOT


# TODO 这里的操作需要核验权限组是否达标，不过呢我还没写。
class BangumiCreate(APIView):
    def post(self, request):
        bangumi_name = str(request.data.get('bangumi_name'))
        bangumi_intro = str(request.data.get('bangumi_intro'))
        print(request.data.get('image'))

        image_base64 = request.data.get("image")
        image_str = base64.b64decode(image_base64.split(',')[1])
        image_type = image_base64.split(';')[0].split(':')[1]
        file_ext = mimetypes.guess_extension(image_type)
        if not file_ext:
            file_ext = '.png'

        try:
            obj = Bangumi(
                bangumi_name=bangumi_name,
                bangumi_intro=bangumi_intro
            )
            obj.save()
            print(ASSETS_ROOT + 'bangumi/' + str(obj.bangumi_id) + file_ext)
            obj.image = 'bangumi/' + str(obj.bangumi_id) + file_ext
            obj.save()
            with open(ASSETS_ROOT + 'bangumi/' + str(obj.bangumi_id) + file_ext, 'wb') as f:
                f.write(image_str)
        except Exception as e:
            print(e)
            return Response(1)
        return Response({"bangumi_id": obj.bangumi_id})


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
            'bangumi_score': obj.bangumi_score,
            'rank': obj.rank,
            'image': urlToImgDate(obj.image)
        })


class BangumiSearch(APIView):
    def get(self, request):
        pattern = request.GET.get('pattern')
        bangumi_list_data = []
        print('search bangumi: pattern=' + pattern)
        try:
            bangumi_list = Bangumi.objects.filter(bangumi_name__contains=pattern)
            bangumi_rank_dict = getBangumiScoreAndRank()
            for bangumi in bangumi_list:
                image_url = bangumi.image
                bangumi_list_data.append({
                    "id": bangumi.bangumi_id,
                    "name": bangumi.bangumi_name,
                    "description": bangumi.bangumi_intro,
                    "image": urlToImgDate(image_url),
                    'score': bangumi_rank_dict[bangumi.bangumi_id]['bangumi_score'],
                    'rank': bangumi_rank_dict[bangumi.bangumi_id]['bangumi_rank'],
                    'rater_cnt': bangumi_rank_dict[bangumi.bangumi_id]['rater_cnt']
                })
        except Exception as e:
            print(e)
            return Response(1)
        return Response({
            'bangumis': bangumi_list_data
        })


class BangumiSelect(APIView):
    def get(self, request):
        print(request.GET.get("keyword"))
        keyword = str(request.GET.get("keyword"))
        bangumis = Bangumi.objects.filter(Q(bangumi_name__icontains=keyword))
        print(list(bangumis))
        bangumi_json = [{'bangumi_id': bangumi.bangumi_id, 'value': bangumi.bangumi_name} for bangumi in list(bangumis)]
        return Response(bangumi_json)


class BangumiUpdate(APIView):
    def post(self, request):
        print(request.data.get('bangumi_intro'))
        bangumi_id = int(request.data.get('bangumi_id'))
        # 图片
        image_base64 = request.data.get("image")
        image_str = base64.b64decode(image_base64.split(',')[1])
        image_type = image_base64.split(';')[0].split(':')[1]

        # 修改名字以及介绍
        bangumi_name = str(request.data.get("bangumi_name"))
        bangumi_intro = str(request.data.get("bangumi_intro"))
        print(bangumi_intro)
        bangumi_info = Bangumi.objects.get(bangumi_id=bangumi_id)
        print(bangumi_info.bangumi_intro)
        bangumi_info.bangumi_name = bangumi_name
        bangumi_info.bangumi_intro = bangumi_intro
        bangumi_info.save()
        file_ext = mimetypes.guess_extension(image_type)
        if not file_ext:
            file_ext = '.png'
        print('bangumi/' + str(bangumi_id) + file_ext)
        if bangumi_info.image == None:
            print("the user has the default avatar and we change it to " + 'bangumi/' + str(bangumi_id) + file_ext)
            bangumi_info.image = 'bangumi/' + str(bangumi_id) + file_ext
            bangumi_info.save()
        else:
            print("now we will delete the original bangumi")
            legacy_image = bangumi_info.image
            print(legacy_image)
            if os.path.exists(ASSETS_ROOT + legacy_image):
                print(ASSETS_ROOT + legacy_image)
                os.remove(ASSETS_ROOT + legacy_image)
            else:
                print("path didn't find check it")
            bangumi_info.image = 'bangumi/' + str(bangumi_id) + file_ext
            bangumi_info.save()

        with open(ASSETS_ROOT + 'bangumi/' + str(bangumi_id) + file_ext, 'wb') as f:
            f.write(image_str)

        return Response(1)
