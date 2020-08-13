
from digitec.users.serializers import UserSerializer
# from rest_framework_jwt.views import ObtainJSONWebToken


def my_jwt_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user' : UserSerializer(user, context={'request':request}).data,
        'request': request.data,
        'request2':request.user.username,
        # 'superuser': UserSerializer(user).is_superuser,
        'authenticated': request.user.is_authenticated,

    }

#inhiret from ObtainJSONWEBTOKEN to add extra data

# class customObtainJSONWebToken(ObtainJSONWebToken):

#     def post(self,request,*args, **kwargs):
#         serializer =self.serializer_class(data=request.data,context={'user': request.user, 'superuser': request.user.is_superuser})
#         # if serializer.is_valid():
