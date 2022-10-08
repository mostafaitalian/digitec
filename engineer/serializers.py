from rest_framework import serializers
from .models import Engineer, Area
from machine.serializers import CallSerializer, MachineSerializer, CallAreaSerializer, MachineAreaSerializer
# from customer.serializers import CustomerSerializer


class EngineerSerializer(serializers.ModelSerializer):
    # calls = serializers.ListField()
    call_set = CallSerializer(many=True, required=False)
    class Meta:
        model = Engineer
        fields = '__all__'




class AreaSerializer(serializers.ModelSerializer):
    engineer_set = EngineerSerializer(many=True, required=False)
    machines = MachineSerializer(many=True,required=False)
    # customers = CustomerSerializer(many=True)
    class Meta:
        model = Area
        fields = ['id','name', 'engineer_set', 'machines']

class EngineerAreaSerializer(serializers.ModelSerializer):
    # calls = serializers.ListField()
    call_set = CallAreaSerializer(many=True, required=False)
    class Meta:
        model = Engineer
        fields = ['id', 'name', 'user' ,'area', 'call_set' ,'begin_at', 'finish_at']
class AreaAreaSerializer(serializers.ModelSerializer):
    engineer_set = EngineerAreaSerializer(many=True, required=False)
    machines = MachineAreaSerializer(many=True,required=False)
    # customers = CustomerSerializer(many=True)
    class Meta:
        model = Area
        fields = ['id','name', 'engineer_set', 'machines']