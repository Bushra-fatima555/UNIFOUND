
from django.contrib import admin
from .models import Claim


@admin.action(description="Approve selected claims")
def approve_claims(modeladmin, request, queryset):
    queryset.update(status='Approved')


@admin.action(description="Reject selected claims")
def reject_claims(modeladmin, request, queryset):
    queryset.update(status='Rejected')


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):

    list_display = (
        'claimant_name',
        'item_name',
        'status',
        'created_at'
    )

    list_filter = ('status',)

    search_fields = (
        'claimant_name',
        'item_name'
    )

    actions = [
        approve_claims,
        reject_claims
    ]
