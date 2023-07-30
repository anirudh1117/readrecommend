from django.shortcuts import render
from django.db.models import Count
from django.http import JsonResponse

from .models import Celebrity, Profession
from Recommend.models import Recommend

# Create your views here.
def people(request):
    filter = request.GET.get('filter', None)
    if filter is None or len(filter) == 0:
        celebrity_ids = Recommend.objects.values_list("Celebrity_id").distinct()
        peoples = Celebrity.objects.filter(id__in =celebrity_ids).annotate(count=Count('celebritys'))
    else:
        peoples = Celebrity.objects.filter(professions__name_slug__iexact = filter).annotate(count=Count('celebritys'))
    profession_list = Profession.objects.all()
    data={
        "peoples":peoples,
        'professions' : profession_list,
    }
    return render(request, 'people.html',data)

def peopleDetail(request,name):
    
   cs=Celebrity.objects.filter(name_slug__iexact=name)
   if cs.first():
       cs = cs[0]
       
#    cs_id= cs.values_list('pk', flat=True)[0]
   bookrecoms= Recommend.objects.filter(Celebrity=cs)
   data={
    "people":cs,
    "bookrecoms": bookrecoms
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
