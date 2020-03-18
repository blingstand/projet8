# pour importer la lib openfoodfact : pip install git+https://github.com/openfoodfacts/openfoodfacts-python
"""
    Maintenant ma base est remplie par 380 lignes
"""
#!/usr/bin/python3
# -*- coding: utf8 -*-
import sys
from datetime import datetime
import openfoodfacts


class Fill_DB():

    SIZE_RESEARCH = 100
    
    TUP_COL = ("product_name", "packaging", "nutrition_grades", "url", "image_url" )

    def __init__(self, nb_product, category, criterions):
        self.nb_product = nb_product
        self.category = category
        self.criterions = criterions
    def call_api(self, category):
        """ Finds 50 prods from a given cat """
        results = openfoodfacts.products.advanced_search({
            "search_terms":"",
            "tagtype_0":"categories ",
            "tag_contains_0":"contains",
            "tag_0": category,
            "tagtype_1":"countries  ",
            "tag_contains_1":"contains",
            "tag_1":"France",
            "page_size": self.SIZE_RESEARCH})

        list_prod = results["products"] #keeps only the products

        return list_prod
    def _kick_duplicates(self, my_list, category):
        """ Kickes the prod with a duplicate name"""

        list_prod_name = []
        list_prod = []

        for prod in my_list: #selects prod from list of products
            name = prod["product_name"].lower()
            if name not in list_prod_name: #anti-duplicate name
                list_prod_name.append(name)
                list_prod.append(prod)
        return list_prod
    def _kick_empty_values(self, my_list, category):
        """kickes a prod from the list if there is no value for 1 selected column"""
        accepted_prod, list_prod = [],[]
        for prod in my_list:
            for criterion in self.criterions:
                try : #to fix error
                    if prod[criterion]!=None and prod not in accepted_prod:
                       accepted_prod.append(prod)
                except Exception as e:
                    accepted_prod.remove(prod)
                    break
        for prod in accepted_prod:
            list_prod.append(prod)

        return list_prod
    def _respect_size(self, my_list, category):
        """ Limits the number of element at 20 """
        list_resp_size = []
        for prod in my_list:
            if len(list_resp_size)<20:
                list_resp_size.append(prod)
        return list_resp_size
    def _just_keep_criterions(self, my_list, category):
        """ return a list filled by dicts of product with only cols present in self.criterions"""
        new_list = []
        count = 0
        for prod in my_list:
            new_prod = {}
            # print(new_prod, prod["product_name"])
            for key in prod:
                if key in self.criterions:
                    new_prod[key] = prod[key]
            if len(new_prod) == len(self.criterions):
                new_list.append(new_prod)
        return new_list
    def _get_list_for_cat(self, category):
        """ Searches in API and returns a list of 20 prod """

        first_list_prod = self.call_api(category) #list of 50 prods with same cat
        #list prod with no duplicate names
        list_with_no_duplicate_name = self._kick_duplicates(first_list_prod, category)

        #list with no empty values for selected columns
        list_without_empty = self._kick_empty_values(list_with_no_duplicate_name, category)

        #keep just the col writen in self.TUP_COL
        list_prod_with_selec_col = self._just_keep_criterions(list_without_empty, category)

        #list do not pass the SIZE_IN_TAB limit
        list_20_prod = self._respect_size(list_prod_with_selec_col, category)

        return list_20_prod
    def create_dict_prod(self):
        """Creates the dict_prod with previous functions  """

        dict_prod = {} #create dico

        print(self.category)
        for cat in self.category:
            list_prod = self._get_list_for_cat(cat)
            print(len(list_prod))
            dict_prod[cat] = list_prod

        return dict_prod

categories = ("Jus de fruits", "Céréales", "Confiture", "Barre chocolatee",\
    "Lait", "Chips", "Bretzels", "Yaourts", "Poissons", "Gâteaux", \
    "Pains de mie", "Charcuterie","Pizzas", "Tartes salées", "Spaghetti", "Riz",\
    "Glaces", "Chocolat noir", "Soupes", "Compotes" )
criterions = ("product_name", "packaging", "nutrition_grades", "url", "image_url" )
criterion_name = ("nom", "conditionnement", "nutriscore", "lien", "lien vers image" )

category = ["Jus de fruits", "Céréales"]
fdb = Fill_DB(3, category, criterions)
dico_cat = fdb.create_dict_prod()

for cat in category:  
    dico_prod = dico_cat[cat]
    print("- -"*20)
    
    for count, prod in enumerate(dico_prod):
        index = 0
        print("n°{}".format(count+1))
        print("category : ", cat)
        while index < 5 : 
            print("{} : {}".format(criterion_name[index], prod[criterions[index]]))
            index += 1 
            print("- -"*20)


#test this crit exists

#je veux une liste de 10 dico_prod pour la catégorie jus de fruit  

    
# def main():
#     before = datetime.now()
#     products = Fill_DB()
#     can_fill = products.check_before_fill()

#     if can_fill == False:
#         print("Erreur > La base est déjà remplie.")
#         sys.exit(0)
#     dict_prod = products.create_dict_prod()
#     print("Récupération des données terminée")
#     progression, ajout = 0, 0
#     for key in dict_prod :
#         for product in dict_prod[key]:
#             category = key
#             name = product["product_name"]
#             labels = product["labels"]
#             additives = product["additives_original_tags"]
#             nb_additives = len(product["additives_original_tags"])
#             packagings = product["packaging"]
#             nutrition_grade = product["nutrition_grades"]
#             nova_group = product["nova_group"]
#             traces = product["traces"]
#             manufacturing_places_tags = product["manufacturing_places"]
#             minerals_tags = product["minerals_tags"]
#             palm_oil = product["ingredients_from_or_that_may_be_from_palm_oil_n"]
#             #page in french
#             url = product["url"].replace("https://world.", "https://fr.", 1)
#             quantity = product["product_quantity"]
#             brands = product["brands_tags"]
#             nutriments = product["nutriments"] #full of infos
#             composition = product["ingredients_text"]

#             try :
#                 if progression == 0:
#                     print("Début de l'écriture dans la base")
#                     print(" -{}% de l'écriture effectué".format(progression))
#                 products.add_substitute(category, name, labels, additives, nb_additives, packagings,\
#                     nutrition_grade, nova_group, traces, manufacturing_places_tags, minerals_tags, \
#                     palm_oil, url, quantity, brands, nutriments, composition)
#                 ajout += 1
#                 progression = progression + ((1/400)*100)
#                 if progression in [20, 40, 60, 80, 100]:
#                     print(" -{}% de l'écriture effectués".format(progression))
#             except Exception as e :
#                 print("/!\ Il y a un problème pour cette entrée : {}.\n{}".format(name, e))
#                 sys.exit(0)

#     print("lignes prêtes à être commit : {}/400".format(ajout))
#     if ajout == 400:
#         products.mydb.commit()
#         print("lignes ajoutées à la bases : {}/400".format(ajout))
#         after = datetime.now()
#         duration = after - before
#         print(" -- Temps écoulé pour remplir la base : {} seconds --".format(duration.seconds))
#     else:
#         raise "Le nombre de lignes ne correspond pas aux attentes du programme."
