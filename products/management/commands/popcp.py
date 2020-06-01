""" this scipt populates the db with datas from get datas """
#!/usr/bin/python3
# -*- coding: utf8 -*-


import os
from django.core.management.base import BaseCommand
from products.models import Category


from products.utils import get_and_insert

def get_cat():
    """ get the cat from pureBeurre/products/cat.txt"""
    with open("products/cat.txt", "r") as fichier:
        a = fichier.read()
    base_cat = a.split(", ")
    base_cat = [cat.lower() for cat in base_cat]
    base_cat = sorted(base_cat)
    return base_cat


class Command(BaseCommand):
    """ this class manages the parameters you can pass to python manage.py"""
    help = "This cmd populate your tables category or product."
    CATEGORIES = get_cat()
    def add_arguments(self, parser):
        """ manages the args to pass to popcp"""
        parser.add_argument('-number_prod',dest="np", default = 5, type=int, \
            help="select the number of products by category", choices=list(range(4, 21)))
        parser.add_argument('-display_entry', "--de", dest="de", type=int, default=0,\
            help="select 1 to display each new entry", choices=[0, 1])

    def _fill_db(self, size, display_entry=0):
        """ manages the filling of the db """
        if size != 5:
            print("\n", "Vous avez choisis", size, "produits/categorie.")
        else:
            print("\nJ'utilise la valeur par défaut de 5 produits/categorie"\
                "\nmais cette valeur peut être changée avec python manage.py pop_db <int>")
        if len(Category.objects.all()) == 0:
            get_and_insert(size, self.CATEGORIES, display_entry)
        else:
            response = input("Votre table Category n'est pas vide ..."\
                "\n1 \t>  vider la table,"\
                "\nautre \t>  quitter.\n>")
            if response == "1":
                os.system("python manage.py dropcp")
                print("la table est vide vous pouvez relancer la commande pour ajouter des tables.")

    def handle(self, *args, **options):
        """ throws _fill_db function with args"""
        print("\n", "* "*30, "\n")
        print("Cette commande peuple les tables Category et Product de la base."\
            "\nAstuce : Tapez python manage.py pop_db -h pour découvrir les arguments \nque "\
            "vous pouvez passer à cette commande")
        self._fill_db(options["np"], options["de"])
        print("\n", "* "*30, "\n")
