from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import User, NotificationToken
from engineer.serializers import EngineerSerializer



class UserSerializer(serializers.ModelSerializer):
    engineer = EngineerSerializer(required=False)

    class Meta:
        model = User
        fields ='__all__'

class NotificationTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationToken
        fields ='__all__'

class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    engineer = EngineerSerializer()

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
           instance.set_password(password)
        instance.save()
        return instance   
        

    class Meta:
        model=User
        fields='__all__'

        # fields=('token', 'username','password')


class UserSerializerWithNormalToken(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = '__all__'