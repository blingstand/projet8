""" this scripts manages the views for the app reserach """
#django
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

#from other app
from user.form import AddFavorite
# from products.models import Category, Product

#from app
from .form import SearchForm
from .searcher import Search

# Create your views here.

def make_a_search(get_from_input, wanted, given_category=None):
    """ returns the wanted value after a search based on input and sometime category"""
    search = Search(get_from_input)
    if given_category is not None:
        prod = search.list_pot_prod(given_category)[0]
        category = prod.category.all()[0]
        substitutes = search.list_sub(category)
    else:
        prod = search.prod
        categories = search.cat_to_choose
    if wanted == ["prod", "sub"]:
        return search, prod, substitutes
    if wanted == ["prod", "categories"]:
        return search, prod, categories
    return f"Verifie le paramètre wanted (valeur actuelle : {wanted})"

class titi(View):
    def get(self, request):
        return render(request, "research/titi.html") 


class ResultsView(View):
    """ manages a HttpResponse in case of get or post method
    request for this url research/advancedSearch"""
    def get(self, request, category=None, get_from_input=None):
        """ manages the get request for the results page """
        try:
            fav_form = AddFavorite()
            print("cas results")
            if category is not None:
                prod, substitutes = make_a_search(
                    get_from_input=get_from_input,
                    wanted=["prod", "sub"],
                    given_category=category)[1:]
                if prod is not None:
                    context = {
                        "product" : prod, "substitutes" : substitutes, "no_prod" : True,
                        'fav_form' : fav_form}
                    return render(request, "research/results.html", context)
            return redirect("research:index")
        except Exception as err:
            print(err)
            return redirect("research:index")


class IndexView(View):
    """ manages the requests for the index page """
    def get(self, request):
        """ manages the get requests for the index page """
        return render(request, 'research/index.html')

    def post(self, request):
        """ manages the post for the index page """
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            #I throw a search
            get_from_input = search_form.cleaned_data["simple_search"] \
            or search_form.cleaned_data["mini_simple_search"]
            #I write result in context
            search, prod, categories = make_a_search(
                get_from_input=get_from_input,
                wanted=["prod", "categories"])
            if prod is not None:
                print("* la recherche mène au cas 1")
                category = prod.category.first()
                substitutes = search.list_sub(category)

                context = {
                    "product" : prod,
                    "nutriscore" : prod.nutriscore.upper(),
                    "substitutes" : substitutes,
                }
                return render(request, "research/results.html", context)
            if categories is not None:
                print("* la recherche mène au cas 2")
                messages.error(request, "Pas de résultats parfaitement identiques "\
                    f"dans la base actuellement pour la recherche : {get_from_input}.")
                context = {
                    "categories" : categories,
                    'however' : " Cependant j'ai des résultats en rapport avec ta recherche ...",
                    'get_from_input' : get_from_input, "few_cat" : len(categories) <= 3}
                return render(request, 'research/index.html', context)
            print("* la recherche mène au cas 3")
            messages.error(request, "Pas de résultats dans la base actuellement pour"\
                f" la recherche : {get_from_input}.")
            context = {"search_form": search_form}
            return render(request, "research/index.html", context)

        return HttpResponse("Problème dans le formulaire")

    #pour la version 2.0 ---------- en cours de réflexion
# class AdvancedSearchView(View):
#     """ manage a HttpResponse in case of get or post method
#     request for this url research/advancedSearch"""

#     def get(self, request):
#         """ manage the HttpResponse for the SearchFormView with get method request """
#         adv_form = AdvancedSearchForm()
#         search_form = SearchForm()
#         context={'adv_form' : adv_form}
#         return render(request, "research/advancedSearch.html", context)

#     def post(self, request):
#         form = AdvancedSearchForm(request.POST)
#         search_form = SearchForm()
#         results=(1,2,3)
#         if form.is_valid():
#             results = [r for r in range(10)]
#             context = { "results" : results, "search_form":search_form}
#             return render(request, "research/results.html", context)
#         return HttpResponse("Pb dans le form")
