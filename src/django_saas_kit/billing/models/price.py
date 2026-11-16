from django.db import models
from django.utils.translation import gettext_lazy as _


class Price(models.Model):

    class Interval(models.TextChoices):
        DAY = "day", _("Day")
        WEEK = "week", _("Week")
        MONTH = "month", _("Month")
        YEAR = "year", _("Year")

    product_reference = models.CharField(
        _("Product reference"),
        max_length=255,
    )
    stripe_product_id = models.CharField(
        _("Stripe product ID"),
        max_length=255,
    )
    stripe_price_id = models.CharField(
        _("Stripe price ID"),
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )

    unit_amount = models.PositiveBigIntegerField(
        _("Unit amount"),
    )
    currency = models.CharField(
        _("Currency"),
        max_length=3,
        default="eur",
    )

    interval = models.CharField(
        _("Billing interval"),
        max_length=10,
        choices=Interval.choices,
    )
    interval_count = models.PositiveIntegerField(
        _("Interval count"),
        default=1,
    )

    active = models.BooleanField(
        _("Active"),
        default=True,
    )

    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("Price")
        verbose_name_plural = _("Prices")

    def __str__(self):
        return (
            f"{self.product_reference} - "
            f"{self.unit_amount} {self.currency.upper()}"
        )