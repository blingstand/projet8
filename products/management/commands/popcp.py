#!/usr/bin/python3
# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand
from products.models import Category, Product

import os
from products.cat import *
from products.utils import *

CATEGORIES = [c.lower() for c in CAT]
class Command(BaseCommand):
    help = "This cmd populate your tables category or product."

    def add_arguments(self, parser):
        parser.add_argument('-select_number_prod', "--snp",
            dest="snp",
            type=int, 
            default=5,  
            help="select the number of products by category", 
            choices=list(range(3,21)))
        parser.add_argument('-display_entry', "--de",
            dest="de",
            type=int, 
            default=0,  
            help="select 1 to display each new entry", 
            choices=[0,1])

    def _fill_db(self, size, display_entry = 0):
        if size != 5:
            print("\n", "Vous avez choisis", size, "produits/categorie.")
        else:
            print("\nJ'utilise la valeur par défaut de 5 produits/categorie"\
                "\nmais cette valeur peut être changée avec python manage.py pop_db --snp <int>")
        if len(Category.objects.all()) == 0:
            get_and_insert(size, CATEGORIES)
        else :
            response = input("Votre table Category n'est pas vide ..."\
                "\n1 \t>  vider la table,"\
                "\nautre \t>  quitter.\n>")
            if response == "1":
                os.system("python manage.py dropcp")
                print("la table est vide vous pouvez relancer la commande pour ajouter des tables.")

    def handle(self, *args, **options):
        print("\n", "* "*30, "\n")
        print("Cette commande peuple les tables Category et Product de la base."\
            "\nAstuce : Tapez python manage.py pop_db -h pour découvrir les arguments \nque "\
            "vous pouvez passer à cette commande")
        self._fill_db(options["snp"], options["de"]) 
        print("\n", "* "*30, "\n")
