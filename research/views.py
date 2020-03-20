from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .form import SearchForm, AdvancedSearchForm

from products.models import Category, Product
# Create your views here.

class AdvancedSearchView(View):
	""" manage a HttpResponse in case of get or post method 
	request for this url research/advancedSearch"""

	def get(self, request):
		""" manage the HttpResponse for the SearchFormView with get method request """
		form = AdvancedSearchForm()
		context={'form' : form}
		return render(request, "research/advancedSearch.html", context)

	def post(self, request):
		form = AdvancedSearchForm(request.POST)
		results=(1,2,3)
		if form.is_valid():
			results = [r for r in range(10)]
			context = { "results" : results}
			return render(request, "research/results.html", context)
		return HttpResponse("Pb dans le form")

class ResultsView(View):
	""" manage a HttpResponse in case of get or post method 
	request for this url research/advancedSearch"""

	def get(self, request):
		""" manage the HttpResponse for the SearchFormView with get method request """
		return render(request, "research/results.html")

class IndexView(View):
	
	def get(self, request):
	    # message = "Bienvenu sur le site pureBeurre !"
	    form = SearchForm()
	    context = { 'form' : form }
	    return render(request, 'research/index.html', context)
	
	def post(self, request):
		form = SearchForm(request.POST)
		if form.is_valid(): 
			#I throw a search 
			get_from_input = form.cleaned_data["simple_search"] 
			#I write result in context
			results = Product.objects.get(name__contains=get_from_input)
			# all_result = [result for result in results]
			context = { "name" : results.name, "link_image" : results.image_url }
			# #I display a result page with results
			return render(request, "research/results.html", context)
		return HttpResponse ("Problème dans le formulaire")