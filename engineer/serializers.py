from rest_framework import serializers
from .models import Engineer


class EngineerSerializer(serializers.ModelSerializer):
    class Meta:
        calls = serializers.ListField(source='calls')
        model = Engineer
        fields = '__all__'