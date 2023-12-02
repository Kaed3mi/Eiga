from rest_framework import serializers
from app.models import User, Character, Bangumi, Blog, Score
from app.utils.utils import urlToImgDate


class ImageField(serializers.CharField):
    def to_representation(self, value):
        # 将字段的值转换为大写
        return urlToImgDate(value)


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


class ScoreModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = "__all__"
