from django.contrib.auth.models import User
from django.db import models

#!!!!! faire un makemigrations et migrate
# Create your models here.

class Profile(models.Model):
    def __str__(self):
        return self.user.username
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    """required pamameters for user : username, password
    > more info : 
    https://docs.djangoproject.com/en/3.0/ref/contrib/auth/#django.contrib.auth.models.User.is_authenticated
    """