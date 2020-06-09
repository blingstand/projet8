# Generated by Django 3.0.3 on 2020-06-09 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20200414_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='code',
            field=models.CharField(max_length=24, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='mail_confirm_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='mail_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]