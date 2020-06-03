from django.test import TestCase
from django.urls import reverse

from unittest import mock, skip


from products.get_datas import GetDatas
from products.models import Category, Product
from products.utils import get_and_insert, is_empty_db, get_number_prod, \
get_list_cat, del_entries, create_cat, create_prod, get_dico_cat

print("test_commands\n", "_ "*20)
#tests unitaires
@skip
class UnitTest(TestCase):

    def setUp(self): 
        """ initiate vars """
        self.category = Category(name='jus')
        self.category.save()
        self.category2 = Category(name='vin')
        self.category2.save()
        self.product1 = Product(
            name="prod1", 
            image_url="fake url",
            url="fake url", 
            nutriscore=3)
        self.product2 = Product(
            name="prod2", 
            image_url="fake url",
            url="fake url", 
            nutriscore=5)
        self.product3 = Product(
            name="prod3", 
            image_url="fake url",
            url="fake url", 
            nutriscore=5)
        self.product1.save()
        self.product2.save()
        self.product3.save()
        self.product1.category.add(self.category)
        self.product2.category.add(self.category)
        self.product3.category.add(self.category)
        self.product1.save()
        self.product2.save()
        self.product3.save()
        self.cat = Category.objects.all()
        self.prod = Product.objects.all()
    def test_get_cat(self): 
        """ tests wether the function can return false if db is not empty """
        is_empty = is_empty_db(self.cat)
        self.assertFalse(is_empty) 
    def test_get_number_prod(self):
        """ tests wether the function can return the number of prod for a cat
        note : all cats have the same number of prods  """
        number_prod = get_number_prod(self.cat)
        self.assertEqual(3, number_prod)
    def test_get_list_cat(self):
        """ tests wether the function can get the name of the cat in Category"""
        list_cat = get_list_cat(self.cat)
        self.assertEqual(list_cat, ('jus', 'vin'))
    def test_del_entries(self):
        """ tests wether the function can delete all the entries from Cat and Prod """
        before = len(self.cat) + len(self.prod)
        self.assertTrue(before > 0)
        del_entries(self.cat, self.prod )
        after = len(self.cat) + len(self.prod)
        self.assertTrue(after == 0)    
    def test_create_cat(self):
        """tests whether the function can add a category in table category"""
        before = len(self.cat)
        create_cat("123")
        after = len(Category.objects.all())
        self.assertEqual(before+1, after)
    def test_create_prod(self):
        before = len(self.prod)
        dico_prod={
            "product_name":"new_prod", 
            "image_url":"fake url",
            "url":"fake url", 
            "nutrition_grades":3, 
            'packaging':'osef',
            'image_nutrition_url':'osef'
            }
        new_prod = Product.objects.filter(name=dico_prod["product_name"])
        create_prod(new_prod, dico_prod, self.category, 1, 1)
        after = len(Product.objects.all())
        self.assertEqual(before+1, after)

#test intégration
class IntergraTest(TestCase): 
    def test_get_and_insert(self):
        """test whether the function can populate the db"""
        before = len(Category.objects.all())
        self.assertEqual(before, 0)
        dico_prod={
            "product_name":"new_prod", 
            "image_url":"fake url",
            "url":"fake url", 
            "nutrition_grades":3, 
            'packaging':'osef',
            'image_nutrition_url':'osef'}
        dico_cat = {"cat":[dico_prod]}
        get_dico_cat = mock.MagicMock(return_value=dico_cat)
        self.assertEqual(get_dico_cat(), {"cat":[dico_prod]})
        
        get_and_insert(1, "new_cat")
        afterc = len(Category.objects.all())
        self.assertEqual(afterc, 1)
        afterp = len(Product.objects.all())
        self.assertEqual(afterp, 1)
        cat = Category.objects.all()[0]
        self.assertEqual(cat.name, "new_cat")
        prod = Product.objects.all()[0]
        self.assertEqual(prod.name, "new_prod")