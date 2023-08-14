from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)
    user_pw = models.CharField(max_length=20)

    def __str__(self):
        return self.user_id