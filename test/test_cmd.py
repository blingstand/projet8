#global import
from unittest import mock, skip
from random import randint

#django import
from django.test import TestCase
from django.urls import reverse

#import from my app
from .utils import create_x_cats, create_x_prods

#import from others app
from products.get_datas import GetDatas
from products.models import Category, Product
from products.utils import get_and_insert, is_empty_db, get_number_prod, \
get_tup_name_cat, del_entries, create_cat, create_prod, get_dico_cat

print("test_commands\n", "_ "*20)
#tests unitaires

class UnitTest(TestCase):

    def setUp(self): 
        """ initiate vars """
        self.cat1, self.cat2 = create_x_cats(2)
        self.prod1, self.prod2, self.prod3 = create_x_prods(3, self.cat1) #3 prod from cat1 

        self.search_cat = Category.objects.all()
        self.search_prod = Product.objects.all()


    def test_get_cat(self): 
        """ tests wether the function can return false if db is not empty """
        search = Category.objects.all()
        is_empty = is_empty_db(self.search_cat)
        self.assertFalse(is_empty) 
    
    def test_get_number_prod(self):
        """ tests wether the function can return the number of prod for a cat
        note : all cats have the same number of prods  """
        number_prod = get_number_prod(self.search_cat)
        self.assertEqual(3, number_prod)

    def test_get_tup_name_cat(self):
        """ tests wether the function can get the name of the cat in Category"""
        tup = get_tup_name_cat(self.search_cat)
        self.assertEqual(tup, ('test_cat1', 'test_cat2'))


    def test_del_entries(self):
        """ tests wether the function can delete all the entries from Cat and Prod """
        before = len(self.search_cat) + len(self.search_prod)
        self.assertTrue(before > 0)
        del_entries(self.search_cat, self.search_prod )
        after = len(self.search_cat) + len(self.search_prod)
        self.assertTrue(after == 0)    
    

    def test_create_cat(self):
        """tests whether the function can add a category in table category"""
        before = len(self.search_cat)
        report = ""
        create_cat("123", 1, report)
        after = len(Category.objects.all())
        self.assertEqual(before+1, after)
    
    def test_create_prod(self):
        before = len(self.search_prod)
        dico_prod={
            "product_name":"new_prod", 
            "image_url":"fake url",
            "url":"fake url", 
            "nutrition_grades":3, 
            'packaging':'osef',
            'image_nutrition_url':'osef'
            }
        new_prod = Product.objects.filter(name=dico_prod["product_name"])
        report = ""
        create_prod(new_prod, dico_prod, self.cat1, 1, 1, report) 
        #new_prod, dico_prod, pmc_cat, count, nb_entry, report, create_report=0
        after = len(Product.objects.all())
        self.assertEqual(before+1, after)

#test intégration

class IntergraTest(TestCase): 
    def test_get_and_insert(self):
        """test whether the function can populate the db"""
        before = len(Category.objects.all())
        self.assertEqual(before, 0)
        # create 1 cat and 3 prod
        cat = "test_cat"
        list_prod = []
        for nb in range(1, 4):
            prod = {
            'product_name': f"test_prod{nb}", 'image_url' : "fake url",
            'url': "fake url", 'nutrition_grades': randint(1,5), "packaging" : "bidon", 
            'category' : cat, 'image_nutrition_url':'fake url'}
            list_prod.append(prod)

        dico_cat = {cat:list_prod}
        patcher = mock.patch("products.utils.get_dico_cat", return_value=dico_cat )
        self.addCleanup(patcher.stop)
        instance = patcher.start()
        
        report = get_and_insert(3, ["test_cat"], create_report=1)
        report = report.split(" ")
        self.assertTrue("test_prod1" in report)
        self.assertTrue("test_prod2" in report)
        self.assertTrue("test_prod3" in report)
        