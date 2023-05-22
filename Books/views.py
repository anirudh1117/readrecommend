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

def people(request):
    peoples = Celebrity.objects.all()

    data={
        "peoples":peoples,
    }
    print(data)
    return render(request, 'people.html',data)

def peopleDetail(request,name):
    
   cs=Celebrity.objects.filter(name=name)
#    cs_id= cs.values_list('pk', flat=True)[0]

   

   bookrecoms= Recommend.objects.filter(Celebrity=cs[0])
   print(bookrecoms)

   data={
    "cs":cs,
    "bookrecoms": bookrecoms
   }

   
  

   return render(request, 'peopleDetail.html',data)


def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def gift(request):
    return render(request, 'gift.html')



