from products.models import Category, Product
import re

class Search():

    def __init__(self, get_from_input): 
        self.input = get_from_input
        self.prod = self.get_prod()

    def get_prod(self):
        try : 
            prod_found = Product.objects.get(name__icontains=self.input)
            # print(f"==>prod_found : {prod_found}")
            return prod_found
        except:
            return None


    def list_pot_prod(self, category=None): 
        """
            From a list of potential prod, returns their categories 
        """
        # return a list of prod 
        list_pot_prod = []
        for word in self.input.split(" "):
            if word in ["de", "aux", "à", "au", "des", "la", "sans"]: 
                continue
            if category: #user selected a cat
                cat = Category.objects.get(name__contains=category)
                queryset = Product.objects.filter(name__icontains=word, category=cat)
            else: #to propose cat from potential pro to user
                queryset = Product.objects.filter(name__icontains=word)

            queryset.order_by("nutriscore")
            [list_pot_prod.append(prod) for prod in queryset]
            list_pot_prod = list(set(list_pot_prod))
        if len(list_pot_prod)==0:
            return None
        return list_pot_prod

    @property
    def cat_to_choose(self): 
        """ Extracts cat from the list of potential prod"""
        list_cat = [] 
        print(f"len(list_pot_prod : {len(self.list_pot_prod())}") 
        print(self.list_pot_prod())
        for pot_prod in self.list_pot_prod():
            list_categories = pot_prod.category.all()
            [list_cat.append(cat) for cat in list_categories]
        list_cat = list(set(list_cat)) #anti doublons
        # print(f"==>list_categories : {list_cat}")
        if len(list_cat) >= 1:
            return list_cat
        return None

    def list_sub(self, category):
        """ returns a list of substitutes sorted by nutriscore 
        like dic["cat"] = [sub1, sub2, sub3 ...]"""
        list_sub = []
        list_sub = Product.objects.filter(category=category).order_by("nutriscore")
        print(f"list_sub : {list_sub} ")
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
