from django.urls import path
from django.contrib.auth import views as auth_views
from appsearch.views import Search, get_classification_options, get_univ_options, get_major_options, get_lecture, add_userbasket, delete_userbasket, get_lecture_group

app_name = 'search'

urlpatterns = [
    path('', Search.as_view(template_name='search/mainPage.html'), name='search'),
    path('get_classification_options/', get_classification_options, name='get_classification_options'),
    path('get_univ_options/', get_univ_options, name='get_univ_options'),
    path('get_major_options/', get_major_options, name='get_major_options'),
    path('get_lecture_group/', get_lecture_group, name='get_lecture_group'),
    path('get_lecture/', get_lecture, name='get_lecture'),
    path('add_userbasket/', add_userbasket, name='add_userbasket'),
    path('delete_userbasket/', delete_userbasket, name='delete_userbasket'),
]