from django.conf import settings

from django.db import models
from django.utils import timezone


class Plans(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    c_goal = models.IntegerField()
    c_current = models.IntegerField(default=0)

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
