# Generated by Django 3.0.3 on 2020-03-19 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_category_last_maj'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='last_maj_0',
            field=models.DateField(auto_now=True),
        ),
    ]
