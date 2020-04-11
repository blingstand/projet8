from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    needed = models.SmallIntegerField(default=0, choices=[(0,0), (1,1)])

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    image_url = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=2)
    packaging = models.CharField(max_length=250)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    @property
    def nutriscore_img(self):
        nutriscore_img = f"{self.nutriscore.upper()}.png"
        return nutriscore_img

# prod1 = p(name="Pur jus d'orange sans pulpe", 
#     image_url="https://static.openfoodfacts.org/images/products/350/211/000/9449/front_fr.80.400.jpg",
#     url="https://world.openfoodfacts.org/product/3502110009449/pur-jus-d-orange-sans-pulpe-tropicana", 
#     nutriscore=3,
#     packaging=1,
#     category=cat)