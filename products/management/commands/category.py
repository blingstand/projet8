#!/usr/bin/python3
# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand
from products.models import Category, Product

import os

from products.cat import * #list cat
from products.openfoodfact import OpenFoodFact #access to off api
from products.utils import * #usefull function


class Command(BaseCommand):

    all_cat = Category.objects.all()
    list_all_cat = [cat.name for cat in all_cat]

    help = "This cmd permits to add, delete, show entries in the table category."

    def add_arguments(self, parser):
        parser.add_argument('-show', "--s",dest="show",type=bool,
            help="show all the entries in category")
        parser.add_argument('-add', "--a", dest="add", type=str, default="", 
            help="Add a new category if it's possible")
        parser.add_argument('-delete', "--d", dest="del", type=str, default="",
            help="Delete a category if it's possible")

    def _show(self):
        print("**** Voici les {} catégories de ma base :".format(len(self.all_cat)))
        
        for count, cat in enumerate(self.list_all_cat):
            print(count, cat)

    def _add(self, new_cat):
        #I check wether this cat exists in OpenFoodFact db 
        off = OpenFoodFact()
        answer = off.this_cat_exists(new_cat)
        if answer: 
            print("Je peux ajouter cette catégorie : {}".format(new_cat))
            try:
                if not Category.objects.filter(name=new_cat).exists(): 
                    print("Maintenant je lui ajoute le même nombre de produits par catégorie que "\
                        "pour les autres catégories.")
                    #get the nb prod/cat
                    nb_prod = len(Product.objects.filter(category=self.all_cat[0]))
                    add_cat = False
                    get_and_insert(nb_prod, new_cat, add_cat)
                    print("Insertion de {} produits dans la catégorie {} réussie."\
                        .format(nb_prod, new_cat))
                else:
                    print("Cette catégorie a déjà été ajoutée.")

            except Exception as e:
                raise e

    def _del(self, cat):
        if cat in self.list_all_cat:
            print("J'enlève cat de la liste des catégories")
            try: 
                cat = Category.objects.get(name=cat)
                cat.delete()
                print("L'élément {} n'est plus dans la liste des catégories.".format(cat))
                return True
            except Exception as e:
                raise e
                print("Il y a eu un problème lors de la supression")
        print("L'élément {} n'est pas dans la liste des catégories.".format(cat))

    def handle(self, *args, **options):
        if options["show"]:
            self._show()
        elif options['add']:
            self._add(options['add'])
        elif options['del']:
            self._del(options['del'])
