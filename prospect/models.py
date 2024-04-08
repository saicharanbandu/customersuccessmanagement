from django.db import models
from misc import models as miscModels
from django.conf import settings

import uuid

from tabernacle_customer_success import constants

class Profile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    name = models.CharField(max_length=255, verbose_name="Prospect Name")
    address = models.CharField(max_length=255, null=True, verbose_name="Street/Locality")
    city = models.CharField(max_length=50, null=True, verbose_name="City/Town/Village")
    country = models.ForeignKey(
        miscModels.Country,
        to_field="uuid",
        on_delete=models.SET_NULL,
        null=True,
    )
    state = models.ForeignKey(
        miscModels.State, to_field="uuid", on_delete=models.SET_NULL, null=True
    )

    email = models.EmailField(
        max_length=255, blank=True, null=True, verbose_name="Email ID"
    )
    website = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Website"
    )
    denomination = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Denomination"
    )
    congregation = models.IntegerField(blank=True, null=True, verbose_name="Congregation Size (Approx)")
    
    remarks = models.TextField( blank=True, null=True, verbose_name="Remarks")

    status = models.CharField(max_length=55, choices=constants.PROSPECT_STATUS_CHOICES, null=True)

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='prospect_manager'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} : {self.city}"


class PointOfContact(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    prospect = models.ForeignKey(
        Profile,
        to_field="uuid",
        on_delete=models.CASCADE,
        related_name="prospect_poc",
        null=True,
    )
    name = models.CharField(max_length=255, verbose_name="Name",  blank=True)
    email = models.EmailField(max_length=255, verbose_name="Email ID", blank=True, null=True)
    mobile = models.CharField(max_length=10, verbose_name="Mobile Number", blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.prospect.name}"


class StatusHistory(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    prospect = models.ForeignKey(
        Profile,
        to_field="uuid",
        on_delete=models.CASCADE,
        related_name="prospect_history",
    )
    status = models.CharField(max_length=55, choices=constants.PROSPECT_STATUS_CHOICES)
    date = models.DateTimeField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.prospect} : {self.status}"