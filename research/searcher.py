from products.models import Category, Product
import re

def find_subs(get_from_input, given_category=None): 
    """
        returns a list of substitutes
    """
    print("* * * "*10)
    print("je cherche dans la base pour le mot : {}".format(get_from_input))
    prod_found = Product.objects.filter(name__contains=get_from_input)
    if given_category is not None:
        query_category = Category.objects.get(name__contains=given_category)
        prod_found = Product.objects.filter(
            name__contains=get_from_input, 
            category=query_category)
    find_smth = prod_found.exists()
    if not find_smth : 
        print("\tRésultat : {}, je recherche mot à mot ...".format(find_smth))
        # return a list of prod 
        dico = {}    
        list_queryset = []
        
        for word in get_from_input.split(" "):
            if word in ["de", "aux", "à", "au", "des"]: 
                continue
            print("\t- - -\n\t", word)
            list_obj_prod = Product.objects.filter(name__contains=word)
            if given_category:
                list_obj_prod = Product.objects.filter(name__contains=word, category=query_category)
            print("\t{} résultats.".format(len(list_obj_prod)))
            [list_queryset.append(prod) for prod in list_obj_prod]
        
        print("\t- - -\n\t{} résultats.".format(list_queryset))
        if len(list_queryset) != 0:
            for queryset in list_queryset:
                try:
                    dico[queryset.category.name].append(queryset)
                except : 
                    dico[queryset.category.name] = []
                    dico[queryset.category.name].append(queryset)
            
        print("\t- - -\n", "\n\tdico final", dico, "\n\t- - -\n")
        if given_category is not None:
            return False, None, dico[given_category]
        return False, None, dico
    else : 

        print("\trésultat :", find_smth,">", prod_found[0])
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
        return find_smth, prod_found[0], list_best_sub