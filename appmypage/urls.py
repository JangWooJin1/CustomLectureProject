from django.urls import path
from .views import *

app_name = 'mypage'

urlpatterns = [
    path('', Mypage.as_view(template_name='mypage/myTimeTablePage.html'), name='mypage'),
    path('delete_timetable/', delete_timetable , name='delete_timetable'),
]