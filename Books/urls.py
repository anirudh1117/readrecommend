from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books-categories', views.categories, name='categories'),
    path('series', views.series, name='series'),
    path('gift', views.gift, name='gift'),
    path('about', views.about, name='about'),
   
    path('contact-us', views.contact, name='contact'),
    path('api/subcategories/<str:category_id>', views.get_sub_category, name='subcategory_api'),
    path('filter-books', views.filterBooks, name="filter-books"),
    path('books', views.books, name='books'),
    path('books/<str:name>', views.bookDetail, name='book-detail'),
] 