from django.db import models
from misc import models as miscModels
import uuid


class ProspectInfo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    name = models.CharField(max_length=255, verbose_name="Name")
    street = models.CharField(max_length=255, verbose_name="Street/Locality")
    city = models.CharField(max_length=50, verbose_name="City/Town/Village")
    country = models.ForeignKey(
        miscModels.Country, to_field="uuid", on_delete=models.SET_NULL, null=True
    )
    state = models.ForeignKey(
        miscModels.State, to_field="uuid", on_delete=models.SET_NULL, null=True
    )
    email = models.EmailField(max_length=255, verbose_name="Email ID")
    website = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Website"
    )
    denomination = models.CharField(max_length=50, verbose_name="Denomination")
    congregation = models.IntegerField(verbose_name="Congregation Size (Approx)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PointOfContactInfo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    prospect = models.ForeignKey(
        ProspectInfo, to_field="uuid", on_delete=models.CASCADE, null=True
    )
    contact_name = models.CharField(max_length=255, verbose_name="Name")
    email = models.EmailField(max_length=255, verbose_name="Email ID")
    mobile = models.CharField(max_length=10, verbose_name="Mobile Number")
    remarks = models.CharField(max_length=1024, verbose_name="Remarks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pOC_name
