from django.urls import path
from django.contrib.auth import views as auth_views
from appresult.views import *

app_name = 'result'

urlpatterns = [
    path('', Result.as_view(template_name='result/resultPage.html'), name='result'),
    path('get_lecture_combinations/', get_lecture_combinations, name='get_lecture_combinations'),
]