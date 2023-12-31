from django.urls import path
from django.contrib.auth import views as auth_views
from appsearch.views import *

app_name = 'search'

urlpatterns = [
    path('', Search.as_view(template_name='search/mainPage.html'), name='search'),
    path('get_classification_options/', get_classification_options, name='get_classification_options'),
    path('get_univ_options/', get_univ_options, name='get_univ_options'),
    path('get_major_options/', get_major_options, name='get_major_options'),
    path('get_lecture_group/', get_lecture_group, name='get_lecture_group'),
    path('get_lecture_item/', get_lecture_item, name='get_lecture_item'),
    path('add_userbasket/', add_userbasket, name='add_userbasket'),
    path('delete_userbasket/', delete_userbasket, name='delete_userbasket'),
    path('get_userbasket_items/', get_userbasket_items, name='get_userbasket_items'),
]