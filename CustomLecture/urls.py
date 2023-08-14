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
from django.urls import path, include
from myapp.views import MainPage, get_classification_options, get_univ_options, get_major_options, get_lecture, add_userbasket, delete_userbasket
# 클래스 : 단어 앞글자 대문자
# 변수 : 두번쨰 단어부터 대문자
# 함수 : 두번째 단어부터 대문자 + 첫번쨰 단어는 동사 명령형으로 할 것 ok? 슬슬 꺼야겠찌 시발새끼야좆같은넘아 개새기야 엘든링 시발새기야 좆머하노 시발롬아 그만해라 눈알 빠지겠다 시발련아 눈알 빠진다 시발색기야 노트북 화면이 도대체 얼마나 엘든링으로 채워진거고 시발련아

urlpatterns = [
    path('admin/', admin.site.urls),
    path('MainPage/', MainPage.as_view(template_name='myapp/mainPage.html'), name='MainPage'),
    path('MainPage/get_classification_options', get_classification_options, name='get_classification_options'),
    path('MainPage/get_univ_options', get_univ_options, name='get_univ_options'),
    path('MainPage/get_major_options', get_major_options, name='get_major_options'),
    path('MainPage/get_lecture', get_lecture, name='get_lecture'),
    path('MainPage/add_userbasket', add_userbasket, name='add_userbasket'),
    path('MainPage/delete_userbasket', delete_userbasket, name='delete_userbasket'),
    path('common/', include('common.urls')),
]
