from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from . import views
app_name = 'machine'
serialize_urls = [path('api/', views.MachineCreateReadView.as_view(), name='api_create'),
                  path('api/<str:slug>/update/', views.MachineUpdateReadView.as_view(), name='api_update'),
                  path('api/machines/customer/<int:customer_id>/', views.MachineOfCustomerListApi.as_view())]
urlpatterns = [path('create/', views.CreateMachineView1.as_view(), name="create"),
               path('list1/', views.MachineList.as_view(), name='list'),
               path('call/create/', views.CallCreateView.as_view(), name="call_create"),
               path('call/list/', views.CallListView.as_view(), name='call_list'),
               path('call/detail/<pk>/', views.CallDetailView.as_view(), name='call_detail'),
               path('detail/<pk>/', views.MachineDetailView.as_view(), name='machine_detail'),
               path('category/create/', views.CreateCategory.as_view(), name='create_category'),
               path('report/create/', views.ReportCreate.as_view(), name='create_report'),
               path('call/<pk>/report/create/', views.create_report, name='create_report1'),
               path('report/list/', views.ReportList.as_view(), name='report_list'),
               path('machine/list/cutom/', views.MachineListCustom.as_view(),  name='machine_list_custom'),
               path('', include(serialize_urls))]