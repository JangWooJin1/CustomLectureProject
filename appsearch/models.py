from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User
# Create your models here.

class LectureGroup(models.Model):
    lecture_code = models.CharField(primary_key=True, max_length=8)
    lecture_curriculum = models.CharField(max_length=10)
    lecture_classification = models.CharField(max_length=15, null=True, blank=True)
    lecture_name = models.CharField(max_length=100)
    lecture_credit = models.IntegerField()
    lecture_univ = models.CharField(max_length=15, null=True, blank=True)
    lecture_major = models.CharField(max_length=50, null=True, blank=True)



class LectureItem(models.Model):
    lecture_id = models.IntegerField(primary_key=True)
    lecture_code = models.ForeignKey(LectureGroup, on_delete=models.CASCADE)
    lecture_number = models.CharField(max_length=5)
    lecture_professor = models.CharField(max_length=15, null=True, blank=True)
    lecture_campus = models.CharField(max_length=5, null=True, blank=True)
    lecture_remark = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['lecture_code', 'lecture_number'], name='unique_lecture')
        ]

    def __str__(self):
        return f"{self.lecture_code}-{self.lecture_number} - {self.lecture_name}"


class LectureItemSchedule(models.Model):
    lecture_id = models.ForeignKey(LectureItem, on_delete=models.CASCADE)
    lecture_room = models.CharField(max_length=50, null=True, blank=True)
    lecture_day = models.CharField(max_length=4, null=True, blank=True)
    lecture_start_time = models.FloatField(null=True, blank=True)
    lecture_end_time = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.lecture_id}-{self.lecture_room}-{self.lecture_day}"


class UserBasket(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture_id = models.ForeignKey(LectureItem, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user_id', 'lecture_id'], name='unique_basket')
        ]

    def __str__(self):
        return f'{self.user_id} - {self.lecture_id}'

