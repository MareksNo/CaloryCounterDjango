from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    calories = models.IntegerField()

    def __str__(self):
        return self.name
