from django.urls import path
from . import views
app_name = 'customer'

urlpatterns = [
    path('', views.CustomerListView.as_view(), name='list'),
    path('create/', views.CustomerCreateView1.as_view(), name='create'),
    path('detail/<str:slug>/', views.CustomerDetail.as_view(), name='detail'),
    path('<str:slug>/update',views.CustomerUpdateView.as_view(), name="update"),
    path('<str:slug>/delete', views.CustomerDeleteView.as_view(), name='delete')]