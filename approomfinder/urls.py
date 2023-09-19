from django.urls import path
from .views import *

app_name = 'roomfinder'

urlpatterns = [
    path('', RoomFinder.as_view(template_name='roomfinder/roomfinderPage.html'), name='roomfinder'),
    path('get_empty_rooms/', get_empty_rooms , name='get_empty_rooms'),
]