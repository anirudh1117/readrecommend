# Generated by Django 4.1.7 on 2023-06-17 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Celebrity', '0004_alter_socialplatform_name'),
        ('Books', '0007_remove_books_authorname_books_author_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='series',
            name='authorName',
        ),
        migrations.AddField(
            model_name='series',
            name='author_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Celebrity.celebrity'),
        ),
        migrations.AddField(
            model_name='series',
            name='sub_categories',
            field=models.ManyToManyField(blank=True, to='Books.subcategory'),
        ),
    ]
