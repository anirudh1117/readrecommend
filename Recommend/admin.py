from django.contrib import admin
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.forms import inlineformset_factory
from django.db import models

from .models import Recommend
from Books.models import Books


class RecommendationFormSet(inlineformset_factory(Books, Recommend, fields=('Celebrity', 'celebrity_comment'), extra=1)):
    pass


class RecommendationInline(admin.TabularInline):
    model = Recommend
    formset = RecommendationFormSet
    extra = 1
