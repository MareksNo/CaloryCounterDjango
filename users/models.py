from django.conf import settings

from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save


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

    @classmethod
    def create_plan(cls, name, c_goal, user):
        plan = cls.objects.create(name=name, c_goal=c_goal, user=user)
        plan.save()

        return plan

class Profile(models.Model):
    MALE = 'm'
    FEMALE = 'f'

    BMR = 'BMR'
    SEDENTARY = 'Sedentary'
    LIGHT = 'Light'
    MODERATE = 'Moderate'
    VERY_ACTIVE = 'Very Active'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    ACTIVITY_CHOICES = [
        (BMR, 'BMR'),
        (SEDENTARY, 'Sedentary'),
        (LIGHT, 'Light'),
        (MODERATE, 'Moderate'),
        (VERY_ACTIVE, 'Very Active')
    ]
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    weight = models.DecimalField(verbose_name='Weight(lbs)', decimal_places=2, max_digits=6, default=154.32)
    height = models.DecimalField(verbose_name='Height(in)', decimal_places=2, max_digits=6, default=70.0)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    age = models.IntegerField(verbose_name='Age', default=18)
    activity = models.CharField(choices=ACTIVITY_CHOICES, max_length=11, default=BMR)

    def __str__(self):
        return f'{self.user}\'s profile'

# Create a RunPython thingy, to create all
# of the profile, then delete the receiver, split the form in 2 parts when creating a user
