from django.contrib.auth.models import User 
from django.db import models

from products.models import Product

class Profile(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    wait_confirmation = models.BooleanField(default=True)
    mail_confirmed = models.BooleanField(default=False)
    code = models.CharField(max_length=24, null=True)
    favlist = models.ManyToManyField(Product)

