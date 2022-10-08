from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.db.models import Sum, Avg, Count, Min, Max 
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import UserSerializer, UserSerializerWithToken, NotificationTokenSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics
from django.contrib.auth import logout
from engineer.models import Engineer, Area
User = get_user_model()
from rest_framework.generics import ListCreateAPIView
from machine.models import Machine, Call
from .models import NotificationToken


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if(hasattr(self.object, 'engineer')):
            t = 0
            ms = self.object.engineer.area.machines.all()
            for m in ms:
                if m.machine_points:

                    t = t + m.machine_points

            context['engineer'] = self.object.engineer
            context['pending_calls'] = self.object.engineer.call_set.filter(status='incomplete')
            context['completed_calls'] = self.object.engineer.call_set.filter(status='completed')
            context['dispatched_calls'] = self.object.engineer.call_set.filter(status='dispatched')
            context['machines'] = Machine.objects.filter(area=self.object.engineer.area)
            context['total_points'] = int(self.object.engineer.area.machines.all().aggregate(Sum('machine_points'))['machine_points__sum'])
            # context['total_points_v2'] = t
            # i = 1
            # for area in Area.objects.all():
            #     context['total_points_{}'.format(i)] = area.machines.aggregate(points_ta01=Sum('machine_points'))
            #     i = i + 1
            if self.object.is_superuser:
            #context['total_points_TA01'] = int(Area.objects.get(name='TA01').machines.aggregate(points_ta01=Sum('machine_points'))['points_ta01'])

                context['total_points_TA02'] = int(Area.objects.get(name='TA02').machines.aggregate(points_ta02=Sum('machine_points'))['points_ta02'])
                context['total_points_TA03'] = int(Area.objects.get(name='TA03').machines.aggregate(points_ta03=Sum('machine_points'))['points_ta03'])
                context['total_points_TA04'] = int(Area.objects.get(name='TA04').machines.aggregate(points_ta04=Sum('machine_points'))['points_ta04'])
                context['total_points_TA05'] = int(Area.objects.get(name='TA05').machines.aggregate(points_ta05=Sum('machine_points'))['points_ta05'])
                context['total_points_TA01'] = int(Area.objects.get(name='TA01').machines.aggregate(points_ta01=Sum('machine_points'))['points_ta01'])
        elif self.object.is_superuser:
            context['pending_calls'] = Call.objects.filter(status='incomplete')
            context['completed_calls'] = Call.objects.filter(status='completed')
            context['dispatched_calls'] = Call.objects.filter(status='dispatched')

            context['machines'] = Machine.objects.all()
            context['total_points'] = int(Machine.objects.all().aggregate(Sum('machine_points'))['machine_points__sum'])

            context['total_points_TA01'] = int(Area.objects.get(name='TA01').machines.aggregate(points_ta01=Sum('machine_points'))['points_ta01'])

            context['total_points_TA02'] = int(Area.objects.get(name='TA02').machines.aggregate(points_ta02=Sum('machine_points'))['points_ta02'])
            context['total_points_TA03'] = int(Area.objects.get(name='TA03').machines.aggregate(points_ta03=Sum('machine_points'))['points_ta03'])
            context['total_points_TA04'] = int(Area.objects.get(name='TA04').machines.aggregate(points_ta04=Sum('machine_points'))['points_ta04'])
            context['total_points_TA05'] = int(Area.objects.get(name='TA05').machines.aggregate(points_ta05=Sum('machine_points'))['points_ta05'])

            
        else:
            context['pending_calls'] = 'not Engineer'
            context['completed_calls'] = 'not Engineer'
            context['dispatched_calls'] = 'not Engineer'

            



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


class CreateNotificationToken(generics.CreateAPIView):

    # queryset = NotificationToken.objects.all()
    serializer_class = NotificationTokenSerializer
    permission_classes = (AllowAny,)
    # def create(self, request, *args, **kwargs): # don't need to `self.request` since `request` is available as a parameter.

    #     # your custom implementation goes here

    #     return Response(status=status.HTTP_302_FOUND)


class NotificationTokenView(APIView):

    def get(self, request, *args, **kwargs):
        notification_tokens = NotificationToken.objects.all()
        serializer = NotificationTokenSerializer(notification_tokens, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = NotificationTokenSerializer(data=request.data)
        if serializer.is_valid():
            nToken = serializer.save()
            user = get_user_model().objects.get(id=request.user.id)
            user.token = nToken
            user.save()
            serializer = NotificationTokenSerializer(nToken)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)