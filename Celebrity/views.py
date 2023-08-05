from django.shortcuts import render
from django.db.models import Count
from django.http import JsonResponse

from .models import Celebrity, Profession
from Recommend.models import Recommend
from utils.common_function import clean_description

# Create your views here.
def people(request):
    filter = request.GET.get('filter', None)
    if filter is None or len(filter) == 0:
        celebrity_ids = Recommend.objects.values_list("Celebrity_id").distinct()
        peoples = Celebrity.objects.filter(id__in =celebrity_ids).annotate(count=Count('celebritys'))
    else:
        peoples = Celebrity.objects.filter(professions__name_slug__iexact = filter).annotate(count=Count('celebritys'))
    profession_list = Profession.objects.all()
    keywords = 'book, recommendation, celebrity, author, amazon, best, world'
    for people in peoples:
        keywords = keywords + ', ' +  people.name + ', ' + people.name_slug
    for profession in profession_list:
        keywords = keywords + ', ' + profession.name
    
    data={
        "peoples":peoples,
        'professions' : profession_list,
        'keywords' : keywords
    }

    return render(request, 'people.html',data)

def peopleDetail(request,name):
    
   cs=Celebrity.objects.filter(name_slug__iexact=name)
   if cs.first():
       cs = cs[0]
   else:
       return render(request, 'peopleDetail.html',{})
       
#    cs_id= cs.values_list('pk', flat=True)[0]
   bookrecoms= Recommend.objects.filter(Celebrity=cs)
   description = "This page shows Books recommended by " + cs.name + " and books card contains images, description and Amazon link."

   keywords = 'book, recommendation, celebrity, author, amazon, best, world'
   keywords = keywords + ', ' +  cs.name + ', ' + cs.name_slug + ', ' + clean_description(cs.description)
   for profession in cs.professions.all():
        keywords = keywords + ', ' + profession.name
   for recom in bookrecoms:
       book  = recom.book
       keywords = keywords + ', ' + book.name + ', ' + book.name_slug + ', ' + book.author_name.name + ', ' + book.title + ', ' + clean_description(cs.description)
   data={
    "people":cs,
    "bookrecoms": bookrecoms,
    "keywords" : keywords,
    "description" : description
   }

   return render(request, 'peopleDetail.html',data)

def peopleSearch(request, name):
    data=Celebrity.objects.filter(name__icontains=name).values('name', 'name_slug')
    for celeb in data:
        print(celeb)
    response_data = [
        {'name': celeb.get('name'), 'name_slug' : celeb.get('name_slug') }
        for celeb in data
    ]
    return JsonResponse(response_data, safe=False)
