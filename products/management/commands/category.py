"""this script manages the list of categories, it can add or delete a category"""
#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand
from products.models import Category, Product

from products.openfoodfact import OpenFoodFact #access to off api
from products.utils import get_and_insert


class Command(BaseCommand):
    """ this class manages the parameters you can pass to python manage.py"""
    all_cat = Category.objects.all()
    list_all_cat = [cat.name for cat in all_cat]

    help = "This cmd permits to add, delete, show entries in the table category."

    def add_arguments(self, parser):
        """ manages the args to pass to category"""
        parser.add_argument('-show', dest="show", type=bool, default=True,\
            help="show all the entries in category")
        parser.add_argument('-add', "--a", dest="add", type=str, \
            help="Add a new category if it's possible")
        parser.add_argument('-delete', "--d", dest="del", type=str, \
            help="Delete a category if it's possible")

    def _show(self):
        """shows the cat from the list"""
        with open("products/cat.txt", "r") as fichier:
            a = fichier.read()

        base_cat = a.split(", ")
        base_cat = [cat.lower() for cat in base_cat]
        base_cat = sorted(base_cat)
        print(f"**** Voici les {len(base_cat)} catégories présentes au départ : \n{base_cat} ")

        print(f"**** Voici les {len(self.all_cat)} catégories présente dans la table Category :")
        for count, cat in enumerate(self.list_all_cat):
            print(count, cat)

    def _add(self, new_cat):
        """ add a category to the list if it exists"""
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

            except Exception as exept:
                raise exept

    def _del(self, cat):
        """ drop a category from the list"""
        if cat in self.list_all_cat:
            print("J'enlève cat de la liste des catégories")
            try:
                cat = Category.objects.get(name=cat)
                cat.delete()
                print("L'élément {} n'est plus dans la liste des catégories.".format(cat))
                return True
            except:
                print("Il y a eu un problème lors de la supression")
        print("L'élément {} n'est pas dans la liste des catégories.".format(cat))

    def handle(self, *args, **options):
        """throw a function according to the parametters"""
        print(args, options)
        if options["show"]:
            print(options["show"])
            self._show()
        elif options['add']:
            self._add(options['add'])
        elif options['del']:
            self._del(options['del'])
