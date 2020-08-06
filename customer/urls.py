from django.urls import path
from . import views
app_name = 'customer'

urlpatterns = [
    path('', views.CustomerListView.as_view(), name='list'),
    path('create/', views.CustomerCreateView.as_view(), name='create'),
    path('detail/<str:slug>/', views.CustomerDetail.as_view(), name='customer-detail'),
    path('<str:slug>/update',views.CustomerUpdateView.as_view(), name="customer-update"),
    path('<str:slug>/delete', views.CustomerDeleteView.as_view(), name='customer-delete'),
    path('department/create/', views.DepartmentCreateView.as_view(), name='deprtment-create')
    ]