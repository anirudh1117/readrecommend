from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models.functions import Length
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import wikipedia

from .models import Celebrity, Profession
from Books.models import Books
from Recommend.models import Recommend
from utils.common_function import clean_description


def people(request):
    professions = request.GET.get('professions', None)
    keyword = request.GET.get('keyword', None)
    celebrity_ids = Recommend.objects.values_list("Celebrity_id").distinct()
    peoples = Celebrity.objects.filter(id__in=celebrity_ids)
    if professions is not None and len(professions) > 0:
        professions = professions.split(",")
        peoples = peoples.filter(professions__name_slug__in=professions)
    if keyword is not None and len(keyword) > 0:
        peoples = peoples.filter(name__icontains=keyword)
    peoples = peoples.annotate(count=Count('celebritys'))
    profession_list = Profession.objects.all().order_by(Length('name').asc())

    keywords = 'book, recommendation, celebrity, author, amazon, best, world, facebook, instagram, twitter'
    for people in peoples:
        keywords = keywords + ', ' + people.name + ', ' + people.name_slug
    for profession in profession_list:
        keywords = keywords + ', ' + profession.name

    platform = []
    for people in peoples:
        social = ['#', '#', '#']
        for socialplatform in people.socialplatform_set.all():
            if socialplatform.name == "FACEBOOK":
                social[0] = socialplatform.link
            elif socialplatform.name == "TWITTER":
                social[1] = socialplatform.link
            elif socialplatform.name == "INSTAGRAM":
                social[2] = socialplatform.link
        platform.append(social)
    peoples = zip(peoples, platform)

    data = {
        "peoples": peoples,
        'professions': profession_list,
        'keywords': keywords
    }

    return render(request, 'people.html', data)


def peopleDetail(request, name):

    cs = Celebrity.objects.filter(name_slug__iexact=name)
    if cs.first():
        cs = cs[0]
    else:
        return render(request, 'peopleDetail.html', {})

#    cs_id= cs.values_list('pk', flat=True)[0]
    platform = ['#', '#', '#']
    for socialplatform in cs.socialplatform_set.all():
        if socialplatform.name == "FACEBOOK":
            platform[0] = socialplatform.link
        elif socialplatform.name == "TWITTER":
            platform[1] = socialplatform.link
        elif socialplatform.name == "INSTAGRAM":
            platform[2] = socialplatform.link
    bookrecoms = Recommend.objects.filter(Celebrity=cs)
    books_id = []
    for recom in bookrecoms:
        books_id.append(recom.book_id)
    books = Books.objects.annotate(count=Count('books')).order_by('-count')
    books = books.filter(id__in=books_id)
    recommended_celebrity = Celebrity.objects.filter(professions__in=cs.professions.all()).exclude(
        name_slug__iexact=cs.name_slug).annotate(count=Count('celebritys')).order_by('-count')
    recommended_celebrity = recommended_celebrity.filter(count__gt=0)
    if len(recommended_celebrity) > 6:
        recommended_celebrity = recommended_celebrity[:6]
    description = "This page shows Books recommended by " + cs.name + \
        " and books card contains images, description and Amazon link."

    keywords = 'book, recommendation, celebrity, author, amazon, best, world, facebook, instagram, twitter'
    keywords = keywords + ', ' + cs.name + ', ' + \
        cs.name_slug + ', ' + clean_description(cs.description)
    for profession in cs.professions.all():
        keywords = keywords + ', ' + profession.name
    for recom in bookrecoms:
        book = recom.book
        keywords = keywords + ', ' + book.name + ', ' + book.name_slug + ', ' + \
            book.author_name.name + ', ' + book.title + \
            ', ' + clean_description(cs.description)
    data = {
        "people": cs,
        "bookrecoms": bookrecoms,
        "books": books,
        "keywords": keywords,
        "description": description,
        "platform": platform,
        "wikipedia": wikipedia_page(cs.name),
        "recommendedCelebrity": recommended_celebrity
    }

    return render(request, 'peopleDetail.html', data)


def wikipedia_page(celebrity_name):
    try:
        page = wikipedia.page(celebrity_name, auto_suggest=False)
        if page:
            wikipedia_url = page.url
            return wikipedia_url
        else:
            return "#"
    except:
        return "/"


def peopleSearch(request, name):
    data = Celebrity.objects.filter(
        name__icontains=name).values('name', 'name_slug')
    response_data = [
        {'name': celeb.get('name'), 'name_slug': celeb.get('name_slug')}
        for celeb in data
    ]
    return JsonResponse(response_data, safe=False)


@csrf_protect
def filterCelebrity(request):
    url = '/people?'
    if request.method == 'POST':
        keyword = ''
        categories = []
        for key in request.POST:
            if key == 'keyword':
                keyword = 'keyword=' + request.POST[key]
            elif key != 'csrfmiddlewaretoken':
                categories.append(key)
        if len(keyword) > 0:
            url = url + keyword
        if len(categories) > 0:
            url = url + '&professions=' + ','.join(categories)

    return redirect(url)


def author(request):
    professions = request.GET.get('professions', None)
    keyword = request.GET.get('keyword', None)

    author_ids = Books.objects.values_list("author_name_id").distinct()
    peoples = Celebrity.objects.filter(id__in=author_ids)
    if professions is not None and len(professions) > 0:
        professions = professions.split(",")
        peoples = peoples.filter(professions__name_slug__in=professions)
    if keyword is not None and len(keyword) > 0:
        peoples = peoples.filter(name_slug__icontains=keyword)
    peoples = peoples.annotate(count=Count('books')).order_by('-count')
    profession_list = Profession.objects.all().order_by(Length('name').asc())

    keywords = 'book, recommendation, celebrity, author, amazon, best, world,facebook, instagram, twitter'
    for people in peoples:
        keywords = keywords + ', ' + people.name + ', ' + people.name_slug
    for profession in profession_list:
        keywords = keywords + ', ' + profession.name

    platform = []
    for people in peoples:
        social = ['#', '#', '#']
        for socialplatform in people.socialplatform_set.all():
            if socialplatform.name == "FACEBOOK":
                social[0] = socialplatform.link
            elif socialplatform.name == "TWITTER":
                social[1] = socialplatform.link
            elif socialplatform.name == "INSTAGRAM":
                social[2] = socialplatform.link
        platform.append(social)
    peoples = zip(peoples, platform)

    data = {
        "peoples": peoples,
        'professions': profession_list,
        'keywords': keywords
    }

    return render(request, 'author.html', data)


def authorDetail(request, name):

    cs = Celebrity.objects.filter(name_slug__iexact=name)
    if cs.first():
        cs = cs[0]
    else:
        return render(request, 'peopleDetail.html', {})

#    cs_id= cs.values_list('pk', flat=True)[0]
    platform = ['#', '#', '#']
    for socialplatform in cs.socialplatform_set.all():
        if socialplatform.name == "FACEBOOK":
            platform[0] = socialplatform.link
        elif socialplatform.name == "TWITTER":
            platform[1] = socialplatform.link
        elif socialplatform.name == "INSTAGRAM":
            platform[2] = socialplatform.link
    books = Books.objects.annotate(count=Count('books')).order_by('-count')
    books = books.filter(author_name=cs)
    recommended_celebrity = Celebrity.objects.filter(professions__in=cs.professions.all()).exclude(
        name_slug__iexact=cs.name_slug).annotate(count=Count('books')).order_by('-count')
    recommended_celebrity = recommended_celebrity.filter(count__gt=0)
    if len(recommended_celebrity) > 6:
        recommended_celebrity = recommended_celebrity[:6]
    description = "This page shows Books written by " + cs.name + \
        " and books card contains images, description and Amazon link."

    keywords = 'book, recommendation, celebrity, author, amazon, best, world,facebook, instagram, twitter'
    keywords = keywords + ', ' + cs.name + ', ' + \
        cs.name_slug + ', ' + clean_description(cs.description)
    for profession in cs.professions.all():
        keywords = keywords + ', ' + profession.name
    for book in books:
        keywords = keywords + ', ' + book.name + ', ' + book.name_slug + ', ' + \
            book.author_name.name + ', ' + book.title + \
            ', ' + clean_description(cs.description)
    data = {
        "people": cs,
        "books": books,
        "keywords": keywords,
        "description": description,
        "platform": platform,
        "wikipedia": wikipedia_page(cs.name),
        "recommendedCelebrity": recommended_celebrity
    }

    return render(request, 'authorDetail.html', data)


@csrf_protect
def filterAuthor(request):
    url = '/people/author?'
    if request.method == 'POST':
        keyword = ''
        categories = []
        for key in request.POST:
            if key == 'keyword':
                keyword = 'keyword=' + request.POST[key]
            elif key != 'csrfmiddlewaretoken':
                categories.append(key)
        if len(keyword) > 0:
            url = url + keyword
        if len(categories) > 0:
            url = url + '&professions=' + ','.join(categories)

    return redirect(url)
