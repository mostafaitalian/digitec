from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from . import views
app_name = 'machine'
serialize_urls = [path('api/', views.MachineCreateReadView.as_view(), name='api_create'),
                  path('api/<str:slug>/update/', views.MachineUpdateReadView.as_view(), name='api_update')]
urlpatterns = [path('create', views.CreateMachineView1.as_view(), name="create"),
               path('list', views.MachineList.as_view(), name='list'),
               path('call/create', views.CallCreateView.as_view(), name="call_create"),
               path('category/create', views.CreateCategory.as_view(), name='create_category'),
               path('', include(serialize_urls))]