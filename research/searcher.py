from products.models import Category, Product
import re

class Search():

    def __init__(self, get_from_input, given_category=None): 
        self.input = get_from_input
        self.category = given_category
        self.prod = self.get_prod()
        if self.prod is not None:
            self.cat_from_prod = self.prod.category.all()[0]
    
    def get_prod(self):
        try : 
            prod_found = Product.objects.get(name__contains=self.input)
            # print(f"==>prod_found : {prod_found}")
            return prod_found
        except:
            return None


    def list_pot_prod(self, cat=None): 
        """
            From a list of potential prod, returns their categories 
        """
        # return a list of prod   
        list_pot_prod = []
        
        for word in self.input.split(" "):
            if word in ["de", "aux", "à", "au", "des", "la", "sans"]: 
                continue
            if cat: 
                queryset = Product.objects.filter(name__contains=word, category=cat)
            else:
                queryset = Product.objects.filter(name__contains=word)

            queryset.order_by("nutriscore")
            [list_pot_prod.append(prod) for prod in queryset]
        return list_pot_prod

    @property
    def cat_to_choose(self): 
        """ Extract cat from the list of potential prod"""
        list_cat = [] 
        for pot_prod in self.list_pot_prod():
            list_categories = pot_prod.category.all()
            [list_cat.append(cat) for cat in list_categories]
        list_cat = list(set(list_cat)) #anti doublons
        # print(f"==>list_categories : {list_cat}")
        if len(list_cat) >= 1:
            return list_cat
        return None

    @property
    def list_sub(self):
        """ return a dictionary like dic["cat"] = [sub1, sub2, sub3 ...]"""
        list_sub_best_nutriscore = []
        list_sub = []
        list_sub = Product.objects.filter(category=self.cat_from_prod).order_by("nutriscore")
        for sub in list_sub:
            if sub.nutriscore <= self.prod.nutriscore:
                list_sub_best_nutriscore.append(sub) 
        # print(f"\t- - -\nlist_sub_best_nutriscore : {list_sub_best_nutriscore}")
        return list_sub


    #idea for later
    # def kick_plastic(self, cat):
    #     """ kick plastic from the dico of substitutes """
    #     no_plastic = []
    #     for count, sub in enumerate(self.list_sub): 
    #         if "plastique" in sub.packaging.split(",") \
    #         or "Plastique" in sub.packaging.split(","):
    #             pass
    #         else:
    #             no_plastic.append(sub)
    #     return no_plastic 
