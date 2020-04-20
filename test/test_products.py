from django.test import TestCase
from django.urls import reverse

from unittest import mock, skip
from products.models import Category, Product

print("test_product\n", "_ "*20)
@skip
class ProductsModelsTest(TestCase):

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

    def test_model_prod_nutriscore_big_img(self):
        self.product = Product(
            name="Pur jus d'orange", 
            image_url="https://static.openfoodfacts.org/images/products/350/211/000/9449/front_fr.80.400.jpg",
            url="https://world.openfoodfacts.org/product/3502110009449/pur-jus-d-orange-sans-pulpe-tropicana", 
            nutriscore="c", packaging="carton")
        self.product.save()
        nutriscore = self.product.nutriscore_big_img
        self.assertTrue("nutriscore_C.png", nutriscore)

class ProductViewsTest(TestCase):

    def setUp(self):
        """datas call before each funtion"""
        #a cat
        self.category = Category(name="jus de fruits")
        self.category.save()
        #a product
        self.product1 = Product(
            name="Pur jus d'orange sans pulpe", 
            image_url="https://static.openfoodfacts.org/images/products/350/211/000/9449/front_fr.80.400.jpg",
            url="https://world.openfoodfacts.org/product/3502110009449/pur-jus-d-orange-sans-pulpe-tropicana", 
            nutriscore=3, packaging="carton")
        self.product1.save()

    def test_redirect_when_no_prod(self):
        """ tests whether access is possible when user is authenticated"""
        response = self.client.get(reverse("products:infos"), follow=True)
        print(response.wsgi_request.build_absolute_uri())
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('research:index'))

    def test_display_page_when_prod_arg(self):
        """ tests whether access is possible when user is authenticated"""
        response = self.client.get("/products/infos/Pur jus d'orange sans pulpe")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Repère nutritionnel pour 100g")