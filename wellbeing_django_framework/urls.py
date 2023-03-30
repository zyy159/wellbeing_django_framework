"""wellbeing_django_framework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path as url
from django.urls import path, include, re_path
from wellbeing_django_framework import views
from rest_framework import routers
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns
from rest_auth.registration.views import VerifyEmailView
from allauth.account.views import confirm_email


# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

snippets_urlpatterns = [
    path('', views.api_root),
    path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),

]
snippets_urlpatterns = format_suffix_patterns(snippets_urlpatterns)

auth_urlpatterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view(),
     name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
     name='account_confirm_email'),
]
auth_urlpatterns = format_suffix_patterns(auth_urlpatterns)

exercise_urlpatterns = [
    url(r'^exercise/', include('wellbeing_django_framework.exercise.urls')),
]

exercise_urlpatterns = format_suffix_patterns(exercise_urlpatterns)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^SignIn/',views.login),
    url(r'^SignUp/',views.register),
    # path('', include(router.urls)),
    path('', include(snippets_urlpatterns)),
    path('', include(auth_urlpatterns)),
    path('', include(exercise_urlpatterns)),
    path('api-auth/', include('rest_framework.urls')),
    # path('snippets/', views.snippet_list),
    # path('snippets/<int:pk>/', views.snippet_detail),
    # ...
    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
    path('openapi', get_schema_view(
        title="Wellbeing",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    # ...
    # ...
    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    # ...
    # Route TemplateView to serve the ReDoc template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
]
