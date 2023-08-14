from django.contrib import admin
from .models import Lecture, LectureRoom, LectureTime

# Register your models here.
admin.site.register(Lecture)
admin.site.register(LectureRoom)
admin.site.register(LectureTime)