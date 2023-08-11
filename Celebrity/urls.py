from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.people, name='people'),
    path ('<str:name>-recommended-books', views.peopleDetail, name='people-detail'),
    path ('search-celebrity/<str:name>', views.peopleSearch, name='people-search'),
    path('filter-celebrity', views.filterCelebrity, name="filter-celebrity"),
    path('author', views.author, name='author'),
    path('filter-author', views.filterAuthor, name="filter-author"),
    path ('<str:name>-written-books', views.authorDetail, name='author-detail'),
] 