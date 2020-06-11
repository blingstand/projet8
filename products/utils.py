#!/usr/bin/python3
# -*- coding: utf8 -*-
import datetime 

from products.get_datas import GetDatas
from products.models import Category, Product

def is_empty_db(pmc_cat):
    """ gets the cat from pureBeurre/products/cat.txt"""
    lencat = len(pmc_cat)
    if lencat > 0:
        return False
    return True
def get_tup_name_cat(pmc_cat):
    """ returns a tupple with all the cat from Category"""
    tup_name_cat = tuple([c.name for c in pmc_cat])
    return tup_name_cat 
def get_number_prod(querryset_cat):
    """ returns the number of prod/cat """
    nb_prod = len(Product.objects.filter(category=querryset_cat[0]))
    return nb_prod
def del_entries(cat, prod):
    cat.delete()
    prod.delete()
def get_dico_cat(size, cat, crit):
    """ returns a dict like dict[cat]=[product1, product2 ...]"""
    gdt = GetDatas(size+5, cat, crit) 
    dico_cat = gdt.create_dict_cat()
    return dico_cat
def create_cat(cat_name, count, report, create_report=0):
    """ create a category and save it"""
    new_cat = Category(name=cat_name)
    if create_report == 1:
        print(cat_name)
        report += f"{cat_name}\n"
    new_cat.save()
    return new_cat, report
def create_prod(new_prod, dico_prod, pmc_cat, count, nb_entry, report, create_report=0):
    """ create a prod and save it"""
    if len(new_prod) == 0: 
        new_prod = Product(\
        name=dico_prod["product_name"],
        image_url=dico_prod["image_url"],
        url=dico_prod["url"],
        nutriscore=dico_prod["nutrition_grades"],
        packaging=dico_prod["packaging"], 
        image_nutrition_url=dico_prod["image_nutrition_url"]
        )
        if create_report == 1:
            print("\t", count+1,new_prod)
            report += f"\t {count+1} {new_prod} \n"
        new_prod.save()
    elif len(new_prod) == 1:
        new_prod = new_prod[0]
    new_prod.category.add(pmc_cat)#pb
    new_prod.save()
    nb_entry += 1
    return nb_entry, report

def delete_table_cat_prod(querryset_cat, querryset_prod):
    querryset_cat.delete()
    querryset_prod.delete()
    print("0/ supression des données dans Category et Product")

def get_and_insert(size, categories, create_report=0): 
    """ populate the cat and prod tables"""
    criterions = ("product_name", "packaging", "nutrition_grades", "url", "image_url", "image_nutrition_url")
    
    date = datetime.datetime.today().strftime('%d-%m-%Y %H:%M:%S')
    report = f'Rapport de mise à jour du {date}\n'
    # if not isinstance(categories, list):
    #     categories = list(categories)
    try: 
        print("1/ récupération des données")
        report += "1/ récupération des données,\n"
        #get a dict like dict[cat]=(prod)
        dico_cat = get_dico_cat(size, categories, criterions)
        print("2/ données récupérées")
        report += "2/ données récupérées,\n"
        count_cat = 1 
        print("3/ début de l'insertion")
        report += "3/ début de l'insertion,\n"
        for name_cat in categories:  
            list_dico_prod = dico_cat[name_cat]
            pmc_cat, report = create_cat(name_cat, count_cat, report, 1)# mod_cat = <class 'products.models.Category'>
            count_cat += 1
            nb_entry = 1
            for count, dico_prod in enumerate(list_dico_prod):
                if nb_entry <= size : 
                    try:  
                        #avoid duplicate
                        new_prod = Product.objects.filter(name=dico_prod["product_name"])
                        nb_entry, report= create_prod(new_prod, dico_prod, pmc_cat, count, nb_entry, report, 1)
                    except Exception as e:
                        print("ERROR", e)
                        debug = Product.objects.filter(name = dico_prod["product_name"])
                        report += "\n- - "*20
                        report += "\nProblème ici : {} | {}".format(\
                            name_cat,dico_prod['product_name'])
                        report += debug[0].category, debug[0].name
                        report += "\n- - "*20
    except Exception as e:
        raise e
        report += f"\n{e}"
    print("4/ fin de l'insertion.")
    report += "4/ fin de l'insertion."
    return report