from django import urls
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from .sitempas import StaticSitemap, celebritySitemap, bookSitemap, authorSitemap

dynamic = {
    'celebrity': celebritySitemap,
    'book': bookSitemap,
}
sitemaps = {'static': StaticSitemap,
            'celebrity': celebritySitemap,
            'book': bookSitemap,
            'author': authorSitemap
        }
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Books.urls')),
    path('people/', include('Celebrity.urls')),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
