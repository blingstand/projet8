from django.contrib.auth.models import User 
from django.db import models

from products.models import Product

class Profile(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    mail_confirm_sent = models.BooleanField(default=False)
    mail_confirmed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    favlist = models.ManyToManyField(Product)

