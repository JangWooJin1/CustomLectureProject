from django.db import models
from django.db.models import UniqueConstraint
from appsearch.models import LectureItem
from appaccount.models import User
# Create your models here.

class MyTimeTable(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture_id = models.ForeignKey(LectureItem, on_delete=models.CASCADE)
    class_num = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user_id', 'lecture_id', 'class_num'], name='unique_time_table')
        ]

    def __str__(self):
        return f'{self.user_id} - {self.lecture_id} - {self.class_num}'