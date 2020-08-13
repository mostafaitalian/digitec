from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from rest_framework.decorators import api_view
from .serializers import UserSerializer, UserSerializerWithToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout
User = get_user_model()
from rest_framework.generics import ListCreateAPIView


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserListView(LoginRequiredMixin, ListView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_list_view = UserListView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()

@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def current_user2(request):

        logout(request)
        return Response('helloo', status=status.HTTP_200_OK)

class UserList(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        queryset = User.objects.all()
        if request.user.is_superuser:
            return Response([UserSerializerWithToken(user).data for user in queryset], status=status.HTTP_200_OK)
        # return Response({'availability': 'you do not have authorization to see users'})
        return Response([UserSerializerWithToken(user).data for user in queryset], status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serialize = UserSerializerWithToken(request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)   
class UserList1(ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializerWithToken
    #queryset = User.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return None