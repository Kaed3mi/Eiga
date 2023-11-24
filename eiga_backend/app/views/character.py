from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Bangumi
from app.models import CharacterBangumi
from app.models import Character


class CharacterSearch(APIView):
    def get(self, request):
        pattern = request.GET.get('pattern')
        obj_list_data = []
        print('search character: pattern=' + pattern)
        try:
            list = Character.objects.filter(character_name__contains=pattern)
            print(list)
            for obj in list:
                obj_list_data.append({
                    "id": obj.character_id,
                    "name": obj.character_name,
                })
        except Exception as e:
            print(e)
            return Response(1)
        return Response({
            'characters': obj_list_data
        })
