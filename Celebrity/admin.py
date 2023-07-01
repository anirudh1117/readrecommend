from django.contrib import admin
from .models import Profession, SocialPlatform, Celebrity

@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']


class SocialPlatformInline(admin.TabularInline):
    model = SocialPlatform

@admin.register(Celebrity)
class CelebrityAdmin(admin.ModelAdmin):
    inlines = [SocialPlatformInline]
    search_fields = ['name']
    autocomplete_fields = ['professions']
    ordering = ['name']