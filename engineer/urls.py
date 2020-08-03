from django.urls import path
from engineer import views
app_name= 'engineer'

urlpatterns = [path('review/create', views.PostCreate.as_view(), name='engineer_review_create'),
               path('create/', views.EngineerCreateView.as_view(), name='engineer_create'),
               path('create/area', views.AreaCreateView.as_view(), name='area_create'),
               path('create/area-engineer', views.AreaEngineerCreateView.as_view(), name='area-engineer-create'),

               path('review/<int:review_id>', views.ReviewDetailView.as_view(),name='engineer_review_detail'),
               path('review/thank_you', views.thank_you, name='engineer_review_thank_you'),
               path('review/approval/<int:review_id>', views.preview_review, name='preview_for_approve')]