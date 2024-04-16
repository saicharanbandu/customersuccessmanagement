from django.contrib import admin
from .import models as prospectModels

admin.site.register(prospectModels.Profile)
admin.site.register(prospectModels.PointOfContact)