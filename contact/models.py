from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=55)
    profile_picture = models.ImageField(upload_to='contact/profile_pictures',blank=True)
    designation = models.CharField(max_length=55)
    organization = models.CharField(max_length=55)
    mobile_number = models.BigIntegerField()
    alt_number = models.BigIntegerField()
    email_id = models.EmailField()
    address = models.CharField(max_length=255)
    

    def __str__(self):
        return self.name
