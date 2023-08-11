from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.db.models import Count

from Celebrity.models import Celebrity
from Recommend.models import Recommend
from Books.models import Books

# sitemap class
class StaticSitemap(Sitemap):
    """Reverse 'static' views for XML sitemap."""
    changefreq = "daily"
    priority = 0.5
    protocol = 'https'

    def items(self):
        # Return list of url names for views to include in sitemap
        return ['home', 'people', 'author', 'books', 'categories']

    def location(self, item):
        return reverse(item)

class celebritySitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        celebrity_ids = Recommend.objects.values_list(
            "Celebrity_id").distinct()
        peoples = Celebrity.objects.filter(
            id__in=celebrity_ids).annotate(count=Count('celebritys'))
        return peoples
    
    def name(self, obj):
        return obj.name
    def slug_field(self, obj):
        return obj.name_slug
    def description(self, obj):
        return obj.description
    def professions(self,obj):
        profession = ",".join(str(msg.name) for msg in obj.professions.all())
        return profession
    def books_recommended(self, obj):
        books = ",".join(str(msg.name) for msg in Recommend.objects.filter(Celebrity=obj))
        return books
    def total_books_recommend(self,obj):
        return str(obj.count) + 'Recommended books'
    
class authorSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        celebrity_ids = Books.objects.values_list(
            "author_name_id").distinct()
        author = Celebrity.objects.filter(
            id__in=celebrity_ids)
        return author
    
    def name(self, obj):
        return obj.name
    def slug_field(self, obj):
        return obj.name_slug
    def description(self, obj):
        return obj.description
    def professions(self,obj):
        profession = ",".join(str(msg.name) for msg in obj.professions.all())
        return profession
    def location(self,obj):
        return '/people/%s-written-books' % (obj.name_slug)
    

class bookSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        books = Books.objects.all()
        return books
    
    def name(self, obj):
        return obj.name
    def slug_field(self, obj):
        return obj.name_slug
    def description(self, obj):
        return obj.description
    
