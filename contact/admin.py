from django.contrib import admin
from . import models as contactModels
# Register your models here.
admin.site.register(contactModels.Contact)