# Generated by Django 3.0.3 on 2020-03-22 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_category_needed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='packaging',
            field=models.CharField(max_length=250),
        ),
    ]
