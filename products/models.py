from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Food(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    calories = models.IntegerField()

    def __str__(self):
        return self.name


class ProductViewCache(models.Model):
    cache_key = models.CharField(max_length=70)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    view_name = models.TextField()

    def __str__(self):
        return self.cache_key
