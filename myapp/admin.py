from django.contrib import admin
from .models import Lecture, LectureRoom, LectureTime, User, UserBasket

# Register your models here.
admin.site.register(User)
admin.site.register(Lecture)
admin.site.register(LectureRoom)
admin.site.register(LectureTime)
admin.site.register(UserBasket)