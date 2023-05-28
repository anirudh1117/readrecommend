from django.contrib import admin
from .models import Profession, SocialPlatform, Celebrity

admin.site.register(Profession)

class SocialPlatformInline(admin.TabularInline):
    model = SocialPlatform

@admin.register(Celebrity)
class CelebrityAdmin(admin.ModelAdmin):
    inlines = [SocialPlatformInline]