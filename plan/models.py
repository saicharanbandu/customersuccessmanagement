from django.db import models
from django.contrib.postgres.fields import ArrayField

import uuid

class AppModule(models.Model):
    """
    Tabernacle Modules
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=256)
    permissions = ArrayField(
        models.CharField(max_length=10), size=4, null=True, blank=True
    )
    precedance = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
    
    
class Tariff(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    modules = ArrayField(models.CharField(max_length=50), size=30, null=True)
    lower_limit = models.IntegerField()
    upper_limit = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
    


