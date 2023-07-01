from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from .models import BookImages, Books,  SubCategory, Categories, Series
from Recommend.admin import RecommendationInline

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

class SubCategoryInline(admin.TabularInline):
    model =  SubCategory

class BooksInline(admin.TabularInline):
    model = Books

class SeriesAdminForm(forms.ModelForm):
    books = forms.ModelChoiceField(
        queryset=Books.objects.all(),
        widget=AutocompleteSelect(Books.series.field.remote_field, admin.site)
    )

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']
    autocomplete_fields = ['author_name', 'categories']
    form = SeriesAdminForm

    class Media:
        js = ('admin/js/adminCategories.js',)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    search_fields = ['name']
    ordering = ['name']

class BooksImagesInline(admin.TabularInline):
    model = BookImages


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    inlines = [BooksImagesInline, RecommendationInline]
    autocomplete_fields = ['series', 'author_name', 'categories','sub_categories']

    class Media:
        js = ('admin/js/adminCategories.js',)