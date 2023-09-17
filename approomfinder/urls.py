from django.urls import path
from .views import *

app_name = 'roomfinder'

urlpatterns = [
    path('', RoomFinder.as_view(template_name='roomfinder/roomfinderPage.html'), name='roomfinder'),
    # path('delete_timetable/', delete_timetable , name='delete_timetable'),
]