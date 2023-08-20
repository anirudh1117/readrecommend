from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Count
from django.views.decorators.csrf import csrf_protect
from django.db.models.functions import Length
import wikipedia

from .models import SubCategory, Categories, Books, ContactForm
from Celebrity.models import Celebrity
from Recommend.models import Recommend
from utils.common_function import create_json_for_list_book, create_json_for_book_Detail, create_json_for_categories, get_categories_list, get_json_for_home
# # Create your views here.


def home(request):
    peoples = Celebrity.objects.annotate(
        count=Count('celebritys')).order_by('-count')[:4]
    categories = Categories.objects.annotate(book_count=Count('books')).values(
        'name', 'book_count', 'name_slug').order_by('-book_count')[:4]
    books = Books.objects.annotate(recommendation_count=Count(
        'books')).order_by('-recommendation_count')[:3]
    keywords = 'book, recommendation, celebrity, author, amazon, best, world, facebook, twitter, instagram'
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
        keywords = keywords + ', ' + people.name + ', ' + people.name_slug
    peoples = zip(peoples, platform)

    for book in books:
        keywords = keywords + ', ' + book.name + ', ' + book.name_slug

    for category in categories:
        keywords = keywords + ', ' + \
            category.get('name') + ', ' + category.get('name_slug')

    json_website = get_json_for_home()

    data = {
        "peoples": peoples,
        "categories": categories,
        "books": books,
        "platform": platform,
        "keywords": keywords,
        'jsonWebsite': json_website
    }
    return render(request, 'home.html', data)


def categories(request):
    categories = Categories.objects.annotate(book_count=Count('books')).values(
        'name', 'book_count', 'name_slug').order_by('-book_count')
    keywords = 'book, recommendation, celebrity, author, amazon, best, world, facebook, twitter, instagram'
    json = create_json_for_categories(categories)
    for category in categories:
        keywords = keywords + ', ' + \
            category.get('name') + ', ' + category.get('name_slug')
    data = {
        "categories": categories,
        "keywords": keywords,
        'jsonCategories': json
    }
    return render(request, 'categories.html', data)


def series(request):
    return render(request, 'series.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        contact = ContactForm.objects.create(
            name=name, email=email, subject=subject, message=message)
        if contact:
            data = {
                "submitted": "yes"
            }
            return render(request, 'contact.html', data)
    data = {
        "submitted": "no"
    }

    return render(request, 'contact.html', data)


def about(request):
    return render(request, 'about.html')


def search(request, keyword):
    keyword = keyword.replace("-", " ")
    celebrity_ids = Recommend.objects.values_list("Celebrity_id").distinct()
    peoples = Celebrity.objects.filter(
        id__in=celebrity_ids, name__icontains=keyword)
    people_count = len(peoples)

    author_ids = Books.objects.values_list("author_name_id").distinct()
    authors = Celebrity.objects.filter(
        id__in=author_ids, name__icontains=keyword)
    author_count = len(authors)

    books = Books.objects.filter(name__icontains=keyword)
    book_count = len(books)

    total = people_count + author_count + book_count
    data = {
        "keyword": keyword,
        "peoples": peoples,
        "people_count": people_count,
        "authors": authors,
        "author_count": author_count,
        "books": books,
        "book_count": book_count,
        "total": total
    }
    return render(request, 'search.html', data)

@csrf_protect
def globalSearch(request):
    url = '/search/'
    if request.method == 'POST':
        keyword = request.POST['keyword']
        keyword = keyword.replace(' ','-')
        url = url + keyword
    
    return redirect(url)


def get_sub_category(request, category_id):
    category_id = [] if category_id == "null" else category_id.split(",")
    subcategories = SubCategory.objects.filter(
        Category_id__in=category_id).distinct()
    response_data = [
        {'id': subcategory.id, 'name': subcategory.name}
        for subcategory in subcategories
    ]

    return JsonResponse(response_data, safe=False)


def books(request):
    categories = request.GET.get('categories', None)
    keyword = request.GET.get('keyword', None)
    books = Books.objects.annotate(count=Count('books')).order_by('-count')

    if categories is not None and len(categories) > 0:
        categories = get_categories_list(categories)
        books = books.filter(categories__name_slug__in=categories)
    if keyword is not None and len(keyword) > 0:
        books = books.filter(name__icontains=keyword)

    categories_list = Categories.objects.all().order_by(Length('name').asc())

    json_list = create_json_for_list_book(books)

    keywords = 'book, recommendation, celebrity, author, amazon, best, world'
    for book in books:
        keywords = keywords + ', ' + book.name + ', ' + book.name_slug

    for category in categories_list:
        keywords = keywords + ', ' + category.name + ', ' + category.name_slug

    data = {
        "books": books,
        'keywords': keywords,
        "categories": categories_list,
        'jsonList': json_list
    }

    return render(request, 'books.html', data)


@csrf_protect
def filterBooks(request):
    url = '/books?'
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
            url = url + '&categories='
            lenOfCategories = len(categories)
            for i in range(0, lenOfCategories):
                url = url + 'best-{0}-books'.format(categories[i])
                if i < (lenOfCategories - 1):
                    url = url + ','

    return redirect(url)


def bookDetail(request, name):

    book = Books.objects.filter(name_slug__iexact=name).annotate(
        count=Count('books')).order_by('-count')
    if book.first():
        book = book[0]
    else:
        return redirect("/books")
    recommend = Recommend.objects.filter(book=book)
    celeberity_ids = []
    for recom in recommend:
        celeberity_ids.append(recom.Celebrity_id)
    peoples = Celebrity.objects.annotate(
        count=Count('celebritys')).order_by('-count')
    peoples = peoples.filter(id__in=celeberity_ids)
    keywords = 'book, recommendation, celebrity, author, amazon, best, world, facebbok, twitter, instagram, '
    keywords = keywords + book.name + ', ' + book.name_slug
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
        keywords = keywords + ', ' + people.name + ', ' + people.name_slug

    json_detail = create_json_for_book_Detail(book, zip(peoples, platform))

    peoples = zip(peoples, platform)
    recomBooks = Books.objects.filter(
        categories__in=book.categories.all()).exclude(id=book.id)
    recomBooks = recomBooks.annotate(count=Count('books')).order_by('-count')
    recomBooks = recomBooks.filter(count__gt=0)
    if len(recomBooks) > 6:
        recomBooks = recomBooks[:6]
    description = "This page shows Book: " + book.name + \
        " , author and list of celebrities"
    for recomBook in recomBooks:
        keywords = keywords + ', ' + recomBook.name + ', ' + recomBook.name_slug

    data = {
        "book": book,
        "recomBooks": recomBooks,
        "keywords": keywords,
        "description": description,
        "wikipedia": wikipedia_page(book.name),
        "peoples": peoples,
        'jsonPeopleList': json_detail,
    }

    return render(request, 'booksDetail.html', data)


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
