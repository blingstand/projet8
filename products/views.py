
from django.shortcuts import render, redirect
from django.views import View

import products.models as pm

# Create your views here.
class myBddView(View):

	def get(self, request): 
		nb_cat = len(pm.Category.objects.all())
		nb_prod = len(pm.Product.objects.all())
		context = { "nb_cat" : nb_cat, "nb_prod" : nb_prod, "last_maj" : "aujourd'hui" } 
		return render(request, "products/myBdd.html", context)

	def post(self, request):
		pass