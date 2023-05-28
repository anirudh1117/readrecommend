from django.db import models

class Recommend(models.Model):
    book = models.ForeignKey( "Books.Books", on_delete=models.CASCADE,related_name='books')
    Celebrity = models.ForeignKey( "Celebrity.Celebrity",related_name='celebritys', on_delete=models.SET_NULL, null=True)
    celebrity_comment = models.TextField(null=True, blank=True)
 
   

    def __str__(self):
        return f'{self.book}' 
