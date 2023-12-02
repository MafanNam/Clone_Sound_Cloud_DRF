from rest_framework import serializers


from audio_library import models


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)


class GenreSerializer(BaseSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'name',)


class LicenseSerializer(BaseSerializer):
    class Meta:
        model = models.License
        fields = ('id', 'text',)



