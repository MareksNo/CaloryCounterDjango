from django.conf import settings

from django.db import models
from django.utils import timezone


class Plans(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    c_goal = models.IntegerField(verbose_name='Calorie goal')
    c_current = models.IntegerField(default=0)
    goal_reached = models.BooleanField(default=False)

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def calories_status(self, calories_ct=None):
        self.c_current += calories_ct

        if self.c_current > self.c_goal:
            self.goal_reached = True
            self.save()
            return 1  # Calories exceeded
        elif self.c_current == self.c_goal:
            self.goal_reached = True
            self.save()
            return 0  # Calories reached

        self.save()
        return -1  # Not reached
