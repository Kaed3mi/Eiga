from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Bangumi
from app.models import CharacterBangumi
from app.models import Character
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import json
import os
import shutil
import base64


class CharacterQuery(APIView):
    def get(self, request):
        character_id = request.GET.get('character_id')
        print('query character: id=' + character_id)
        character = Character.objects.get(character_id=character_id)
        # print(character.image)
        with open(character.image, 'rb') as f:
            image_data = base64.b64encode(f.read())
        Json = json.loads(character.intro)
        # print(Json)
        Json["image"] = str(image_data)[2:-1]
        Json["character_name"] = str(character.character_name)
        return JsonResponse(Json)


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
