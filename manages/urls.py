"""manages URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,re_path
from app01 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('classes/', views.classes),
    path('students/', views.students),
    path('teachers/', views.teachers),
    path('teacher_add/', views.teacher_add),
    re_path('edit_teacher-(\d+)/', views.edit_teacher),
    path('upload/',views.upload),
    path('uploadformdata/',views.uploadformdata),
    path('uploadiframe/',views.uploadiframe),
    path('logout/',views.logout)
]
