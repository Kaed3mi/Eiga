import base64

from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Bangumi
from app.models import CharacterBangumi
from app.models import Character
from app.utils.utils import urlToImgDate
from eiga_backend.settings import ASSETS_ROOT


class BangumiCharacterQuery(APIView):
    def get(self, request):
        bangumi_id = int(request.GET.get('bangumi_id'))
        character_list_data = []
        print('query bangumiCharacter: id=', bangumi_id)
        try:
            character_bangumi_list = CharacterBangumi.objects.filter(bangumi_id=bangumi_id)
            for character_bangumi in character_bangumi_list:
                character: Character = Character.objects.get(character_id=character_bangumi.character_id.character_id)
                character_list_data.append({
                    "id": character.character_id,
                    "character_name": character.character_name,
                })
        except Exception as e:
            print(e)
            return Response(1)
        return Response({
            'characters': character_list_data,
        })


class BangumiCharaterUpdate(APIView):
    def post(self, request):
        print(request.data)
        bangumi_id = int(request.data.get('bangumi_id'))
        characters = list(request.data.get('characters'))
        character_bangumi_list = CharacterBangumi.objects.filter(bangumi_id=bangumi_id)
        for character_bangumi in character_bangumi_list:
            print("deleting " + str(character_bangumi.character_id.character_id))
            character_bangumi.delete()
        for relation in characters:
            character = Character.objects.get(character_id=relation['character_id'])
            bangumi = Bangumi.objects.get(bangumi_id=bangumi_id)
            relate = CharacterBangumi.objects.create(character_id=character, bangumi_id=bangumi)
            relate.save()
        print(characters)
        return Response(1)


class StarringQuery(APIView):
    def get(self, request):
        character_id = request.GET.get('character_id')
        print('角色id：' + str(character_id))
        bangumiList = CharacterBangumi.objects.filter(character_id_id=character_id)
        starring_bangumis = []
        for bangumi in bangumiList:
            starring_bangumi: Bangumi = Bangumi.objects.get(bangumi_id=bangumi.bangumi_id.bangumi_id)
            starring_bangumis.append({
                'bangumi_id': starring_bangumi.bangumi_id,
                'bangumi_name': starring_bangumi.bangumi_name,
                'image': urlToImgDate(starring_bangumi.image)
            })
        print('出演番组表：' + str(starring_bangumis))
        return Response({
            'starring_bangumis': starring_bangumis
        })
