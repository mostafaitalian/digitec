from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
# from rest_framework_jwt.views import (obtain_jwt_token,
#  RefreshJSONWebToken,
#  ObtainJSONWebToken,
#  )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from machine.models import Call

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('customer/', include('customer.urls', namespace='customer')),
    path('machine/', include('machine.urls', namespace='machine')),
    path('engineer/', include('engineer.urls', namespace='engineer')),
    path("", TemplateView.as_view(template_name="pages/home.html",
    extra_context={'dispatched_calls': Call.objects.filter(status='dispatched').order_by('-created_date')[:4],
    'pending_calls': Call.objects.filter(status='incomplete').order_by('-created_date')[:4],
    'completed_calls': Call.objects.filter(status='completed').order_by('-created_date')[:4]}),
    name="home"),
    
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path(
        "test/",
        TemplateView.as_view(template_name="pages/test.html"),
        name="about",
    ),
    path("contact-us/", TemplateView.as_view(template_name="pages/contactus.html"), name="contact-us"),

    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path(
        "users/",
        include("digitec.users.urls", namespace="users"),
    ),
    path("accounts/", include("allauth.urls")),
    # path('token-auth/', obtain_jwt_token),
    # path('api/token-auth2/', ObtainJSONWebToken.as_view()),
    # path('token-auth-refresh/', RefreshJSONWebToken.as_view())
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Your stuff: custom urls includes go here
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
