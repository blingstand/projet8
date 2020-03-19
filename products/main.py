#!/usr/bin/python3
# -*- coding: utf8 -*-
from fill_db.get_datas_from_off import Fill_DB


categories = ("Jus de fruits", "Céréales", "Confiture", "Barre chocolatee",\
    "Lait", "Chips", "Bretzels", "Yaourts", "Poissons", "Gâteaux", \
    "Pains de mie", "Charcuterie","Pizzas", "Tartes salées", "Spaghetti", "Riz",\
    "Glaces", "Chocolat noir", "Soupes", "Compotes" )

for cat in categories:
    new_line = Category(cat)
    
# criterions = ("product_name", "packaging", "nutrition_grades", "url", "image_url" )
# criterion_name = ("nom", "conditionnement", "nutriscore", "lien", "lien vers image" )

# category = ["Jus de fruits", "Céréales"]
# fdb = Fill_DB(3, category, criterions)
# dico_cat = fdb.create_dict_prod()

# for cat in category:  
#     dico_prod = dico_cat[cat]
#     print("- -"*20)
    
#     for prod in dico_prod:
#         index = 0
#         print("n°{}".format(count+1))
#         print("category : ", cat)
#         while index < 5 : 
#             print("{} : {}".format(criterion_name[index], prod[criterions[index]]))
#             index += 1 
#             print("- -"*20)