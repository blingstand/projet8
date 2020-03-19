from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    last_maj_0 = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def last_maj(self): 
        if self.last_maj_0 is not None:
            correct_form_last_maj = "{}-{}-{}".format(self.last_maj_0.day, self.last_maj_0.month, self.last_maj_0.year)
            return correct_form_last_maj
        print("Valeur nulle > Pensez à enregistrer")
        

class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    image_url = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    nutriscore = models.SmallIntegerField()
    packaging = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    last_maj = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def last_maj(self): 
        if self.last_maj_0 is not None:
            correct_form_last_maj = "{}-{}-{}".format(self.last_maj_0.day, self.last_maj_0.month, self.last_maj_0.year)
            return correct_form_last_maj
        print("Valeur nulle > Pensez à enregistrer")

    