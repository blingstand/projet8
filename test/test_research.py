
#global
from unittest import mock, skip

#django
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.test import TestCase
from django.urls import reverse

#other apps
from research.form import SearchForm, AdvancedSearchForm
import research.views as v
import research.searcher as s
from products.models import Category, Product

#app
from .utils import create_user_and_profile, create_x_cats, create_x_prods
print("test_research\n", "_ "*20)
#-- unit test_get --

class UnitTest(TestCase):
    def setUp(self):
        #cat1 : 3 prods / cat2 : 1 prod
        self.cat1, self.cat2 = create_x_cats(2)
        self.prod1, self.prod2, self.prod3, self.prod4 = create_x_prods(4, self.cat1)
        self.prod4.category.add(self.cat2)

        self.prod1.name = "Pur jus d'orange sans pulpe"
        self.prod2.name = "Jus d'orange pas bon pas bio pas cher"
        self.prod3.name, self.prod4.name = "Pomme pomme jus", "Poppom à la pomme"
        self.cat1.name, self.cat2.name = "jus de fruits", "compote"

        [elem.save() for elem in [self.prod1, self.prod2, self.prod3, self.prod4]]
        [elem.save() for elem in [self.cat1, self.cat2]]
        
    def test_get_make_a_search(self):
        """ Tests whether the function returns the wanted value after 
        a search based on input and sometime category"""
        #---wanted_values = ["prod", "sub"]
        get_from_input = "Jus d'orange pas bon pas bio pas cher"
        wanted_values = ["prod", "sub"]
        given_category = "jus de fruits"
        search, product, substitutes = v.make_a_search(get_from_input, wanted_values, given_category)
        self.assertTrue(product, "Pur jus d'orange sans pulpe")
        self.assertTrue(substitutes[0], "Pur jus d'orange sans pulpe")
        #---wanted_values = ["prod", "categories"]
        wanted_values = ["prod", "categories"]
        given_category = None
        search, product, categories = v.make_a_search(get_from_input, wanted_values, given_category)
        self.assertTrue(product, "Jus d'orange pas bon pas bio pas cher")
        self.assertTrue(categories[0], "jus de fruits") 
        #---wanted_values = ["prod", "categories"]
        wanted_values = None
        given_category = None
        response = v.make_a_search(get_from_input, wanted_values, given_category)
        self.assertTrue(response, f"Verifie le paramètre wanted (valeur actuelle : {wanted_values})")

    def test_get_Search_get_prod(self):
        """ Tests the output if the searcher can find smth and not"""
        #can find
        search = s.Search("Pur jus d'orange sans pulpe")
        prod = search.get_prod()
        self.assertTrue(prod, "Pur jus d'orange sans pulpe")
        #can't find
        search = s.Search("123456")
        prod = search.get_prod()
        self.assertTrue(prod == None)

    def test_get_Search_list_pot_prod(self, category=None): 
        """ Tests whether the function returns a list of potential prod """
        
        search = s.Search("pomme")
        #without cat 
        list_pot_prod = search.list_pot_prod()
        categories = search.cat_to_choose
        self.assertTrue(len(list_pot_prod), 2) #prod3 et pro4 
        #withcat
        list_pot_prod = search.list_pot_prod(category="compote")
        self.assertTrue(len(list_pot_prod), 1) #only prod 4

    
    def test_get_Search_cat_to_choose(self):
        """ Tests whether function returns cat from the list of potential prod"""
        search = s.Search("pomme")
        categories = search.cat_to_choose
        self.assertTrue(len(categories), 2) #jus de fruit an compote


    def test_get_Search_list_sub(self):
        """ Tests whether function returns a dictionary full of substitute sorted by nutriscore """
        search = s.Search("pomme")
        list_sub = search.list_sub(category=self.cat1)
        self.assertTrue(len(list_sub), 3) #3 prods

#-- integration test_get -- 

class ResultsViewTests(TestCase):

    def setUp(self):
        patcher = mock.patch("research.views.SearchForm")
        self.addCleanup(patcher.stop)
        mock_form_class = patcher.start()
        self.mock_form = mock_form_class.return_value
        
        #cat1 : 2 prods 
        self.cat1 = create_x_cats(1)[0]
        self.prod1, self.prod2 = create_x_prods(2, self.cat1)
        self.prod1.name = "Pur jus d'orange sans pulpe"
        self.prod2.name = "Jus d'orange pas bon pas bio pas cher"
        [elem.save() for elem in [self.prod1, self.prod2]]



    def test_get_no_res_access_wrong_params(self):
        """ Tests whether the function redirects if params are wrong"""
        response = self.client.get("/p10/results/aaa/aaa")
        self.assertEqual(response.status_code , 302)
        self.assertRedirects(response, reverse('research:index'))

    def test_get_no_res_access_get_no_param(self):
        """ Tests whether the function redirects if no param"""
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
        """ Tests whether the function returns a web page """
        response = self.client.get('http://127.0.0.1:8000/p10/index')
        self.assertEqual(response.status_code, 200)
        
    def test_index_post_form_is_not_valid(self):
        """ Tests whether the function loads an error page if form is not valid """
        self.mock_form.is_valid.return_value = False
        response = self.client.post(reverse("research:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Problème dans le formulaire")
    
    def test_index_post_find_result(self):
        """ Tests whether the function gets the input data, find a prod, subs and load aresult page """
        self.mock_form.is_valid.return_value = True
        self.mock_form.cleaned_data = {"simple_search" : "Pur jus d'orange sans pulpe"}
        response = self.client.post(reverse("research:index"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vous pouvez remplacer cet aliment par ... ! ")


    def test_index_post_do_not_find_result(self):
        """ Tests whether the function gets the input data, but do not find anything """
        self.mock_form.is_valid.return_value = True
        self.mock_form.cleaned_data = {"simple_search" : "123"}
        response = self.client.post(reverse("research:index"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pas de résultats dans la base actuellement")

    def test_index_post_no_result_but_category(self):
        """ Tests whether the function gets the input data,  do not find anything but propose new categories """
        self.mock_form.is_valid.return_value = True
        self.mock_form.cleaned_data = {"simple_search" : "pas sans pulpe"}
        response = self.client.post(reverse("research:index"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pas de résultats parfaitement identiques ")
