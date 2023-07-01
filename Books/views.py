from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from .models import SubCategory, Categories,BookImages,Books
from Celebrity.models import Profession,SocialPlatform,Celebrity
from Recommend.models import Recommend
# # Create your views here.


def home(request):
    peoples = Celebrity.objects.annotate(count=Count('celebritys')).order_by('-count')[:4]
    data={
        "peoples":peoples,
    }
    print(peoples)
    return render(request, 'home.html', data)


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

def get_sub_category(request, category_id):
    category_id = [] if category_id == "null" else category_id.split(",")
    subcategories = SubCategory.objects.filter(Category_id__in=category_id).distinct()
    response_data = [
        {'id': subcategory.id, 'name': subcategory.name}
        for subcategory in subcategories
    ]

    return JsonResponse(response_data, safe=False)



