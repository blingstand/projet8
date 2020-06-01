#!/usr/bin/python3
# -*- coding: utf8 -*-
from products.get_datas import GetDatas
from products.models import Category, Product

def is_empty_db(cat):
    """ gets the cat from pureBeurre/products/cat.txt"""
    lencat = len(cat)
    if lencat > 0:
        return False
    return True
def get_list_cat(cat):
    """ returns a tupple with all the cat from Category"""
    tup_cat = tuple([c.name for c in cat])
    return tup_cat 
def get_number_prod(cat):
    """ returns the number of prod/cat """
    print(Product.objects.filter(category=cat[0]))
    nb_prod = len(Product.objects.filter(category=cat[0]))
    return nb_prod
def del_entries(cat, prod):
    cat.delete()
    prod.delete()
def get_dico_cat(size, cat, crit):
    """ returns a dict like dict[cat]=[product1, product2 ...]"""
    gdt = GetDatas(size+5, cat, crit) 
    dico_cat = gdt.create_dict_cat()
    print("\n", "*** Insertion des données dans la base ***")
    return dico_cat
def create_cat(cat, verbose=1):
    new_cat = Category(name=cat)
    if verbose == 1:
        print(cat, "> created")
    new_cat.save()
def create_prod(new_prod, dico_prod, new_cat, count, nb_entry, verbose=1):
    if len(new_prod) == 0: 
        new_prod = Product(\
        name=dico_prod["product_name"],
        image_url=dico_prod["image_url"],
        url=dico_prod["url"],
        nutriscore=dico_prod["nutrition_grades"],
        packaging=dico_prod["packaging"], 
        image_nutrition_url=dico_prod["image_nutrition_url"]
        )
        if verbose == 1:
            print("\t", count+1,new_prod, "> created")
        new_prod.save()
    elif len(new_prod) == 1:
        new_prod = new_prod[0]
    new_prod.category.add(new_cat)
    new_prod.save()
    nb_entry += 1
    return nb_entry
def get_and_insert(size, categories, verbose=0): 
    """ populate the cat and prod tables"""
    criterions = ("product_name", "packaging", "nutrition_grades", "url", "image_url", "image_nutrition_url")
    repport = ''
    repport += "*** Récupération des données depuis le site Open Food Fact ***"
    if not isinstance(categories, list):
        categories = [categories]
    try: 
        dico_cat = get_dico_cat(size, categories, criterions)

        for cat in categories:  
            print("cat : ", cat)
            list_dico_prod = dico_cat[cat]
            create_cat(cat)
            nb_entry = 1
            for count, dico_prod in enumerate(list_dico_prod):
                print(count, dico_prod)
                if nb_entry <= size : 
                    repport += f"\n{cat} - {nb_entry}, {dico_prod['product_name']}"
                    try:  
                        #avoid duplicate
                        new_prod = Product.objects.filter(name=dico_prod["product_name"])
                        nb_entry = create_prod(new_prod, dico_prod, cat, count, nb_entry)
                    except Exception as e:
                        print("1", e)
                        debug = Product.objects.filter(name = dico_prod["product_name"])
                        repport += "\n- - "*20
                        repport += "\nProblème ici : {} | {}".format(\
                            cat,dico_prod['product_name'])
                        repport += debug[0].category, debug[0].name
                        repport += "\n- - "*20
    except Exception as e:
        raise e
        repport += f"\n{e}"
    return repport