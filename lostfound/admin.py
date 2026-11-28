
from django.contrib import admin
from .models import Item, Claim


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        'item_name',
        'item_type',
        'category',
        'user',
        'status',
        'created_at',
    )

    search_fields = (
        'item_name',
        'description',
        'location',
        'user__username',
    )

    list_filter = (
        'item_type',
        'category',
        'status',
    )

    ordering = ('-created_at',)


Claim._meta.verbose_name = "Lost & Found Claim"
Claim._meta.verbose_name_plural = "Lost & Found Claims"


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):

    list_display = (
        'item',
        'claimant',
        'status',
        'created_at',
    )

    search_fields = (
        'item__item_name',
        'claimant__username',
        'claim_message',
    )

    list_filter = (
        'status',
        'created_at',
    )

    ordering = ('-created_at',)
