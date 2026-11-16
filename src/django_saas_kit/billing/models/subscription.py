from django.db import models
from django.utils.translation import gettext_lazy as _

from billing.models.customer import Customer
from billing.models.price import Price


class Subscription(models.Model):

    class Status(models.TextChoices):
        INCOMPLETE = "incomplete", _("Incomplete")
        INCOMPLETE_EXPIRED = "incomplete_expired", _("Incomplete expired")
        TRIALING = "trialing", _("Trialing")
        ACTIVE = "active", _("Active")
        PAST_DUE = "past_due", _("Past due")
        CANCELED = "canceled", _("Canceled")
        UNPAID = "unpaid", _("Unpaid")
        PAUSED = "paused", _("Paused")

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="subscriptions",
        verbose_name=_("Customer"),
    )
    stripe_subscription_id = models.CharField(
        _("Stripe subscription ID"),
        max_length=255,
        unique=True,
    )

    status = models.CharField(
        _("Status"),
        max_length=30,
        choices=Status.choices,
        default=Status.INCOMPLETE,
    )

    current_period_start = models.DateTimeField(
        _("Current period start"),
        null=True,
        blank=True,
    )
    current_period_end = models.DateTimeField(
        _("Current period end"),
        null=True,
        blank=True,
    )

    cancel_at_period_end = models.BooleanField(
        _("Cancel at period end"),
        default=False,
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
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")

    def __str__(self):
        return self.stripe_subscription_id


class SubscriptionItem(models.Model):
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Subscription"),
    )
    price = models.ForeignKey(
        Price,
        on_delete=models.PROTECT,
        related_name="subscription_items",
        verbose_name=_("Price"),
    )
    quantity = models.PositiveIntegerField(
        _("Quantity"),
        default=1,
    )

    stripe_subscription_item_id = models.CharField(
        _("Stripe subscription item ID"),
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = _("Subscription item")
        verbose_name_plural = _("Subscription items")

    def __str__(self):
        return f"{self.subscription} - {self.price}"