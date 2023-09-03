from django.db import models
from django.shortcuts import reverse
import os
from django.core.exceptions import ValidationError
from utils.common_function import slugify
from Celebrity.models import Celebrity

class Categories(models.Model):
    name = models.CharField(max_length=100,blank=False)
    name_slug = models.SlugField(blank=True, null=True, editable=False)

    def __str__(self):
        return f'{self.name}' 
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        if self.pk is None and Categories.objects.filter(name_slug=self.name_slug).exists():
            raise ValidationError("Name must be unique (case-insensitive).")
        super().save(*args, **kwargs)

class SubCategory(models.Model):
    name = models.CharField(max_length=100,blank=False)
    name_slug = models.SlugField(blank=True, null=True, editable=False)
    Category = models.ForeignKey(Categories, blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.name}' 
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)

def get_upload_series_path(instance, filename):
    field_value = instance.name
    # date_time = timezone.now().strftime('%Y/%m/%d')
    filename = os.path.basename(filename)
    return f'media/Series/{field_value}/{filename}'

class Series(models.Model):
    name = models.CharField(max_length=100,blank=True)
    name_slug = models.SlugField(blank=True, null=True, editable=False)
    title = models.CharField(max_length=256,blank=True)
    author_name = models.ForeignKey(Celebrity, null=True, on_delete=models.DO_NOTHING)
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField('Categories', blank=True)
    sub_categories = models.ManyToManyField('SubCategory', blank=True)
    ISBN = models.CharField(max_length=100,blank=True)
    image = models.FileField(upload_to=get_upload_series_path, blank=True)


    def __str__(self):
        return f'{self.name}' 
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        if self.pk is None and Series.objects.filter(name_slug=self.name_slug).exists():
            raise ValidationError("Name must be unique (case-insensitive).")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        path = reverse('series-detail', args=[self.name_slug])
        return str(path)


class Books(models.Model):
    name = models.CharField(max_length=100,blank=False)
    name_slug = models.SlugField(blank=True, null=True, editable=False)
    title = models.CharField(max_length=256,blank=False)
    author_name = models.ForeignKey(Celebrity, null=True, on_delete=models.DO_NOTHING)
    description = models.TextField(null=True, blank=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True)
    categories = models.ManyToManyField('Categories', blank=True)
    sub_categories = models.ManyToManyField('SubCategory', blank=True)
    ISBN = models.CharField(max_length=100,blank=True)
    amazonlink = models.URLField(default='https://amzn.to/3MquoAM')
    dateOfPublish = models.DateField(null=True)

    def __str__(self):
        return f'{self.name}' 
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        if self.pk is None and Books.objects.filter(name_slug=self.name_slug).exists():
            raise ValidationError("Name must be unique (case-insensitive).")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        path = reverse('book-detail', args=[self.name_slug])
        return str(path)

 
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


class ContactForm(models.Model):
    name = models.CharField(max_length=100,blank=False)
    email = models.CharField(max_length=100,blank=False)
    subject = models.CharField(max_length=100,blank=False)
    message = models.TextField(max_length=500,blank=False)

    def __str__(self):
        return f'{self.name}' 


