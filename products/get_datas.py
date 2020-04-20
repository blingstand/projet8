"""This script extracts the datas from OFF json response in order to return a dictionnary
with cat and prod to facilitate the population of the db"""
#!/usr/bin/python3
# -*- coding: utf8 -*-

from products.openfoodfact import OpenFoodFact

class GetDatas():
    """ this class manages the method to extract, organise and return the datas"""
    SIZE_RESEARCH = 100
    # criterions = ("product_name", "packaging", "nutrition_grades", "url", "image_url" )

    def __init__(self, size, category, criterions):
        """ initiate the instance"""
        self.size = size
        self.category = category
        self.criterions = criterions

    def call_api(self, category):
        """ Finds self.SIZE_RESEARCH prods from a given cat """
        off = OpenFoodFact()
        results = off.advanced_search({
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

    def _kick_duplicates(self, my_list):
        """ Kickes the prod with a duplicate name"""

        list_prod_name = []
        list_prod = []
        exceptions = []
        for prod in my_list: #selects prod from list of products
            try:
                name = prod["product_name"].lower()
                if name[:5] == "arroz":
                    print(f"----------------------------{name}")
                    exceptions.append(prod)
            except KeyError:
                exceptions.append(prod)
                continue
            if name not in list_prod_name and prod not in exceptions: #anti-duplicate name
                list_prod_name.append(name)
                list_prod.append(prod)
        return list_prod
    def _kick_empty_values(self, my_list):
        """kickes a prod from the list if there is no value for 1 selected column"""
        accepted_prod, list_prod = [], []
        for prod in my_list:
            for criterion in self.criterions:
                try: #to fix error
                    if prod[criterion] != None and prod not in accepted_prod:
                        accepted_prod.append(prod)
                except:
                    accepted_prod.remove(prod)
                    break
        for prod in accepted_prod:
            list_prod.append(prod)

        return list_prod
    def _respect_size(self, my_list):
        """ Limits the number of elements """
        list_resp_size = []
        for prod in my_list:
            if len(list_resp_size) < self.size:
                list_resp_size.append(prod)
        return list_resp_size
    def _just_keep_criterions(self, my_list):
        """ return a list filled by dicts of product with only cols present in self.criterions"""
        new_list = []
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
        """ Searches in API and returns a list of prods """

        first_list_prod = self.call_api(category) #list of 50 prods with same cat
        #list prod with no duplicate names
        list_with_no_duplicate_name = self._kick_duplicates(first_list_prod)

        #list with no empty values for selected columns
        list_without_empty = self._kick_empty_values(list_with_no_duplicate_name)

        #keep just the col writen in self.TUP_COL
        list_prod_with_selec_col = self._just_keep_criterions(list_without_empty)

        #list do not pass the SIZE_IN_TAB limit
        list_prod_resp_size = self._respect_size(list_prod_with_selec_col)

        return list_prod_resp_size
    def create_dict_cat(self):
        """Creates the dict_prod with previous functions  """

        dict_prod = {} #create dico
        for cat in self.category:
            list_prod = self._get_list_for_cat(cat)
            dict_prod[cat] = list_prod

        return dict_prod
