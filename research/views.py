from django.shortcuts import render
from django.views import View

from .form import SearchForm

# Create your views here.
class SearchFormView(View):
	"""manage a HttpResponse in case of get or post method request"""
	
	def get(self, request):
		""" manage the HttpResponse for the SearchFormView with get method request """
		form = SearchForm()
		context={'form' : form}
		return render(request, "research/searchForm.html", context)

	def post(self, request):
		pass
