from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categories', views.categories, name='categories'),
    path('series', views.series, name='series'),
    path('gift', views.gift, name='gift'),
    path('about', views.about, name='about'),
   
    path('contact', views.contact, name='contact'),
    path('api/subcategories/<str:category_id>', views.get_sub_category, name='subcategory_api'),
] 