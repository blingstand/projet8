from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import Category, Product

def get_last_maj():
    last_maj_cat = max([all_cat.last_maj_0 for all_cat in Category.objects.all()])
    last_maj_prod = max([all_prod.last_maj_0 for all_prod in Product.objects.all()])
    last_maj = max([last_maj_cat, last_maj_prod])
    return last_maj

class myBddView(View):

    def get(self, request, actualize=0): 
        if actualize == 1:
            pass
        nb_cat = len(Category.objects.all())
        nb_prod = len(Product.objects.all())
        context = { "nb_cat" : nb_cat, "nb_prod" : nb_prod, "last_maj" : get_last_maj()} 
        return render(request, "products/myBdd.html", context)

    def post(self, request):
        pass