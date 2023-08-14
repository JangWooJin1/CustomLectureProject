"""CustomLecture URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from myapp.views import mainPage, get_classification_options, get_univ_options, get_major_options, get_lecture, add_userbasket

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mainPage/', mainPage.as_view(), name='mainPage'),
    path('mainPage/get_classification_options', get_classification_options, name='get_classification_options'),
    path('mainPage/get_univ_options', get_univ_options, name='get_univ_options'),
    path('mainPage/get_major_options', get_major_options, name='get_major_options'),
    path('mainPage/get_lecture', get_lecture, name='get_lecture'),
    path('mainPage/add_userbasket', add_userbasket, name='add_userbasket'),
]
