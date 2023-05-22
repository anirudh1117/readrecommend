from django.contrib import admin
from .models import BookImages, Books,  SubCategory, Categories


admin.site.register(SubCategory)
admin.site.register(Categories)
admin.site.register(Books)
admin.site.register(BookImages)

# admin.site.register(Rating)
