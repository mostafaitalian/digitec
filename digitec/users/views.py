from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import UserSerializer, UserSerializerWithToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import logout
from engineer.models import Engineer
User = get_user_model()
from rest_framework.generics import ListCreateAPIView
from machine.models import Machine


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if(hasattr(self.object, 'engineer')):
            context['engineer'] = self.object.engineer
            context['pending_calls'] = self.object.engineer.call_set.filter(status='pending')
            context['completed_calls'] = self.object.engineer.call_set.filter(status='completed')

        else:
            context['engineer'] ='not Enginner'
            context['pending_calls'] = 'not Engineer'
            context['completed_calls'] = 'not Engineer'
            context['machines'] = Machine.objects.all()
            



        return context
    

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
# @permission_classes(AllowAny)
# @permission_classes(AllowAny)
@authentication_classes(SessionAuthentication)
@api_view(['GET'])
def current_user(request):
    if request.user.is_authenticated == True:
        serializer = UserSerializerWithToken(User.objects.get(username=request.user.username))
        # logout(request,)
        # serializer.data['is_authenticated'] = request.user.is_authenticated

        return Response({'is_Athenticated':request.user.is_authenticated,  'user':serializer.data}, status=status.HTTP_200_OK)
    return Response({'is_Athenticated':request.user.is_authenticated,'user': 'not authenticated yet'})
@api_view(['GET'])
def current_user2(request):

        logout(request)
        return Response({'helloo':'hello'}, status=status.HTTP_200_OK)

class UserList(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        queryset = User.objects.all()
        if request.user.is_superuser:
            return Response([UserSerializerWithToken(user).data for user in queryset], status=status.HTTP_200_OK)
        # return Response({'availability': 'you do not have authorization to see users'})
        return Response([UserSerializerWithToken(user).data for user in queryset], status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serialize = UserSerializer(data=request.data)
        if serialize.is_valid(raise_exception=True):
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