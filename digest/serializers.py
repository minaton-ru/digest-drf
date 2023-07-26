from .models import Digest
from rest_framework import serializers


class DigestSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True)

    class Meta:
        model = Digest
        fields = ['pk', 'posts', ]
