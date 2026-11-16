from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    external_reference = models.CharField(
        _("External reference"),
        max_length=255,
        unique=True,
    )
    stripe_customer_id = models.CharField(
        _("Stripe customer ID"),
        max_length=255,
        unique=True,
    )
    email = models.EmailField(
        _("Email address"),
        blank=True,
    )

    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.external_reference