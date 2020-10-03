from rest_framework import serializers
from .models import Engineer, Area
from machine.serializers import CallSerializer
# from customer.serializers import CustomerSerializer


class EngineerSerializer(serializers.ModelSerializer):
    # calls = serializers.ListField()
    call_set = CallSerializer(many=True, required=False)
    class Meta:
        model = Engineer
        fields = '__all__'
class AreaSerializer(serializers.ModelSerializer):
    engineer_set = EngineerSerializer(many=True, required=False)
    # customers = CustomerSerializer(many=True)
    class Meta:
        model = Area
        fields = '__all__'