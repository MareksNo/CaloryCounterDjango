from django.contrib import admin
from users import models


class ProfileAdmin(admin.ModelAdmin):

    list_select_related = True


admin.site.register(models.Plans)
admin.site.register(models.Profile, ProfileAdmin)
