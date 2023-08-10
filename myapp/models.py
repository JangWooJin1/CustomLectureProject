from django.db import models
from django.db.models import UniqueConstraint

# Create your models here.
class Lecture(models.Model):
    lecture_id = models.IntegerField(primary_key=True)
    lecture_curriculum = models.CharField(max_length=10)
    lecture_classification = models.CharField(max_length=15, null=True, blank=True)
    lecture_code = models.CharField(max_length=8)
    lecture_number = models.CharField(max_length=5)
    lecture_name = models.CharField(max_length=100)
    lecture_professor = models.CharField(max_length=15, null=True, blank=True)
    lecture_campus = models.CharField(max_length=5, null=True, blank=True)
    lecture_credit = models.IntegerField()
    lecture_univ = models.CharField(max_length=15, null=True, blank=True)
    lecture_major = models.CharField(max_length=50, null=True, blank=True)
    lecture_remark = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['lecture_code', 'lecture_number'], name='unique_lecture')
        ]

    def __str__(self):
        return f"{self.lecture_code}-{self.lecture_number} - {self.lecture_name}"


class LectureRoom(models.Model):
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    lecture_room = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.lecture_id} - {self.lecture_room}"


class LectureTime(models.Model):
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    lecture_day = models.CharField(max_length=4, null=True, blank=True)
    lecture_start_time = models.FloatField(null=True, blank=True)
    lecture_end_time = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.lecture_id} - {self.lecture_day}"
