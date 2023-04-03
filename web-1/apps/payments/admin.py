from apps.payments.models import Plan, Price
from django.contrib import admin


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    """Price model admin."""

    list_display = ['id', 'stripe_id', 'currency', 'amount']
    readonly_fields = ['stripe_id']
    search_fields = ['currency']
    list_filter = ['currency']


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """Plan model admin."""

    list_display = [
        'stripe_id', 'name',
        'interval', 'description',
        'price'
    ]
    readonly_fields = ['stripe_id', 'product_id']
    search_fields = ['name']
    list_filter = ['interval']
