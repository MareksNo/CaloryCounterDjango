from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Food(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    calories = models.IntegerField()

    def __str__(self):
        return self.name