from django.contrib import admin

from .import models as prospectModels
# Register your models here.

admin.site.register(prospectModels.Profile)
admin.site.register(prospectModels.PointOfContact)