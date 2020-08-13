from rest_framework import serializers
from .models import Machine
from engineer.models import Engineer


class MachineSerializer(serializers.ModelSerializer):
    # engineers = serializers.PrimaryKeyRelatedField(many=True, queryset=Engineer.objects.all())
    # engineerss = serializers.ListSerializer(child=engineers)
    class Meta:
        model = Machine
        fields= ('category', 'customer', 'department', 'area','name', 'serial',
        'serial2', 'machine_model', 'slug', 'description', 'added', 'speed','engineers' )
        # exclude=('engineers',)