from django.test import TestCase
from unittest import mock, skip

from products.models import Category, Product
print("test_product\n", "_ "*20)
@skip
class ProductsModels(TestCase):

    def test_model_cat_return(self): 

        category = Category(name='jus de fruits')
        category.save()
        self.assertTrue(category, 'jus de fruits')

    def test_model_prod_return(self): 

        self.product = Product(
            name="Pur jus d'orange sans pulpe", 
            image_url="https://static.openfoodfacts.org/images/products/350/211/000/9449/front_fr.80.400.jpg",
            url="https://world.openfoodfacts.org/product/3502110009449/pur-jus-d-orange-sans-pulpe-tropicana", 
            nutriscore="c", packaging="carton")
        self.product.save()
        self.assertTrue(self.product, "Pur jus d'orange sans pulpe")

    def test_model_prod_nutriscore_img(self):
        self.product = Product(
            name="Pur jus d'orange", 
            image_url="https://static.openfoodfacts.org/images/products/350/211/000/9449/front_fr.80.400.jpg",
            url="https://world.openfoodfacts.org/product/3502110009449/pur-jus-d-orange-sans-pulpe-tropicana", 
            nutriscore="c", packaging="carton")
        self.product.save()
        nutriscore = self.product.nutriscore_img
        self.assertTrue("C.png", nutriscore)