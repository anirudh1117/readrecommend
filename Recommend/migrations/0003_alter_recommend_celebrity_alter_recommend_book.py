# Generated by Django 4.1.7 on 2023-05-21 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Celebrity', '0001_initial'),
        ('Books', '0003_books_amazonlink_delete_affillatelink'),
        ('Recommend', '0002_remove_recommend_recommendeddate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommend',
            name='Celebrity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='celebritys', to='Celebrity.celebrity'),
        ),
        migrations.AlterField(
            model_name='recommend',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='Books.books'),
        ),
    ]
