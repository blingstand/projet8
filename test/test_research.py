from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.test import TestCase
from django.urls import reverse

from unittest import mock, skip

from research.form import SearchForm, AdvancedSearchForm
import research.views as v
import research.searcher as s
from products.models import Category, Product

print("test_research\n", "_ "*20)
#-- unit test --

class UnitTest(TestCase):
    def setUp(self):
        #a cat
        self.category = Category(name="jus de fruits")
        self.category.save()
        #a product
        self.product1 = Product(
            name="Pur jus d'orange sans pulpe", 
            image_url="https://static.openfoodfacts.org/images/products/350/211/000/9449/front_fr.80.400.jpg",
            url="https://world.openfoodfacts.org/product/3502110009449/pur-jus-d-orange-sans-pulpe-tropicana", 
            nutriscore=3, packaging="carton")
        self.product2 = Product(
            name="Jus d'orange pas bon pas bio pas cher", 
            image_url="fake url",
            url="fake url", 
            nutriscore=5, packaging="osef")
        self.product1.save()
        self.product2.save()
        self.product1.category.add(self.category)
        self.product2.category.add(self.category)
        self.product1.save()
        self.product2.save()
        self.category2 = Category(name="compote")
        self.category2.save()
        self.product3 = Product(
            name="Pomme pomme jus", 
            image_url="fake url",
            url="fake url", 
            nutriscore=5, packaging="osef")
        self.product4 = Product(
            name="Poppom à la pomme", 
            image_url="fake url",
            url="fake url", 
            nutriscore=5, packaging="osef")
        self.product3.save()
        self.product4.save()
        self.product3.category.add(self.category)
        self.product4.category.add(self.category2)
        self.product3.save()
        self.product4.save()
        
    def test_make_a_search(self):
        """ tests whether the function returns the wanted value after 
        a search based on input and sometime category"""
        #---wanted_values = ["prod", "sub"]
        get_from_input = "Jus d'orange pas bon pas bio pas cher"
        wanted_values = ["prod", "sub"]
        given_category = "jus de fruits"
        product, substitutes = v.make_a_search(get_from_input, wanted_values, given_category)
        self.assertTrue(product, "Pur jus d'orange sans pulpe")
        self.assertTrue(substitutes[0], "Pur jus d'orange sans pulpe")
        #---wanted_values = ["prod", "categories"]
        wanted_values = ["prod", "categories"]
        given_category = None
        product, categories = v.make_a_search(get_from_input, wanted_values, given_category)
        self.assertTrue(product, "Jus d'orange pas bon pas bio pas cher")
        self.assertTrue(categories[0], "jus de fruits") 

    def test_Search_get_prod(self):
        """ Tests the output if the searcher can find smth and not"""
        #can find
        search = s.Search("Pur jus d'orange sans pulpe")
        prod = search.get_prod()
        self.assertTrue(prod, "Pur jus d'orange sans pulpe")
        #can't find
        search = s.Search("123456")
        prod = search.get_prod()
        self.assertTrue(prod == None)

    def test_Search_list_pot_prod(self, category=None): 
        """ Tests whether the function returns a list of potential prod """
        
        search = s.Search("pomme")
        #without cat 
        list_pot_prod = search.list_pot_prod()
        categories = search.cat_to_choose
        print(categories)
        self.assertTrue(len(list_pot_prod), 2) #prod3 et pro4 
        #withcat
        list_pot_prod = search.list_pot_prod(category="compote")
        self.assertTrue(len(list_pot_prod), 1) #only prod 4

    
    def test_Search_cat_to_choose(self):
        """ Tests whether function returns cat from the list of potential prod"""
        search = s.Search("pomme")
        categories = search.cat_to_choose
        print(categories)
        self.assertTrue(len(categories), 2) #jus de fruit an compote


    def test_Search_list_sub(self):
        """ Tests whether function returns a dictionary full of substitute sorted by nutriscore """
        search = s.Search("pomme")
        list_sub = search.list_sub(category=self.category)
        print(list_sub)
        self.assertTrue(len(list_sub), 3) #3 prods


class ResultsViewTests(TestCase):

    def setUp(self):
        patcher = mock.patch("research.views.SearchForm")
        self.addCleanup(patcher.stop)
        mock_form_class = patcher.start()
        self.mock_form = mock_form_class.return_value
        #a category 
        self.category = Category(name="jus de fruits")
        self.category.save()
        #2 products
        self.product1 = Product(
            name="Pur jus d'orange sans pulpe", 
            image_url="https://static.openfoodfacts.org/images/products/350/211/000/9449/front_fr.80.400.jpg",
            url="https://world.openfoodfacts.org/product/3502110009449/pur-jus-d-orange-sans-pulpe-tropicana", 
            nutriscore=3, packaging="carton")
        self.product2 = Product(
            name="Jus d'orange pas bon pas bio pas cher", 
            image_url="fake url",
            url="fake url", 
            nutriscore=5, packaging="osef")
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


    def test_res_access_get_with_params(self):
        response = self.client.get("/results/jus de fruits/Pur jus d'orange")
        self.assertEqual(response.status_code , 200)
        self.assertContains(response, "Résultats")

    def test_no_res_access_wrong_params(self):
        response = self.client.get("/results/aaa/aaa")
        self.assertEqual(response.status_code , 302)
        self.assertRedirects(response, reverse('research:index'))

    def test_no_res_access_get_no_param(self):
        response = self.client.get(reverse('research:results' ))
        self.assertEqual(response.status_code , 302)
        self.assertRedirects(response, reverse('research:index'))


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
            nutriscore=5, packaging="osef")
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
