from django.core.management.base import BaseCommand
from products.models import Category, Product


import os

from products.get_datas import GetDatas

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
            criterions = ("product_name", "packaging", "nutrition_grades", "url", "image_url")
            categories = [a.lower() for a in ["Jus de fruits", "Céréales", "Confiture", "Barre chocolatee",\
                    "Lait", "Chips", "Bretzels", "Yaourts", "Poissons", "Gâteaux", \
                    "Pains de mie", "Charcuterie","Pizzas", "Tartes salées", "Spaghetti", "Riz",\
                    "Glaces", "Chocolat noir", "Soupes", "Compotes" ]]
            
            print("\n", "*** Récupération des données depuis le site Open Food Fact ***")
            objet = GetDatas(size, categories, criterions) 
            dico_cat = objet.create_dict_cat()
            print("\n", "*** Insertion des données dans la base ***")
            for cat in categories:  
                list_prod = dico_cat[cat]
                
                new_cat = Category(name=cat)
                new_cat.save()
                if display_entry == 1:
                        print(cat, "> created")
                for count, dico_prod in enumerate(list_prod):
                    new_prod = Product(\
                    name=dico_prod["product_name"],
                    image_url=dico_prod["image_url"],
                    url=dico_prod["url"],
                    nutriscore=dico_prod["nutrition_grades"],
                    packaging=dico_prod["packaging"],
                    category=new_cat)
                    if display_entry == 1:
                        print("\t", count+1,new_prod, "> created")
                    new_prod.save()
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
