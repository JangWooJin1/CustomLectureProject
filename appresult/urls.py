from django.urls import path
from django.contrib.auth import views as auth_views
from appresult.views import *

app_name = 'result'

urlpatterns = [
    #path('', Search.as_view(template_name='search/mainPage.html'), name='result'),
]