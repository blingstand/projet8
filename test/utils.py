from random import randint
from products.models import Category, Product


 
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
