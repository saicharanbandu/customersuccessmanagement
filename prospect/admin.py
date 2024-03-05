from django.contrib import admin

from .import models
# Register your models here.

admin.site.register(models.ProspectInfo)
admin.site.register(models.PointOfContactInfo)