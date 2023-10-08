from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/<str:keyword>', views.search, name='search'),
    path('global-search', views.globalSearch, name='global-search'),
    path('books-categories', views.categories, name='categories'),
    path('series/', views.series, name='series'),
    path('filter-series', views.filterSeries, name="filter-series"),
    path('series/<str:name>-books-in-order', views.seriesDetail, name='series-detail'),
    path('about', views.about, name='about'),
    path('privacy-policy', views.privacyPolicy, name='privacy-policy'),
   
    path('contact-us', views.contact, name='contact'),
    path('api/subcategories/<str:category_id>', views.get_sub_category, name='subcategory_api'),
    path('filter-books', views.filterBooks, name="filter-books"),
    path('books', views.books, name='books'),
    path('books/<str:name>', views.bookDetail, name='book-detail'),
] 