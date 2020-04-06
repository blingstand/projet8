#django
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

#from app
from .form import SearchForm, AdvancedSearchForm
from .searcher import Search

#from other app 
from user.form import AddFavorite
from products.models import Category, Product
# Create your views here.


class ResultsView(View):
    """ manage a HttpResponse in case of get or post method 
    request for this url research/advancedSearch"""
    search_form = SearchForm()
    def get(self, request, category=None, get_from_input=None):
        """ manage the HttpResponse for the SearchFormView with get method request """
        fav_form = AddFavorite()
        print(f"cat : {category}, get_from_input : {get_from_input} ")
        if category is not None:
            search = Search(get_from_input)
            print(f"Cas result get : {get_from_input} et {category}")
            prod = search.list_pot_prod(category)[0]
            print(f"J'ai {prod} ! ")
            category = prod.category.all()[0]
            print(f"j'ai category : {category}")
            substitutes = search.list_sub(category) 
            print(f"Voici les substituts : {substitutes}")
            context = { 
            "product" : prod, "substitutes" : substitutes, "no_prod" : True, 
            'fav_form' : fav_form, 'search_form' : self.search_form}
            return render(request, "research/results.html", context)
        return redirect("research:index")

    def post(self, request, category=None, get_from_input=None):
        pass

class IndexView(View):
    """ gère les index """
    def get(self, request):
        search_form = SearchForm()
        context = {'search_form' : search_form}
        return render(request, 'research/index.html', context)
    
    def post(self, request):
        search_form = SearchForm(request.POST)
        if search_form.is_valid(): 
            #I throw a search 
            get_from_input = search_form.cleaned_data["simple_search"] \
            or search_form.cleaned_data["mini_simple_search"]
            #I write result in context
            search = Search(get_from_input)
            # print("* * * "*10)
            print(f"je cherche dans la base pour la recherche : {get_from_input}")
            prod = search.prod
            print("prod -->", prod)
            categories = search.cat_to_choose
            print("categories -->", categories)
            if prod is not None:
                print("cas 1")
                category = prod.category.first()
                substitutes = search.list_sub(category)
                # print("Résultats : le produit recherché était", prod,\
                #     "et voici les substituts trouvés :\n", substitutes)
                # print("* * * "*10)
                context = { 
                "product" : prod, 
                "nutriscore" : prod.nutriscore.upper(), 
                "substitutes" : substitutes, 
                'search_form' : search_form
                }
                return render(request, "research/results.html", context)
            elif categories is not None:
                print("cas 2")
                messages.error(request, "Pas de résultats parfaitement identiques "\
                    f"dans la base actuellement pour la recherche : {get_from_input}.")
                context = { 
                    'search_form' : search_form, "categories" : categories,
                    'however' : " Cependant j'ai des résultats en rapport avec ta recherche ...", 
                    'get_from_input' : get_from_input, "few_cat" : len(categories) <= 3}
                return render(request, 'research/index.html', context)
            else:
                print("cas 3")
                messages.error(request, "Pas de résultats dans la base actuellement pour"\
                    f" la recherche : {get_from_input}.")
                return redirect("research:index")
                
            context = {"search_form": search_form}
            return render(request, "research/index.html", context)
            
        return HttpResponse ("Problème dans le formulaire")

    #pour la version 2.0
class AdvancedSearchView(View):
    """ manage a HttpResponse in case of get or post method 
    request for this url research/advancedSearch"""

    def get(self, request):
        """ manage the HttpResponse for the SearchFormView with get method request """
        adv_form = AdvancedSearchForm()
        search_form = SearchForm()
        context={'adv_form' : adv_form, 'search_form' : search_form}
        return render(request, "research/advancedSearch.html", context)

    def post(self, request):
        form = AdvancedSearchForm(request.POST)
        search_form = SearchForm()
        results=(1,2,3)
        if form.is_valid():
            results = [r for r in range(10)]
            context = { "results" : results, "search_form":search_form}
            return render(request, "research/results.html", context)
        return HttpResponse("Pb dans le form")
