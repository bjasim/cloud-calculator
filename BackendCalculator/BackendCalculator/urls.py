"""
URL configuration for BackendCalculator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('aws_app/', admin.site.urls),
    path('aws/', include('aws_app.urls')),    
    path('azure/', include('azure_app.urls')),    
    path('gcp/', include('gcp_app.urls')),    
    path('oracle/', include('oracle_app.urls')),    

    path('testing/', include('testing.urls')),


]
