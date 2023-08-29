from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(LectureGroup)
admin.site.register(LectureItem)
admin.site.register(LectureItemSchedule)
admin.site.register(UserBasket)