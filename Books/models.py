from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import os
from datetime import timezone
from utils.common_function import slugify

class SubCategory(models.Model):
    name = models.CharField(max_length=100,blank=False)
    name_slug = models.SlugField(blank=True, null=True, editable=False)

    def __str__(self):
        return f'{self.name}' 
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)

class Categories(models.Model):
    name = models.CharField(max_length=100,blank=False)
    SubCategories = models.ManyToManyField('SubCategory', blank=True)
    name_slug = models.SlugField(blank=True, null=True, editable=False)

    def __str__(self):
        return f'{self.name}' 
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)


class Series(models.Model):
    name = models.CharField(max_length=100,blank=False)
    name_slug = models.SlugField(blank=True, null=True, editable=False)
    title = models.CharField(max_length=256,blank=False)
    authorName = models.CharField(max_length=100,blank=False)
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField('Categories', blank=True)
    ISBN = models.CharField(max_length=100,blank=True)


    def __str__(self):
        return f'{self.name}' 
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)


class Books(models.Model):
    name = models.CharField(max_length=100,blank=False)
    name_slug = models.SlugField(blank=True, null=True, editable=False)
    title = models.CharField(max_length=256,blank=False)
    authorName = models.CharField(max_length=100,blank=False)
    description = models.TextField(null=True, blank=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True)
    categories = models.ManyToManyField('Categories', blank=True)
    ISBN = models.CharField(max_length=100,blank=True)
    amazonlink = models.URLField(default='https://amzn.to/3MquoAM')
    dateOfPublish = models.DateField(null=True)

    def __str__(self):
        return f'{self.name}' 
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)

 
def get_upload_path(instance, filename):
    field_value = instance.book.name
    # date_time = timezone.now().strftime('%Y/%m/%d')
    filename = os.path.basename(filename)
    return f'media/Books/{field_value}/{filename}'


class BookImages(models.Model):
    book = models.ForeignKey( "Books", on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_upload_path, blank=True)

# class Rating(models.Model):
#     name = models.CharField(max_length=100,blank=False)
#     rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
#     book = models.ForeignKey( "Books", on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.name}' 


