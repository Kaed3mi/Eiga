import mimetypes

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
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
import io


class CharacterQuery(APIView):
    def get(self, request):
        print("request: ")
        print(request.GET.get('character_id'))
        character_id = request.GET.get('character_id')
        print('query character: id=' + character_id)
        character = Character.objects.get(character_id=character_id)
        with open(character.image, 'rb') as f:
            image_data = base64.b64encode(f.read())
        print(character.intro)
        Json = json.loads(character.intro.replace("'", '"'))
        print(Json)
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


class CharacterUpdate(APIView):
    def post(self, request):
        # print(request.data.get("character_id"))
        character_id = request.data.get("character_id")
        # print(request.data.get("attributes"))
        # print(request.data.get("introduction"))
        # print(request.data.get("image"))
        image_base64 = request.data.get("image")
        image_str = base64.b64decode(image_base64.split(',')[1])
        image_type = image_base64.split(';')[0].split(':')[1]
        # print(image_type)
        dic = {"attributes": request.data.get("attributes"), "introduce": request.data.get("introduction")}
        # print(str(dic))
        print(request.data.get("attributes"))


        character_info = Character.objects.get(character_id=character_id)
        character_info.intro = str(dic)
        character_info.save()
        file_ext = mimetypes.guess_extension(image_type)
        if not file_ext:
            file_ext = '.png'
        print('characters/' + character_id + file_ext)
        if character_info.image == None:
            print("the user has the default avatar and we change it to " + 'characters/' + character_id + file_ext)
            character_info.image = 'characters/' + character_id + file_ext
            character_info.save()
        else:
            print("now we will delete the original avatar")
            legacy_image = character_info.image
            print(legacy_image)
            if os.path.exists(legacy_image):
                os.remove(legacy_image)
            else:
                print("path didn't find check it")
            character_info.image = 'characters/' + character_id + file_ext
            character_info.save()

        with open('characters/' + character_id + file_ext, 'wb') as f:
            f.write(image_str)
        return Response(1)

class CharacterSelect(APIView):
    def get(self, request):
        print(request.GET.get("keyword"))
        keyword = str(request.GET.get("keyword"))
        print(keyword)
        characters = Character.objects.filter(Q(character_name__icontains=keyword))
        print(characters.__len__())
        print(list(characters))
        character_list = list(characters)
        characters_json = [{'character_id': character.character_id, 'value': character.character_name} for character in character_list]
        print(characters_json)
        return Response(characters_json)
