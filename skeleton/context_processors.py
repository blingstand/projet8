from research.form import SearchForm

def get_search_form(request):
	search_form = SearchForm()
	dico = {"search_form":search_form}
	return dico