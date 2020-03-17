from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .form import SearchForm, AdvancedSearchForm

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

