from products.models import Category, Product
import re

class Search():

    def __init__(self, get_from_input, given_category=None): 
        self.input = get_from_input
        self.category = given_category
        if self.prod is not None:
            self.cat_from_prod = self.prod.category.all()[0]
    
    @property
    def prod(self):
        try : 
            if self.category is not None:
                query_category = Category.objects.get(name__contains=self.category)
                prod_found = Product.objects.get(
                    name__contains=self.input, 
                    category=query_category)
                return prod_found
            prod_found = Product.objects.get(name__contains=self.input)
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
            if word in ["de", "aux", "à", "au", "des", "la"]: 
                continue
            print("\t- - -\n\t", word)
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
        print(f"contenu de list_pot_prod : {self.list_pot_prod()}")
        for pot_prod in self.list_pot_prod():
            list_categories = pot_prod.category.all()
            print(pot_prod, list_categories)
            [list_cat.append(cat) for cat in list_categories]
            print(list_cat)
        list_cat = list(set(list_cat)) #anti doublons
        print(f"==>list_categories : {list_cat}")
        if len(list_cat) >= 1:
            return list_cat
        return None

    @property
    def list_sub(self):
        """ return a dictionary like dic["cat"] = [sub1, sub2, sub3 ...]"""
        list_sub_best_nutriscore = []
        list_sub = []
        if self.prod is not None: 
            list_sub = Product.objects.filter(category=self.cat_from_prod).order_by("nutriscore")
            for sub in list_sub:
                print(sub)
                if sub.nutriscore <= self.prod.nutriscore:
                    list_sub_best_nutriscore.append(sub) 
        elif self.category:
            category = Category.objects.get(name__contains=self.category)    
            list_sub = self.list_pot_prod(category)
            best_nutriscore = min([sub.nutriscore for sub in list_sub])
            print(f"best_nutriscore : {best_nutriscore}")
            for sub in list_sub:
                if sub.nutriscore <= best_nutriscore:
                    list_sub_best_nutriscore.append(sub)
        print(f"\t- - -\nlist_sub_best_nutriscore : {list_sub_best_nutriscore}")
        return list_sub


    #idea for later
    def kick_plastic(self, cat):
        """ kick plastic from the dico of substitutes """
        no_plastic = []
        for count, sub in enumerate(self.list_sub): 
            if "plastique" in sub.packaging.split(",") \
            or "Plastique" in sub.packaging.split(","):
                pass
            else:
                no_plastic.append(sub)
        return no_plastic 
