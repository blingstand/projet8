""" this scipt populates the db with datas from get datas """
#!/usr/bin/python3
# -*- coding: utf8 -*-


import os, datetime
from django.core.management.base import BaseCommand
from products.models import Category, Product

from config.settings import BASE_DIR
from products.utils import get_and_insert, is_empty_db, get_number_prod, \
get_tup_name_cat, del_entries, delete_table_cat_prod


querryset_cat = Category.objects.all()
querryset_prod = Product.objects.all()

class Command(BaseCommand):
    """ this class manages the parameters you can pass to python manage.py"""
    help = "This cmd update your tables category or product with fresh values."
    
    def _update(self):
        """ manages the filling of the db """
        tup_name_cat = get_tup_name_cat(querryset_cat)
        print(f"Catégories de la base : {tup_name_cat}")
        if is_empty_db(tup_name_cat):
            text = "La base est vide ! Il n'y a rien à actualiser\n"\
            "Commencez par la remplir avec popcp <valeur:int> !"
            return text

        number_prod_in_cat1 = get_number_prod(querryset_cat)
        print(f"il y a {number_prod_in_cat1} produits par catégories dans votre base avant actualisation")
        print("début de la mise à jour de la base ...")
        print("* * * ")
        delete_table_cat_prod(querryset_cat, querryset_prod)
        report = get_and_insert(number_prod_in_cat1, tup_name_cat)
        date = datetime.datetime.today().strftime('%d-%m-%Y %H:%M:%S')
        report += f'\n\n> Rapport de mise à jour du {date}\n'

        print("* * * ")
        print("fin de la mise à jour de la base.")
        querryset_cat2 = Category.objects.all()
        number_prod_in_cat2 = get_number_prod(querryset_cat2)
        print(f"vérification que tout se soit bien passé : {number_prod_in_cat2 == number_prod_in_cat1}")
        with open(f"{BASE_DIR}/update.txt", "w") as fichier:
            fichier.write(report)
        print(f"retrouvez le rapport de mise à jour ici : {BASE_DIR}/update.txt")

            


    def handle(self, *args, **options):
        """ throws _fill_db function with args"""
        print("\n", "* "*30, "\n")
        print("Cette commande peuple les tables Category et Product de la base."\
            "\nAstuce : Tapez python manage.py pop_db -h pour découvrir les arguments \nque "\
            "vous pouvez passer à cette commande")
        self._update()
        print("\n", "* "*30, "\n")
