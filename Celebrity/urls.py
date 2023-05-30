from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.people, name='people'),
    path ('<str:name>-books', views.peopleDetail, name='people-detail'),
] 