from django.db import models

class Recommend(models.Model):
    book = models.ForeignKey( "Books.Books", on_delete=models.CASCADE,related_name='books')
    Celebrity = models.ManyToManyField( "Celebrity.Celebrity",related_name='celebritys')
    celebrityComment = models.TextField(null=True, blank=True)
 
   

    def __str__(self):
        return f'{self.book}' 
