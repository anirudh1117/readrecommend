from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class SubCategory(models.Model):
    name = models.CharField(max_length=100,blank=False)

    def __str__(self):
        return f'{self.name}' 

class Categories(models.Model):
    name = models.CharField(max_length=100,blank=False)
    SubCategories = models.ManyToManyField('SubCategory')

    def __str__(self):
        return f'{self.name}' 

class Books(models.Model):
    name = models.CharField(max_length=100,blank=False)
    title = models.CharField(max_length=256,blank=False)
    authorName = models.CharField(max_length=100,blank=False)
    description = models.TextField()
    categories = models.ManyToManyField('Categories')
    ISBN = models.CharField(max_length=100,blank=True)
    amazonlink = models.URLField(default='https://amzn.to/3MquoAM')
    dateOfPublish = models.DateTimeField()

    def __str__(self):
        return f'{self.name}' 

 
def get_upload_path(instance, filename):
    field_value = instance.book.name
    date_time = timezone.now().strftime('%Y/%m/%d')
    filename = os.path.basename(filename)
    return f'{field_value}/{date_time}/{filename}'


class BookImages(models.Model):
    book = models.ForeignKey( "Books", on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_upload_path, blank=True)

# class Rating(models.Model):
#     name = models.CharField(max_length=100,blank=False)
#     rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
#     book = models.ForeignKey( "Books", on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.name}' 


