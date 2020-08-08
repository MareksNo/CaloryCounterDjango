from django.contrib import admin
from users import models

admin.site.register(models.Plans)
admin.site.register(models.Profile)