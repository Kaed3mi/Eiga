from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Bangumi
from app.models import Character
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import json
import os
import shutil
import base64


class CharacterQuery(APIView):
    def post(self, request):
        character_id = str(1)
        character = Character.objects.get(character_id=character_id)
        # print(character.image)
        with open(character.image, 'rb') as f:
            image_data = base64.b64encode(f.read())
        Json = json.loads(character.intro)
        # print(Json)
        Json["image"] = str(image_data)[2:-1]
        # print(Json)
        return JsonResponse(Json)
