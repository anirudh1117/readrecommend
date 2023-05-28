from django.shortcuts import render
from .models import SubCategory, Categories,BookImages,Books
from Celebrity.models import Profession,SocialPlatform,Celebrity
from Recommend.models import Recommend
# # Create your views here.


def home(request):
    return render(request, 'home.html')


def categories(request):
    return render(request, 'categories.html')

def series(request):
    return render(request, 'series.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def gift(request):
    return render(request, 'gift.html')



