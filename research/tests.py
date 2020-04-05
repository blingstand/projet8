from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.test import TestCase
from django.urls import reverse

from unittest import mock, skip

from .form import SearchForm, AdvancedSearchForm
from .views import IndexView

from products.models import Category, Product


class IndexViewTests(TestCase):
    
    def setUp(self):
        patcher = mock.patch("research.views.SearchForm")
        self.addCleanup(patcher.stop)
        mock_form_class = patcher.start()
        self.mock_form = mock_form_class.return_value
        # a category 
        self.category = Category(name="jus de fruits")
        self.category.save()
        self.product1 = Product(
            name="Pur jus d'orange sans pulpe", 
            image_url="https://static.openfoodfacts.org/images/products/350/211/000/9449/front_fr.80.400.jpg",
            url="https://world.openfoodfacts.org/product/3502110009449/pur-jus-d-orange-sans-pulpe-tropicana", 
            nutriscore=3, packaging="carton")
        self.product2 = Product(
            name="Jus d'orange pas bon pas bio pas cher", 
            image_url="fake url",
            url="fake url", 
            nutriscore=5, packaging="bouteille plastique")
        self.product1.save()
        self.product2.save()
        self.product1.category.add(self.category)
        self.product2.category.add(self.category)
        self.product1.save()
        self.product2.save()

    def tearDown(self):
        self.category.delete()
        self.product1.delete()
        self.product2.delete()

    def test_get_access_page(self):
        """ user can access page index """
        response = self.client.get('http://127.0.0.1:8000/index')
        self.assertEqual(response.status_code, 200)
        
    def test_index_post_form_is_not_valid(self):
        """
            user gets an error page if form is not valid 
        """
        self.mock_form.is_valid.return_value = False
        response = self.client.post(reverse("research:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Problème dans le formulaire")

    def test_index_post_find_result(self):
        """ user can fill the input and server can get the input  value """
        self.mock_form.is_valid.return_value = True
        self.mock_form.cleaned_data = {"simple_search" : "Pur jus d'orange sans pulpe"}
        response = self.client.post(reverse("research:index"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vous pouvez remplacer cet aliment par ... ! ")


    def test_index_post_do_not_find_result(self):
        """ user can fill the input and server can get the input  value """
        self.mock_form.is_valid.return_value = True
        self.mock_form.cleaned_data = {"simple_search" : "123"}
        response = self.client.post(reverse("research:index"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pas de résultats dans la base actuellement")

    def test_index_post_no_result_but_category(self):
        """ user can fill the input and server can get the input  value """
        self.mock_form.is_valid.return_value = True
        self.mock_form.cleaned_data = {"simple_search" : "pas sans pulpe"}
        response = self.client.post(reverse("research:index"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pas de résultats parfaitement identiques ")

class ResultsViewTests(TestCase):

    def setUp(self):
        patcher = mock.patch("research.views.SearchForm")
        self.addCleanup(patcher.stop)
        mock_form_class = patcher.start()
        self.mock_form = mock_form_class.return_value
        # a category 
        self.category = Category(name="jus de fruits")
        self.category.save()
        self.product1 = Product(
            name="Pur jus d'orange sans pulpe", 
            image_url="https://static.openfoodfacts.org/images/products/350/211/000/9449/front_fr.80.400.jpg",
            url="https://world.openfoodfacts.org/product/3502110009449/pur-jus-d-orange-sans-pulpe-tropicana", 
            nutriscore=3, packaging="carton")
        self.product2 = Product(
            name="Jus d'orange pas bon pas bio pas cher", 
            image_url="fake url",
            url="fake url", 
            nutriscore=5, packaging="bouteille plastique")
        self.product1.save()
        self.product2.save()
        self.product1.category.add(self.category)
        self.product2.category.add(self.category)
        self.product1.save()
        self.product2.save()

    def tearDown(self):
        self.category.delete()
        self.product1.delete()
        self.product2.delete()


    def test_access_get_with_params(self):
        response = self.client.get("/results/jus de fruits/Pur jus d'orange")
        self.assertEqual(response.status_code , 200)
        self.assertContains(response, "Résultats")

    def test_no_access_get_no_param(self):
        response = self.client.get(reverse('research:results' ))
        self.assertEqual(response.status_code , 302)
        self.assertRedirects(response, reverse('research:index'))

