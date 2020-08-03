from rest_framework import serializers
from .models import Machine


class MachineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Machine
        fields=('name', 'slug', 'serial', 'speed', 'category', 'customer','department')