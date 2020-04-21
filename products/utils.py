#!/usr/bin/python3
# -*- coding: utf8 -*-
from products.get_datas import GetDatas
from products.models import Category, Product


def get_and_insert(size, categories, display_entry=None, add_cat=True): 
    criterions = ("product_name", "packaging", "nutrition_grades", "url", "image_url", "image_nutrition_url")
    
    print("\n", "*** Récupération des données depuis le site Open Food Fact ***")
    if not isinstance(categories, list):
        categories = [categories]
    try: 
        objet = GetDatas(size+5, categories, criterions) 
        dico_cat = objet.create_dict_cat()
        print("\n", "*** Insertion des données dans la base ***")
        for cat in categories:  
            list_prod = dico_cat[cat]
            new_cat = Category(name=cat)
            if add_cat : 
                if display_entry == 1:
                    print(cat, "> created")
                new_cat.save()
            nb_entry = 1
            for count, dico_prod in enumerate(list_prod):
                if nb_entry <= size : 
                    print(cat, " - ", nb_entry, dico_prod["product_name"])
                    try:  
                        new_prod = Product.objects.filter(name=dico_prod["product_name"])

                        if len(new_prod) == 0: 
                            new_prod = Product(\
                            name=dico_prod["product_name"],
                            image_url=dico_prod["image_url"],
                            url=dico_prod["url"],
                            nutriscore=dico_prod["nutrition_grades"],
                            packaging=dico_prod["packaging"], 
                            image_nutrition_url=dico_prod["image_nutrition_url"]
                            )
                            if display_entry == 1:
                                print("\t", count+1,new_prod, "> created")
                            new_prod.save()
                        elif len(new_prod) == 1:
                            new_prod = new_prod[0]
                        new_prod.category.add(new_cat)
                        nb_entry += 1
                    except Exception as e:
                        raise e
                        debug = Product.objects.filter(name = dico_prod["product_name"])
                        print("- - "*20)
                        print("Problème ici : {} | {}".format(cat,dico_prod["product_name"]))
                        print(debug[0].category, debug[0].name)
                        print("- - "*20)
    except Exception as e:
        print(e)