from django.shortcuts import render
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
		pass