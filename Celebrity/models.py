from django.db import models
from django.core.exceptions import ValidationError
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
            if professionObj.first():
                raise ValidationError({"detail" : "This Profession is already created"})
        super().save(*args, **kwargs)
    
    
def get_upload_path(instance, filename):
    field_value = instance.name
    date_time = timezone.now().strftime('%Y/%m/%d')
    filename = os.path.basename(filename)
    return f'Celebrity/{field_value}/{date_time}/{filename}'

class Celebrity(models.Model):
    name = models.CharField(max_length=100,blank=False)
    name_slug = models.SlugField(blank=True, null=True, editable=False)
    description = models.TextField(blank=True, null=True)
    professions = models.ManyToManyField('Profession')
    image = models.FileField(upload_to=get_upload_path, blank=True)


    def __str__(self):
        return f'{self.name}' 
    
    def save(self, *args, **kwargs):
        if self.name:
            self.name_slug = slugify(self.name.upper())
        super().save(*args, **kwargs)



PLATFORM_CHOICES = (
    ("INSTAGRAM", "INSTAGRAM"),
    ("TWITTER", "TWITTER"),
    ("FACEBOOK", "FACEBOOK"),
)

class SocialPlatform(models.Model):
    Celebrity = models.ForeignKey( "Celebrity", on_delete=models.CASCADE)
    name = models.CharField(max_length=100,choices = PLATFORM_CHOICES)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}' 
    
