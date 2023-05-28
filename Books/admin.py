from django.contrib import admin
from .models import BookImages, Books,  SubCategory, Categories, Series
from Recommend.admin import RecommendationInline


admin.site.register(SubCategory)
admin.site.register(Categories)
admin.site.register(Series)

class BooksImagesInline(admin.TabularInline):
    model = BookImages

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    inlines = [BooksImagesInline, RecommendationInline]

