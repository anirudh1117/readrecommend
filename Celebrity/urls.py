from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.people, name='people'),
    path ('<str:name>', views.peopleDetail, name='people-detail'),
] 