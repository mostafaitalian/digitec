from django.urls import path, include
from engineer import views
from rest_framework import routers



app_name= 'engineer'
router = routers.DefaultRouter()
router.register(r'areas1',views.AreaListApi1)
serialize_urls = [
 
    path('api/engineers/', views.EngineerListApi.as_view(), name='api_engineers-create'),
    path('api/areas/', views.AreaListApi.as_view(), name='api_areas-create'),
    ]
urlpatterns = [path('review/create', views.review_create, name='engineer_review_create'),
               path('create/', views.EngineerCreateView.as_view(), name='engineer_create'),
               path('create/area', views.AreaCreateView.as_view(), name='area_create'),
               path('create/area-engineer', views.AreaEngineerCreateView.as_view(), name='area-engineer-create'),
               path('area/list/', views.AreaList.as_view(), name='area_list'),
               path('review/<int:review_id>', views.ReviewDetailView.as_view(),name='engineer_review_detail'),
               path('review/thank_you', views.thank_you, name='engineer_review_thank_you'),
               path('', include(router.urls)),
               path('review/approval/<int:review_id>', views.preview_review, name='preview_for_approve'),
               path('', include(serialize_urls)),
               ]