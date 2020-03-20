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
    nutriscore = models.CharField(max_length=2)
    packaging = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    last_maj_0 = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def last_maj(self): 
        if self.last_maj_0 is not None:
            correct_form_last_maj = "{}-{}-{}".format(self.last_maj_0.day, self.last_maj_0.month, self.last_maj_0.year)
            return correct_form_last_maj
        print("Valeur nulle > Pensez à enregistrer")

# prod1 = p(name="Pur jus d'orange sans pulpe", 
#     image_url="https://static.openfoodfacts.org/images/products/350/211/000/9449/front_fr.80.400.jpg",
#     url="https://world.openfoodfacts.org/product/3502110009449/pur-jus-d-orange-sans-pulpe-tropicana", 
#     nutriscore=3,
#     packaging=1,
#     category=cat)