from rest_framework import serializers
from app.models import User, Character, Bangumi, Blog


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CharacterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"


class BangumiModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bangumi
        fields = "__all__"


class BlogModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
