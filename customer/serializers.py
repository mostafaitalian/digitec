from .models import Customer, Department
from engineer.serializers import AreaSerializer, EngineerSerializer
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
    area = AreaSerializer()
    engineers = EngineerSerializer(many=True,required=False)


    class Meta:
        model = Customer
        fields ='__all__'