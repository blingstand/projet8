from products.models import Category, Product
import re

def find_subs(get_from_input): 
    """
        returns a list of substitutes
    """
    print("* * * "*10)
    print("je cherche dans la base pour le mot : {}".format(get_from_input))
    prod_found = Product.objects.filter(name__contains=get_from_input)
    
    if not prod_found.exists() : 
        print("résultat :", prod_found.exists(), "je recherche mot à mot ...")
        # return a list of prod 
        dico = {}    
        for word in get_from_input.split(" "):
            if word in ["de"]: 
                continue
            print("- - -")
            print(word)
            list_obj_prod = Product.objects.filter(name__contains=word)
            print(list_obj_prod.exists())
            print(type(list_obj_prod))
            print([prod.category.name for prod in list_obj_prod])
            if list_obj_prod.exists():
                dico[word] = list_obj_prod
            print("- - - - "*5)
        print("dico final", dico)
        good_prods_nutriscore = [prod.nutriscore for prod in prod_found]
    else : 

        print("\trésultat :", prod_found.exists(),">", prod_found[0])
        cat_found = prod_found[0].category
        print("\tIl appartient à la catégorie :", cat_found.name)
        print("\tJe cherche donc des substituts ...")
        substituts_same_cat = Product.objects.filter(category=cat_found)
        best_nutriscore = min([sub.nutriscore for sub in substituts_same_cat])
        print("\tMeilleur nutriscore :", best_nutriscore)
        search = Product.objects.filter(category=cat_found, nutriscore=best_nutriscore)
        print("\tNombre de substituts : {}, j'enlève les conditionnement en plastique.".format(len(search)))
        list_best_sub = []
        for count, sub in enumerate(search): 
            if "plastique" in sub.packaging.split(",") \
            or "Plastique" in sub.packaging.split(","):
                pass
            else:
                list_best_sub.append(sub)
        print("\tNombre de substituts : {}.".format(len(list_best_sub))) 
        print("* * * "*10)   
        return prod_found[0], list_best_sub