from django.urls import path

from digitec.users.views import (
    user_list_view,
    user_redirect_view,
    user_update_view,
    user_detail_view,
    current_user,
    current_user2,
    UserList,
    UserList1
)

app_name = "users"
urlpatterns = [
    path('api/current-user/', current_user),
    path('api/token-user/', current_user2),
    path('api/userss/', UserList1.as_view()),
    path('api/user-list/', UserList.as_view()),
    path("", view=user_list_view, name="list"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),

]
