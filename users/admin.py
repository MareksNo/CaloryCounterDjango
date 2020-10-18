from django.contrib import admin

from django.core.cache import cache

from users import models

class ProfileAdmin(admin.ModelAdmin):

    list_select_related = True

class PlanAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        cache.delete(f'plans{request.user}')
        return super().save_model(request, obj, form, change)


admin.site.register(models.Plans, PlanAdmin)
admin.site.register(models.Profile, ProfileAdmin)
