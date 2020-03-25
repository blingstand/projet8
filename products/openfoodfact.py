# -*- coding: utf-8 -*-
import requests
import urllib

class OpenFoodFact(): 
    def build_url(self, parameters=None):
        service='cgi'
        resource_type='search.pl'
        geo_url = 'https://fr.openfoodfacts.org'
        base_url = "/".join([geo_url, service, resource_type])
        extension = urllib.parse.urlencode(parameters)
        base_url = "?".join([base_url, extension])

        return base_url

    def advanced_search(self, post_query):

        post_query['json'] = '1'
        url = self.build_url(parameters=post_query)
        response = requests.get(url)
        response = response.json()
        return response

    def this_cat_exists(self, cat):
        response = self.advanced_search({
        "search_terms":"",
        "tagtype_0":"categories ",
        "tag_contains_0":"contains",
        "tag_0": cat,
        "tagtype_1":"countries  ",
        "tag_contains_1":"contains",
        "tag_1":"France"})
        if len(response['products']) >= 1:
            return True
        return False

off = OpenFoodFact()
cat = "jus de fruits"
rep = off.this_cat_exists(cat)
print("la catégorie({}) est-elle présente dans la base de donnée OFF ?\n>Réponse : {}".format(cat, rep))