from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Bangumi
from app.models import CharacterBangumi
from app.models import Character


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
