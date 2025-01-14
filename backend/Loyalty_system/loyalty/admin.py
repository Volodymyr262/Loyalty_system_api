from django.contrib import admin
from .models import LoyaltyTier

@admin.register(LoyaltyTier)
class LoyaltyTierAdmin(admin.ModelAdmin):
    list_display = ('tier_name', 'program', 'points_to_reach')
    list_filter = ('program',)
    search_fields = ('tier_name',)