"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.conf import settings
from rest_framework.routers import DefaultRouter


doc_patterns = [
    # YOUR PATTERNS
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


admin_endpoint = [
    
    path('admin/users/', include(('accounts.users.urls.admin'))),
    path('admin/users/', include(('accounts.students.urls.admin'))),
    path('admin/', include(('apps.courses.urls.admin')))


]

front_endpoint = [
    
    path('user/auth/', include(('accounts.users.urls.front'))),
    path('user/profile/', include(('accounts.students.urls.front')))

   
] 



urlpatterns = [

    path('api/v1/', include(front_endpoint)),
    path('api/v1/', include(admin_endpoint)),
    path('api/v1/', include(doc_patterns)),
]
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     #path('api/v1/user/', include(user_manager_endpoint)),
#     path('api/v1/', include(doc_patterns)),
#     path('auth/', include((UserRouter)))
# ] 
