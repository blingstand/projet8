# Generated by Django 3.0.3 on 2020-03-13 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200312_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='secret_answer',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='secret_question',
        ),
        migrations.AddField(
            model_name='profile',
            name='mail_confirm_sent',
            field=models.BooleanField(default=False),
        ),
    ]
