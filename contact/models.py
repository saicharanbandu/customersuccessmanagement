from django.db import models
from django.conf import settings

import uuid

class Contact(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=55)
    profile_picture = models.ImageField(
        upload_to="profile_pictures", null=True, blank=True
    )
    designation = models.CharField(max_length=55, null=True, blank=True)
    organization = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    alt_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='contact_created_by'
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='contact_updated_by'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
