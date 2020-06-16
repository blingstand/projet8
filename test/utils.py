#global
from random import randint

#django
from django.contrib.auth.models import User

#other apps
from products.models import Category, Product
from user.models import Profile

def create_user_and_profile(pseudo, password): 
    new_user = User(username=pseudo)
    profile = Profile(user=new_user)
    new_user.set_password(password)
    new_user.save()
    profile.save()
    return new_user, profile
 
def create_x_cats(number_cat):
    list_cat = []
    for nbc in range(1, number_cat+1):
        category = Category(name=f"test_cat{nbc}")
        category.save()
        list_cat.append(category)
    return list_cat


def create_x_prods(number_prod, cat_they_belong):
    list_prod = []
    for nbp in range(1, number_prod+1):
        prod = Product(
        name= f"test_prod{nbp}", image_url="fake url",
        url="fake url", nutriscore=randint(1,5))
        prod.save()
        prod.category.add(cat_they_belong)
        prod.save()
        list_prod.append(prod)
    return list_prod

def popdatabase():
    category = Category(name="jus de fruits")
    category.save()
    list_prod = []
    product1 = Product(
        name="Pur jus d'orange sans pulpe", 
        image_url="https://static.openfoodfacts.org/images/products/350/211/000/9449/front_fr.80.400.jpg",
        url="https://world.openfoodfacts.org/product/3502110009449/pur-jus-d-orange-sans-pulpe-tropicana", 
        nutriscore="b", packaging="osef")
    list_prod.append(product1)
    product2 = Product(
        name="Jus d'orange - Solevita - 1 L", 
        image_url="https://static.openfoodfacts.org/images/products/20245900/front_fr.148.full.jpg",
        url="https://fr.openfoodfacts.org/produit/20245900/jus-d-orange-solevita", 
        nutriscore="c", packaging="osef")
    list_prod.append(product2)
    product1.save()
    product2.save()
    product1.category.add(category)
    product2.category.add(category)
    product1.save()
    product2.save() 
    return list_prod