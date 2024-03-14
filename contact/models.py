from django.db import models


class Contact(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
