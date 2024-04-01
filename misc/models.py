from django.db import models
import uuid


class Country(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'country'
        verbose_name_plural = 'countries'
        ordering = ('name',)

class State(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    country = models.ForeignKey(Country, to_field='uuid', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'state'
        verbose_name_plural = 'states'
        ordering = ('name',)
