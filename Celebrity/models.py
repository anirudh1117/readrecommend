from django.db import models
from django.core.exceptions import ValidationError
from django.shortcuts import reverse
import os
from datetime import timezone

from utils.common_function import slugify

class Profession(models.Model):
    name = models.CharField(max_length=100,blank=False)
    name_slug = models.SlugField(blank=True, null=True, editable=False)

    def __str__(self):
        return f'{self.name}' 
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
            professionObj = Profession.objects.filter(name_slug=self.name_slug)
            if self.pk is None and professionObj.first():
                raise ValidationError({"detail" : "This Profession is already created"})
        super().save(*args, **kwargs)
    
    
def get_upload_path(instance, filename):
    field_value = instance.name
    
    filename = os.path.basename(filename)
    return f'media/Celebrity/{field_value}/{filename}'

class Celebrity(models.Model):
    name = models.CharField(max_length=100,blank=False, unique=True)
    name_slug = models.SlugField(blank=True, null=True, editable=False)
    description = models.TextField(blank=True, null=True)
    professions = models.ManyToManyField('Profession')
    image = models.FileField(upload_to=get_upload_path, blank=True)


    def __str__(self):
        return f'{self.name}' 
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        if self.pk is None and Celebrity.objects.filter(name_slug=self.name_slug).exists():
            raise ValidationError("Name must be unique (case-insensitive).")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        path = reverse('people-detail', args=[self.name_slug])
        return str(path)



PLATFORM_CHOICES = (
    ("INSTAGRAM", "INSTAGRAM"),
    ("TWITTER", "TWITTER"),
    ("FACEBOOK", "FACEBOOK"),
    ("LINKEDIN", "LINKEDIN")
)

class SocialPlatform(models.Model):
    Celebrity = models.ForeignKey( "Celebrity", on_delete=models.CASCADE)
    name = models.CharField(max_length=100,choices = PLATFORM_CHOICES)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}' 
    
