from django.urls import path, include
from . import views
app_name = 'customer'


serializer_urls = [
    path('customers/', views.CustomerListCreateApi.as_view())
]

urlpatterns = [
    path('list/', views.CustomerListView.as_view(), name='customer-list'),
    path('create/', views.CustomerCreateView.as_view(), name='customer-create'),
    path('detail/<int:id>/', views.CustomerDetail.as_view(), name='customer-detail'),
    path('<int:id>/update',views.CustomerUpdateView.as_view(), name="customer-update"),
    path('<int:id>/delete', views.CustomerDeleteView.as_view(), name='customer-delete'),
    path('department/create/', views.DepartmentCreateView.as_view(), name='department-create'),
    path('customer/bulk', views.bulk_customers_view, name='customer_bulk'),
    path('api/', include(serializer_urls))
    ]