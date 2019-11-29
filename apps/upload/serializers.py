from rest_framework import serializers

from .models import UploadImage


class UploadImageSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault(), write_only=True)

    class Meta:
        model = UploadImage
        fields = ('id', 'name', 'image', 'creator')

    def validate(self, validated_data):
        if not validated_data.get('image', False):
            validated_data['name'] = ''
            validated_data['image'] = self.initial_data.get('file', 'Data retrieval error')
            return validated_data
