""" this script request datas from open food fact"""
# -*- coding: utf-8 -*-
import requests
import urllib
#inspired by 
class OpenFoodFact(): 
    """ this class manages the methods to get datas"""
    def build_url(self, parameters=None):
        """builds the url for OFF api """ 
        service='cgi'
        resource_type='search.pl'
        geo_url = 'https://fr.openfoodfacts.org'
        base_url = "/".join([geo_url, service, resource_type])
        extension = urllib.parse.urlencode(parameters)
        base_url = "?".join([base_url, extension])

        return base_url

    def advanced_search(self, post_query):
        """ manages the parameters to get a json response"""
        post_query['json'] = '1'
        url = self.build_url(parameters=post_query)
        response = requests.get(url)
        response = response.json()
        return response

    def this_cat_exists(self, cat):
        """ tests whether the wanted cat exists in OFF"""
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
